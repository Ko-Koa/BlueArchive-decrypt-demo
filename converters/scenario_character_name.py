from typing import Any

from alive_progress import alive_bar

from FlatData.ProductionStep import ProductionStep
from FlatData.ScenarioCharacterNameExcel import ScenarioCharacterNameExcel
from FlatData.ScenarioCharacterShapes import ScenarioCharacterShapes
from modules.loader import ConverterMeta
from modules.converter import DBConverter


__converter__meta__ = ConverterMeta(
    aim_file="ScenarioCharacterNameDBSchema", dist_file_name="scenario_character_name"
)


class Converter(DBConverter[ScenarioCharacterNameExcel]):
    def __init__(self) -> None:
        super().__init__("ScenarioCharacterNameDBSchema", ScenarioCharacterNameExcel)

    def parse_data(self, data: Any) -> list[dict[str, Any]]:
        results = []
        total_length = len(data)
        with alive_bar(total_length, manual=True, title="解析数据") as bar:
            for index in range(total_length):
                root = ScenarioCharacterNameExcel.GetRootAs(data[index][1])
                meta = {
                    "character_name": root.CharacterName(),
                    "production_step": ProductionStep(root.ProductionStep()).name,
                    "name_kr": root.NameKr(),
                    "nickname_ke": root.NicknameKe(),
                    "name_jp": root.NameJp(),
                    "nickname_jp": root.NicknameJp(),
                    "name_th": root.NameTh(),
                    "nickname_th": root.NicknameTh(),
                    "name_tw": root.NameTw(),
                    "nickname_tw": root.NicknameTw(),
                    "name_en": root.NameEn(),
                    "nickname_en": root.NicknameEn(),
                    "shape": ScenarioCharacterShapes(root.Shape()).name,
                    "spine_prefab_name": root.SpinePrefabName(),
                    "small_portrait": root.SmallPortrait(),
                }
                
                bar((index + 1) / total_length)
                results.append(meta)

        return results
