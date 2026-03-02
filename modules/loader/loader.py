import pkgutil
import importlib
from typing import Type, Optional

from loguru import logger

from .models import ConverterMeta
from modules.converter import BaseConverter


class ConverterPlugin(object):
    __slots__ = ("converter", "save_name")

    def __init__(
        self,
        converter: BaseConverter,
        aim_file: str,
        dist_file_name: Optional[str] = None,
    ) -> None:
        self.converter = converter
        self.save_name = dist_file_name or aim_file.split(".")[0]


_converters: dict[str, ConverterPlugin] = {}


def load_converter(converter_path: str):
    """加载转换器"""
    try:
        module = importlib.import_module(converter_path)
        converter_meta: ConverterMeta | None = getattr(
            module, "__converter__meta__", None
        )
        if converter_meta is None:
            logger.error(f"转换器 {converter_path} 缺失 __converter__meta__")
            return False

        converter: Type[BaseConverter] | None = getattr(module, "Converter", None)
        if converter is None:
            logger.error(f"转换器 {converter_path} 缺失 Converter 类")
            return False

        aim_file = converter_meta.aim_file
        dist_file_name = converter_meta.dist_file_name

        converter_plugin = ConverterPlugin(
            converter=converter(), aim_file=aim_file, dist_file_name=dist_file_name
        )
        _converters[aim_file] = converter_plugin
        logger.success(f'加载转换器 "{converter_path.split(".")[-1]}"')

    except Exception as e:
        logger.opt(exception=True).error(f"加载转换器 {converter_path} 发生错误")
        return False


def load_converters(package_name: str):
    """加载所有转换器"""
    plugins_package = importlib.import_module(package_name)
    module_list = pkgutil.iter_modules(plugins_package.__path__)
    for module in module_list:
        module_name = plugins_package.__name__ + "." + module.name
        load_converter(module_name)


def get_converters():
    return _converters


__all__ = ["load_converters", "get_converters"]
