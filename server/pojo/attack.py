from server.base_params import StatusBase
from server.default_params import Tower


class Attribute:
    def __init__(self, blood_max=0, mana_max=0, attack=0, defense=0, speed=0, critical_strike=0, critical_damage=0):
        self.blood_max = blood_max
        self.mana_max = mana_max
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.critical_strike = critical_strike
        self.critical_damage = critical_damage


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
        self.skill_callback = None


class TowerMonsterCombatPojo(CombatPojo):

    def __init__(self, tower_level: int):
        super().__init__()
        self.name = Tower.monster_name[(tower_level - 1) % Tower.tower_max]
        self.current_blood = int(tower_level * StatusBase.blood_base * 1.5)
        self.blood_max = self.current_blood
        self.current_mana = int(tower_level * StatusBase.mana_base * 1.5)
        self.mana_max = self.current_mana
        self.attack = int(StatusBase.attack_base * tower_level * 1.2)
        self.defense = int(StatusBase.defense_base * tower_level * 1.2)
        self.speed = StatusBase.speed_base + tower_level // 1000
        self.critical_strike = min(StatusBase.critical_strike_base + tower_level / 15000, 1)
        self.critical_damage = StatusBase.critical_damage_base + tower_level / 10000


class UserCombatPojo(CombatPojo):

    def __init__(self, user_name: str, user_level: int, current_blood: int, current_mana: int, add_attribute: Attribute,
                 skill_callback: callable = None):
        super().__init__()
        self.name = user_name
        self.blood_max = StatusBase.blood_base * user_level + add_attribute.blood_max
        if current_blood > self.blood_max:
            self.current_blood = self.blood_max
        else:
            self.current_blood = current_blood
        self.mana_max = StatusBase.mana_base * user_level + add_attribute.mana_max
        if current_mana > self.mana_max:
            self.current_mana = self.mana_max
        else:
            self.current_mana = current_mana
        self.attack = StatusBase.attack_base * user_level + add_attribute.attack
        self.defense = StatusBase.defense_base * user_level + add_attribute.defense
        self.speed = StatusBase.speed_base + add_attribute.speed
        self.critical_strike = min(StatusBase.critical_strike_base + add_attribute.critical_strike, 1)
        self.critical_damage = StatusBase.critical_damage_base + add_attribute.critical_damage
        self.skill_callback = skill_callback
