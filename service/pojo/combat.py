from service.base_params import StatusBase
from service.pojo.user import UserStatus
class CombatPojo:

    def __init__(self):
        self.current_blood = 0
        self.blood_max = 0
        self.current_mana = 0
        self.mana_max = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.critical_strike = 0
        self.critical_damage = 0
        self.exp_add = 0

class TowerMonsterCombatPojo(CombatPojo):

    def __init__(self, tower_level: int):
        super().__init__()
        self.current_blood = int(tower_level * StatusBase.blood_base * 2.5)
        self.blood_max = self.current_blood
        self.current_mana = int(tower_level * StatusBase.mono_base * 2.5)
        self.mana_max = self.current_mana
        self.attack = int(StatusBase.attack_base * tower_level * 2.2)
        self.defense = int(StatusBase.defense_base * tower_level * 2.2)
        self.speed = StatusBase.speed_base + tower_level // 1000
        self.critical_strike = min(StatusBase.critical_strike_base + tower_level / 15000, 1)
        self.critical_damage = StatusBase.critical_damage_base + tower_level / 10000
        self.exp_add = -1


class UserCombatPojo(CombatPojo):

    def __init__(self, user_level: int, user_status: UserStatus):
        super().__init__()
        self.current_blood = user_status.blood
        self.blood_max = StatusBase.blood_base * user_level
        self.current_mana = user_status.mana
        self.mana_max = StatusBase.mono_base * user_level
        self.attack = StatusBase.attack_base * user_level
        self.defense = StatusBase.defense_base * user_level
        self.speed = StatusBase.speed_base
        self.critical_strike = StatusBase.critical_strike_base
        self.critical_damage = StatusBase.critical_damage_base
        self.exp_add = StatusBase.exp_add_base

def get_attribute_content(attribute :CombatPojo):
    base = f"""[血量] {attribute.current_blood} / {attribute.blood_max}
[魔力] {attribute.current_mana} / {attribute.mana_max}
[攻击] {attribute.attack}
[防御] {attribute.defense}
[速度] {attribute.speed}
[暴击率] {attribute.critical_strike * 100:.1f}%
[暴击伤害] {attribute.critical_damage * 100:.1f}%
"""
    if attribute.exp_add != -1:
        base = base + f"[经验加成] {attribute.exp_add * 100}%"
    return base


