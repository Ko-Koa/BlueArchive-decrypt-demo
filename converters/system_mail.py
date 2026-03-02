from os import name
from typing import Any

from FlatData.MailType import MailType
from modules.loader import ConverterMeta
from FlatData.SystemMailExcelTable import SystemMailExcelTable
from modules.converter.table_converter import TableConverter, TableConvertConfig

__converter__meta__ = ConverterMeta(aim_file="systemmailexceltable.bytes")


class Converter(TableConverter[SystemMailExcelTable]):
    def __init__(self) -> None:
        config: TableConvertConfig = {
            "file_name": "systemmailexceltable",
            "key": "SystemMailExcelTable",
            "table_key": "SystemMail",
        }
        super().__init__(config, SystemMailExcelTable)

    def parse_data(self, data: Any) -> list[dict[str, Any]]:
        results = []
        root = SystemMailExcelTable.GetRootAs(data)
        for index in range(root.DataListLength()):
            table = root.DataList(index)
            if table is None:
                continue

            comment = self.decrypt_value(table.Comment())
            sender = self.decrypt_value(table.Sender())
            mail_type_value = self.decrypt_value(table.MailType())
            expired_day = self.decrypt_value(table.ExpiredDay())

            meta = {
                "mail_type": MailType(mail_type_value).name,
                "expired_day": expired_day,
                "comment": comment,
                "sender": sender,
            }

            results.append(meta)

        return results
