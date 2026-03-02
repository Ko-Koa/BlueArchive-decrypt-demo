# 项目设置
import os
import sys
from typing import Optional

import yaml
from pydantic import BaseModel


class YamlConfigModel(BaseModel):
    excel_path: Optional[str]
    excel_db_path: Optional[str]


def get_project_path():
    """获取项目根目录路径"""
    if getattr(sys, "frozen", False):
        # 打包后的执行环境
        return os.path.dirname(os.path.realpath(sys.executable))
    else:
        # 开发环境
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_yaml_config():
    """获取yaml配置"""
    yaml_path = os.path.join(get_project_path(), "config.yaml")
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return YamlConfigModel(**data)


# 项目目录
project_path = get_project_path()

# YAML配置数据
yaml_config = get_yaml_config()
