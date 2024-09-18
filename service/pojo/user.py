from service.util import RandomUtil
from gv import Global
from service.error import LFError


class User:

    def __init__(self, mongo_dict) -> None:
        self._id = mongo_dict["_id"]
        self.name = mongo_dict["name"]
        self.exp = int(mongo_dict["exp"])
        self.level = int(mongo_dict["level"])
        self.bag = list(mongo_dict["bag"])
        self.bag_set = set(self.bag)
        self.coin = int(mongo_dict["coin"])

    def get_id(self):
        return self._id


class UserDao:

    @staticmethod
    def register(_id: str) -> str:
        user_new_name = RandomUtil.random_name_str()
        cnt = 10
        while Global.user_db.find_one(filter={"name": user_new_name}) and cnt:
            user_new_name = RandomUtil.random_name_str()
            cnt -= 1
        if not Global.user_db.find_one(filter={"name": user_new_name}):
            Global.user_db.insert_one(
                {"_id": _id, "name": user_new_name, "exp": 0, "level": 1, "bag": [], "coin": 100000})
            return user_new_name
        else:
            raise LFError("[error] 尝试多次未随机到非重复姓名")

    @staticmethod
    def get_user_by_id(_id: str) -> User | None:
        mongo_dict = Global.user_db.find_one({"_id": _id})
        if not mongo_dict:
            return None
        return User(mongo_dict)

    @staticmethod
    def update_user(_id: str, user_dict: dict) -> None:
        result = Global.user_db.update_one(filter={"_id": _id}, update={'$set': user_dict})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
