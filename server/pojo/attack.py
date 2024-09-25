from server.base_params import StatusBase
from server.default_params import Tower
from server.util import gen_ico


class Attribute:
    def __init__(self, blood_max=0, mana_max=0, attack=0, defense=0, speed=0, critical_strike=0, critical_damage=0,
                 defense_strike=0, hurt_percentage_add=0, attack_percentage_add=0, defense_percentage_add=0, blood_max_percentage_add=0, mana_max_percentage_add=0):
        self.blood_max = blood_max
        self.mana_max = mana_max
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.critical_strike = critical_strike
        self.critical_damage = critical_damage
        self.defense_strike = defense_strike
        self.hurt_percentage_add = hurt_percentage_add
        self.defense_percentage_add = defense_percentage_add
        self.attack_percentage_add = attack_percentage_add
        self.attack_percentage_add = attack_percentage_add
        self.blood_max_percentage_add = blood_max_percentage_add
        self.mana_max_percentage_add = mana_max_percentage_add


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
        self.defense_strike = 0
        self.hurt_percentage_add = 0
        self.skill_callback = None


class TowerMonsterCombatPojo(CombatPojo):

    def __init__(self, tower_level: int):
        super().__init__()
        self.name = Tower.monster_name[(tower_level - 1) % Tower.tower_max] + gen_ico(tower_level)
        self.current_blood = int(tower_level * StatusBase.blood_base * 1.3)
        self.blood_max = self.current_blood
        self.current_mana = int(tower_level * StatusBase.mana_base * 1.3)
        self.mana_max = self.current_mana
        self.attack = int(StatusBase.attack_base * tower_level * 1.2)
        self.defense = int(StatusBase.defense_base * tower_level)
        self.speed = StatusBase.speed_base + tower_level // 500
        self.critical_strike = min(StatusBase.critical_strike_base + tower_level / 1500, 1.5)
        self.critical_damage = StatusBase.critical_damage_base + tower_level / 1000
        self.defense_strike = min(StatusBase.critical_strike_base + tower_level / 2500, 1)
        if tower_level >= 10000:
            self.hurt_percentage_add = 0.5
        else:
            self.hurt_percentage_add = 0


class SeaMonsterCombatPojo(CombatPojo):

    def __init__(self, name: str, speed):
        super().__init__()
        self.name = name
        self.current_blood = 100000000000000000
        self.blood_max = self.current_blood
        self.current_mana = 100000000000000000
        self.mana_max = self.current_mana
        self.attack = 100000000000000000
        self.defense = 0
        self.speed = speed
        self.critical_strike = 0
        self.critical_damage = 0
        self.defense_strike = 0
        self.hurt_percentage_add = 0

class UserCombatPojo(CombatPojo):

    def __init__(self, user_name: str, user_level: int, current_blood: int, current_mana: int, add_attribute: Attribute,
                 skill_callback: callable = None):
        super().__init__()
        self.name = user_name
        self.blood_max = int((StatusBase.blood_base * user_level + add_attribute.blood_max) * (1 + add_attribute.blood_max_percentage_add))
        if current_blood > self.blood_max:
            self.current_blood = self.blood_max
        else:
            self.current_blood = current_blood
        if self.current_blood < 0:
            self.current_blood = 0
        self.mana_max = int((StatusBase.mana_base * user_level + add_attribute.mana_max) * (1 + add_attribute.mana_max_percentage_add))
        if current_mana > self.mana_max:
            self.current_mana = self.mana_max
        else:
            self.current_mana = current_mana
        if self.current_mana < 0:
            self.current_mana = 0
        self.attack = (StatusBase.attack_base * user_level + add_attribute.attack) * (
                    1 + add_attribute.attack_percentage_add)
        self.defense = (StatusBase.defense_base * user_level + add_attribute.defense) * (
                    1 + add_attribute.defense_percentage_add)
        self.speed = StatusBase.speed_base + add_attribute.speed
        self.critical_strike = StatusBase.critical_strike_base + add_attribute.critical_strike
        self.critical_damage = StatusBase.critical_damage_base + add_attribute.critical_damage
        self.defense_strike = add_attribute.defense_strike
        self.hurt_percentage_add = add_attribute.hurt_percentage_add
        self.skill_callback = skill_callback
