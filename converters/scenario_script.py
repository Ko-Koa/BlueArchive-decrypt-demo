from typing import Any

from alive_progress import alive_bar

from FlatData.ScenarioScriptExcel import ScenarioScriptExcel
from modules.loader import ConverterMeta
from modules.converter import DBConverter


__converter__meta__ = ConverterMeta(
    aim_file="ScenarioScriptDBSchema", dist_file_name="scenario_script"
)


class Converter(DBConverter[ScenarioScriptExcel]):
    def __init__(self) -> None:
        super().__init__("ScenarioScriptDBSchema", ScenarioScriptExcel)

    def parse_data(self, data: Any) -> list[dict[str, Any]]:
        results = []
        total_length = len(data)
        with alive_bar(total_length, manual=True, title="解析数据") as bar:
            for index in range(total_length):
                root = ScenarioScriptExcel.GetRootAs(data[index][1])
                meta = {
                    "group_id": root.GroupId(),
                    "selection_group": root.SelectionGroup(),
                    "bgm_id": root.BgmId(),
                    "sound": root.Sound(),
                    "transition": root.Transition(),
                    "bg_name": root.BgName(),
                    "bg_effect": root.BgEffect(),
                    "popup_file_name": root.PopupFileName(),
                    "script_kr": root.ScriptKr(),
                    "text_jp": root.TextJp(),
                    "text_th": root.TextTh(),
                    "text_tw": root.TextTw(),
                    "text_en": root.TextEn(),
                    "voice_id": root.VoiceId(),
                    "teen_mode": root.TeenMode(),
                }
                bar((index + 1) / total_length)
                results.append(meta)

        return results
