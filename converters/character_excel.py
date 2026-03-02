from typing import Any

from alive_progress import alive_bar

from FlatData.AimIKType import AimIKType
from FlatData.Club import Club
from FlatData.EquipmentCategory import EquipmentCategory
from FlatData.School import School
from FlatData.SquadType import SquadType
from FlatData.StatLevelUpType import StatLevelUpType
from FlatData.Tag import Tag
from modules.loader import ConverterMeta
from modules.converter import DBConverter
from FlatData.CharacterExcel import CharacterExcel
from FlatData.Rarity import Rarity
from FlatData.TacticEntityType import TacticEntityType
from FlatData.TacticRole import TacticRole
from FlatData.WeaponType import WeaponType
from FlatData.TacticRange import TacticRange
from FlatData.BulletType import BulletType
from FlatData.ArmorType import ArmorType

__converter__meta__ = ConverterMeta(
    aim_file="CharacterDBSchema", dist_file_name="character"
)


class Converter(DBConverter[CharacterExcel]):
    def __init__(self) -> None:
        super().__init__("CharacterDBSchema", CharacterExcel)

    def parse_data(self, data: Any) -> list[dict[str, Any]]:
        results = []
        total_length = len(data)
        with alive_bar(total_length, manual=True, title="解析数据") as bar:
            for index in range(total_length):

                root = CharacterExcel.GetRootAs(data[index][3])
                meta = {
                    "id": root.Id(),
                    "dev_name": root.DevName(),
                    "costume_group_id": root.CostumeGroupId(),
                    "is_playable": root.IsPlayable(),
                    "production_step": root.ProductionStep(),
                    "collection_visible": root.CollectionVisible(),
                    "release_date": root.ReleaseDate(),
                    "collection_visible_start_date": root.CollectionVisibleStartDate(),
                    "collection_visible_end_date": root.CollectionVisibleEndDate(),
                    "is_playable_character": root.IsPlayableCharacter(),
                    "localize_etc_id": root.LocalizeEtcId(),
                    "rarity": Rarity(root.Rarity()).name,
                    "is_npc": root.IsNpc(),
                    "tactic_entity_type": TacticEntityType(root.TacticEntityType()).name,
                    "can_survive": root.CanSurvive(),
                    "is_dummy": root.IsDummy(),
                    "sub_parts_count": root.SubPartsCount(),
                    "tactic_role": TacticRole(root.TacticRole()).name,
                    "weapon_type": WeaponType(root.WeaponType()).name,
                    "tactic_range": TacticRange(root.TacticRange()).name,
                    "bullet_type": BulletType(root.BulletType()).name,
                    "armor_type": ArmorType(root.ArmorType()).name,
                    "aim_ik_type": AimIKType(root.AimIkType()).name,
                    "school": School(root.School()).name,
                    "club": Club(root.Club()).name,
                    "default_star_grade": root.DefaultStarGrade(),
                    "max_star_grade": root.MaxStarGrade(),
                    "stat_level_up_type": StatLevelUpType(root.StatLevelUpType()).name,
                    "squad_type": SquadType(root.SquadType()).name,
                    "jumpable": root.Jumpable(),
                    "personality_id": root.PersonalityId(),
                    "character_ai_id": root.CharacterAiId(),
                    "external_bt_id": root.ExternalBtId(),
                    "main_combat_style_id": root.MainCombatStyleId(),
                    "combat_style_index": root.CombatStyleIndex(),
                    "scenario_character": root.ScenarioCharacter(),
                    "spawn_template_id": root.SpawnTemplateId(),
                    "favor_levelup_type": root.FavorLevelupType(),
                    "equipment_slot": [
                        EquipmentCategory(root.EquipmentSlot(i)).name
                        for i in range(root.EquipmentSlotLength())
                    ],
                    "weapon_localize_id": root.WeaponLocalizeId(),
                    "display_enemy_info": root.DisplayEnemyInfo(),
                    "body_radius": root.BodyRadius(),
                    "random_effect_radius": root.RandomEffectRadius(),
                    "hp_bar_hide": root.HpBarHide(),
                    "hp_bar_height": root.HpBarHeight(),
                    "highlight_floater_height": root.HighlightFloaterHeight(),
                    "emoji_offset_x": root.EmojiOffsetX(),
                    "emoji_offset_y": root.EmojiOffsetY(),
                    "move_start_frame": root.MoveStartFrame(),
                    "move_end_frame": root.MoveEndFrame(),
                    "jump_motion_frame": root.JumpMotionFrame(),
                    "appear_frame": root.AppearFrame(),
                    "can_move": root.CanMove(),
                    "can_fix": root.CanFix(),
                    "can_crowd_control": root.CanCrowdControl(),
                    "can_battle_item_move": root.CanBattleItemMove(),
                    "ignore_obstacle": root.IgnoreObstacle(),
                    "is_air_unit": root.IsAirUnit(),
                    "air_unit_height": root.AirUnitHeight(),
                    "tags": [Tag(root.Tags(i)).name for i in range(root.TagsLength())],
                    "secret_stone_item_id": root.SecretStoneItemId(),
                    "secret_stone_item_amount": root.SecretStoneItemAmount(),
                    "character_piece_item_id": root.CharacterPieceItemId(),
                    "character_piece_item_amount": root.CharacterPieceItemAmount(),
                    "combine_recipe_id": root.CombineRecipeId(),
                }
                bar((index + 1) / total_length)
                results.append(meta)

        return results
