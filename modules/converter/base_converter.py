import json
from typing import Any, Optional
from abc import ABC, abstractmethod


def bytes_handler(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8")  # 将 bytes 转为 string
    raise TypeError(f"Type not serializable: {type(obj)}")


class BaseConverter(ABC):
    @abstractmethod
    def load_data(self) -> Any:
        """加载数据"""
        pass

    @abstractmethod
    def parse_data(self, data: Any) -> list[dict[str, Any]]:
        """解析数据"""
        pass

    def convert(self, save_path: Optional[str] = None):
        """转换数据
        - save_path(Optional[str]):保存路径,当为None时,则不进行保存

        """
        data = self.load_data()
        parsed_data = self.parse_data(data)

        if save_path is not None:
            with open(save_path, "w") as f:
                json.dump(
                    obj=parsed_data,
                    fp=f,
                    ensure_ascii=False,
                    indent=4,
                    default=bytes_handler,
                )

        return parsed_data
