import os

from loguru import logger

from config.project import project_path
from modules.loader import load_converters, get_converters

if __name__ == "__main__":
    dist_path = os.path.join(project_path, "dist")
    if not os.path.exists(dist_path):
        os.mkdir(dist_path)

    files = ["systemmailexceltable.bytes"]

    # 使用db_collections需要将ExcelDB.db放入config.yaml中对应的位置
    db_collections = [
        # "CharacterDBSchema",
        # "ScenarioCharacterNameDBSchema",
        # "ScenarioScriptDBSchema",
    ]

    load_converters("converters")
    converters = get_converters()

    # 转换本地文件
    for file in files:
        converter_plugin = converters.get(file)
        if converter_plugin is None:
            logger.warning(f"文件 {file} 没有对应的转换器")
            continue

        converter = converter_plugin.converter
        save_name = converter_plugin.save_name

        save_path = os.path.join(dist_path, f"{save_name}.json")
        converter.convert(save_path)
        logger.success(f"{save_name} 转换完成")

    # 转换数据库中的文件
    for db_collection in db_collections:
        converter_plugin = converters.get(db_collection)
        if converter_plugin is None:
            logger.warning(f"数据库表 {db_collection} 没有对应的转换器")
            continue

        converter = converter_plugin.converter
        save_name = converter_plugin.save_name

        save_path = os.path.join(dist_path, f"{save_name}.json")
        converter.convert(save_path)
        logger.success(f"{save_name} 转换完成")
