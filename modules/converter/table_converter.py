from csv import excel
import os
from typing import Any, Type, TypedDict, TypeVar, Generic

from .base_converter import BaseConverter
from ..crypto import XOR, create_key, TableDecrypt
from config.project import yaml_config

T = TypeVar("T")


class TableConvertConfig(TypedDict):
    """转换器配置
    - file_name(str):文件名称
    - key(str): 密码
    - table_key(str):table字段解密使用的key
    """

    file_name: str
    key: str
    table_key: str


class TableConverter(Generic[T], BaseConverter):
    """用于转换Excel.zip解压出来的bytes文件,通常经过加密"""

    def __init__(self, config: TableConvertConfig, fb_type: Type[T]) -> None:
        self.config = config
        self.fb_type = fb_type

        super().__init__()

    def decrypt_value(self, data: Any):
        """对字段进行解密"""
        key = create_key(self.config["table_key"], 8)
        return TableDecrypt.decrypt_table_value(data=data, key=key)

    def load_data(self) -> Any:
        file_name = self.config["file_name"]
        excel_path = yaml_config.excel_path
        if excel_path is None:
            raise Exception("未设置excel_path,请在config.yaml中进行配置!!")

        file_path = os.path.join(excel_path, f"{file_name}.bytes")
        with open(file_path, "rb") as f:
            file_data = f.read()

        return XOR(bytearray(file_data), self.config["key"])
