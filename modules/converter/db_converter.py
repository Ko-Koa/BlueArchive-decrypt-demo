from typing import Any, Type, TypeVar, Generic

from .base_converter import BaseConverter
from modules.excel_db_manager import excel_db

T = TypeVar("T")


class DBConverter(Generic[T], BaseConverter):
    def __init__(self, collection_name: str, fb_type: Type[T]) -> None:
        self.collection_name = collection_name
        self.fb_type = fb_type
        super().__init__()

    def load_data(self) -> Any:
        return list(excel_db.cursor.execute(f"SELECT * FROM {self.collection_name}"))
