class User:

    def __init__(self, mongo_dict) -> None:
        self._id = mongo_dict["_id"]
        self.name = mongo_dict["name"]
        self.exp = int(mongo_dict["exp"])
        self.level = int(mongo_dict["level"])
        self.coin = int(mongo_dict["coin"])
        self.tower_level = int(mongo_dict["tower_level"])
        self.blood = mongo_dict["blood"]
        self.mana = int(mongo_dict["mana"])
        self.exp_add_cnt = int(mongo_dict["exp_add_cnt"])
        self.head_equip = mongo_dict["head_equip"]
        self.body_equip = mongo_dict["body_equip"]
        self.foot_equip = mongo_dict["foot_equip"]
        self.weapon_equip = mongo_dict["weapon_equip"]
        self.talisman_equip = mongo_dict["talisman_equip"]
        self.skill = mongo_dict["skill"]
        self.bag: dict = mongo_dict["bag"]
        self.last_balance = int(mongo_dict["last_balance"])

    def get_id(self):
        return self._id


