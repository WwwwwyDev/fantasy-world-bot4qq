class User:
    def __init__(self, _id : str, name: str, level: int, bag: list, coin: int) -> None:
        self._id = _id
        self.name = name
        self.level = int(level)
        self.bag = list(bag)
        self.bag_set = set(self.bag)
        self.coin = int(coin)

    def get_mongo_dict(self) -> dict:
        return {"_id": self._id, "name": self.name, "level": self.level, "bag": self.bag, "coin": self.coin}

