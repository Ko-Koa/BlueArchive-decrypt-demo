from pydantic import BaseModel
from typing import Optional


class ConverterMeta(BaseModel):
    """转换器插件meta数据约定
    - target (str): 转换器目标文件(带扩展名)或者对应数据库中的collection名字
    - dist_file_name (Optional[str]):转换之后的文件名称,默认使用taget名称
    """

    aim_file: str
    dist_file_name: Optional[str] = None


__all__ = ["ConverterMeta"]
