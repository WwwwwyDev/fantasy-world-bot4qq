from server.base_params import bs_rate
from server.util import filter_num

class Item:
    def __init__(self, _id: str, name: str, description: str, price: int):
        self.id = _id
        if _id.startswith("SP"):
            self.type = "特殊"
            self.type_id = 0
        elif _id.startswith("EQ"):
            self.type = "装备"
            self.type_id = 1
        elif _id.startswith("SK"):
            self.type = "技能"
            self.type_id = 2
        else:
            self.type = "消耗品"
            self.type_id = 3
        self.name = name
        self.description = description
        self.price = price
        self.out_price = int(price * 0.6)


class ItemSpecial(Item):
    def __init__(self, _id: str, name: str, description: str, price: int):
        super().__init__(_id, name, description, price)


class ItemNormal(Item):
    def __init__(self, _id: str, name: str, description: str, price: int,  after_use: callable):
        super().__init__(_id, name, description, price)
        self.after_use = after_use


class ItemSkill(Item):
    def __init__(self, _id: str, name: str, description: str, price: int, on_attack: callable):
        super().__init__(_id, name, description, price)
        self.on_attack = on_attack


class StatusAdd:

    def __init__(self, blood_max=0, mana_max=0, attack=0, defense=0, critical_strike=0, critical_damage=0, speed=0):
        """
        :param blood_max: 最大血量加成
        :param mana_max: 最大魔法值加成
        :param attack: 攻击加成
        :param defense: 防御加成
        :param critical_strike: 暴击率加成
        :param critical_damage: 暴击伤害加成
        :param speed: 速度加成
        """
        self.blood_max = blood_max
        self.mana_max = mana_max
        self.attack = attack
        self.defense = defense
        self.critical_strike = critical_strike
        self.critical_damage = critical_damage
        self.speed = speed

    def get_desc(self, bs_level: int = 0):
        content = ""
        if self.blood_max:
            content += f"最大血量加成: {filter_num(self.blood_max)}"
            if bs_level > 0:
                content += f" + {filter_num(int(bs_level * self.blood_max * bs_rate))}"
            content += "\n"
        if self.mana_max:
            content += f"最大魔力加成: {filter_num(self.mana_max)}"
            if bs_level > 0:
                content += f" + {filter_num(int(bs_level * self.mana_max * bs_rate))}"
            content += "\n"
        if self.attack:
            content += f"攻击加成: {filter_num(self.attack)}"
            if bs_level > 0:
                content += f" + {filter_num(int(bs_level * self.attack * bs_rate))}"
            content += "\n"
        if self.defense:
            content += f"防御加成: {filter_num(self.defense)}"
            if bs_level > 0:
                content += f" + {filter_num(int(bs_level * self.defense * bs_rate))}"
            content += "\n"
        if self.critical_strike:
            content += f"暴击率加成: {int(self.critical_strike * 100)}%\n"
            # if bs_level > 0:
            #     content += f" + {int(bs_level * self.critical_strike * bs_rate * 100)}%"
            # content += "\n"
        if self.critical_damage:
            content += f"暴击伤害加成: {filter_num(int(self.critical_damage * 100))}%"
            if bs_level > 0:
                content += f" + {filter_num(int(bs_level * self.critical_damage * bs_rate * 100))}%"
            content += "\n"
        if self.speed:
            content += f"速度加成: {self.speed}\n"
            # if bs_level > 0:
            #     content += f" + {int(bs_level * self.speed * bs_rate)}"
            # content += "\n"
        return content[:-1]


position_mp = ["武器", "头盔", "上装", "下装", "鞋子", "护符"]


class ItemEquip(Item):
    def __init__(self, _id: str, name: str, description: str, price: int, position: int, add_status: StatusAdd):
        super().__init__(_id, name, description, price)
        self.position = position
        self.type = position_mp[position]
        self.add_status = add_status
        self.description = description + "\n" + add_status.get_desc()
