from server.base_params import StatusBase
from server.default_params import Tower
from server.pojo.user import User


class CombatPojo:

    def __init__(self):
        self.name = ""
        self.current_blood = 0
        self.blood_max = 0
        self.current_mana = 0
        self.mana_max = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.critical_strike = 0
        self.critical_damage = 0


class TowerMonsterCombatPojo(CombatPojo):

    def __init__(self, tower_level: int):
        super().__init__()
        self.name = Tower.monster_name[(tower_level - 1) % Tower.tower_max]
        self.current_blood = int(tower_level * StatusBase.blood_base * 1.5)
        self.blood_max = self.current_blood
        self.current_mana = int(tower_level * StatusBase.mono_base * 1.5)
        self.mana_max = self.current_mana
        self.attack = int(StatusBase.attack_base * tower_level * 1.2)
        self.defense = int(StatusBase.defense_base * tower_level * 1.2)
        self.speed = StatusBase.speed_base + tower_level // 1000
        self.critical_strike = min(StatusBase.critical_strike_base + tower_level / 15000, 1)
        self.critical_damage = StatusBase.critical_damage_base + tower_level / 10000


class UserCombatPojo(CombatPojo):

    def __init__(self, user: User):
        super().__init__()
        self.name = user.name
        self.current_blood = user.blood
        self.blood_max = StatusBase.blood_base * user.level
        self.current_mana = user.mana
        self.mana_max = StatusBase.mono_base * user.level
        self.attack = StatusBase.attack_base * user.level
        self.defense = StatusBase.defense_base * user.level
        self.speed = StatusBase.speed_base
        self.critical_strike = StatusBase.critical_strike_base
        self.critical_damage = StatusBase.critical_damage_base


