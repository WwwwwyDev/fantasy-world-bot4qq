class Item:
    def __init__(self, _id: str, name: str, description: str, price: int, is_on_store: bool):
        self.id = _id
        if _id.startswith("SP"):
            self.type = "特殊"
        elif _id.startswith("EQ"):
            self.type = "装备"
        elif _id.startswith("SK"):
            self.type = "技能"
        else:
            self.type = "消耗品"
        self.name = name
        self.description = description
        self.price = price
        self.out_price = price * 0.6
        self.is_on_store = is_on_store

class ItemSpecial(Item):
    def __init__(self, _id: str, name: str, description: str, price: int, is_on_store: bool, after_use: callable):
        super().__init__(_id, name, description, price, is_on_store)
        self.after_use = after_use

class ItemNormal(Item):
    def __init__(self, _id: str, name: str, description: str, price: int, is_on_store: bool, after_use: callable):
        super().__init__(_id, name, description, price, is_on_store)
        self.after_use = after_use


class ItemSkill(Item):
    def __init__(self, _id: str, name: str, description: str, price: int, is_on_store: bool, need_mono: int = 0, need_blood: int = 0, probability = 0, attack_add_pct = 0):
        super().__init__(_id, name, description, price, is_on_store)
        self.need_mono = need_mono
        self.need_blood = need_blood
        self.probability = probability
        self.attack_add_pct = attack_add_pct

class StatusAdd:

    def __init__(self, blood_max = 0, mono_max = 0, attack = 0, defense = 0, critical_strike = 0, critical_damage = 0, speed = 0, exp = 0):
        """
        :param blood_max: 最大血量加成
        :param mono_max: 最大魔法值加成
        :param attack: 攻击加成
        :param defense: 防御加成
        :param critical_strike: 暴击率加成
        :param critical_damage: 暴击伤害加成
        :param speed: 速度加成
        :param exp: 经验加成
        """
        self.blood_max = blood_max
        self.mono_max = mono_max
        self.attack = attack
        self.defense = defense
        self.critical_strike = critical_strike
        self.critical_damage = critical_damage
        self.speed = speed
        self.exp = exp

class ItemEquip(Item):
    def __init__(self, _id: str, name: str, description: str, price: int, is_on_store: bool, position: int,add_status: StatusAdd):
        super().__init__(_id, name, description, price, is_on_store)
        self.position = position
        self.add_status  = add_status


