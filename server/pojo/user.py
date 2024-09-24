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
        self.coin_add_cnt = int(mongo_dict["coin_add_cnt"])
        self.head_equip = mongo_dict["head_equip"]
        self.body_equip = mongo_dict["body_equip"]
        self.pants_equip = mongo_dict["pants_equip"]
        self.foot_equip = mongo_dict["foot_equip"]
        self.weapon_equip = mongo_dict["weapon_equip"]
        self.talisman_equip = mongo_dict["talisman_equip"]
        self.head_level = mongo_dict["head_level"]
        self.body_level = mongo_dict["body_level"]
        self.pants_level = mongo_dict["pants_level"]
        self.foot_level = mongo_dict["foot_level"]
        self.weapon_level = mongo_dict["weapon_level"]
        self.talisman_level = mongo_dict["talisman_level"]
        self.skill = mongo_dict["skill"]
        self.bag: dict = mongo_dict["bag"]
        self.last_tower_balance = int(mongo_dict["last_tower_balance"])
        self.last_bank_balance = int(mongo_dict["last_bank_balance"])
        self.bank_coin = int(mongo_dict["bank_coin"])
        self.bank_level = int(mongo_dict["bank_level"])
        self.mongo_dict = mongo_dict

    def get_id(self):
        return self._id


