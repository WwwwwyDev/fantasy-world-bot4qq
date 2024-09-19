from service.util import RandomUtil
from gv import Global
from service.error import LFError
from service.default_params import get_default_user


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
        self.last_balance = int(mongo_dict["last_balance"])

    def get_id(self):
        return self._id


class UserDao:

    @staticmethod
    def register(_id: str) -> str:
        user_new_name = RandomUtil.random_name_str()
        cnt = 10
        while Global.user_c.find_one(filter={"name": user_new_name}) and cnt:
            user_new_name = RandomUtil.random_name_str()
            cnt -= 1
        if not Global.user_c.find_one(filter={"name": user_new_name}):
            Global.user_c.insert_one(get_default_user(_id, user_new_name))
            return user_new_name
        else:
            raise LFError("[error] 尝试多次未随机到非重复姓名")

    @staticmethod
    def get_user_by_id(_id: str) -> User | None:
        mongo_dict = Global.user_c.find_one({"_id": _id})
        if not mongo_dict:
            return None
        template_dict = get_default_user(_id, mongo_dict["name"])
        filter_dict = {}
        if len(mongo_dict) != len(template_dict):
            filter_dict = {k: v for k, v in template_dict.items() if k not in mongo_dict}
            UserDao.update_user(_id, {"$set": filter_dict})
        mongo_dict.update(filter_dict)
        return User(mongo_dict)

    @staticmethod
    def get_user_by_name(name: str) -> User | None:
        mongo_dict = Global.user_c.find_one({"name": name})
        if not mongo_dict:
            return None
        _id = mongo_dict["_id"]
        template_dict = get_default_user(_id, mongo_dict["name"])
        filter_dict = {}
        if len(mongo_dict) != len(template_dict):
            filter_dict = {k: v for k, v in template_dict.items() if k not in mongo_dict}
            UserDao.update_user(_id, {"$set": filter_dict})
        mongo_dict.update(filter_dict)
        return User(mongo_dict)

    @staticmethod
    def update_user(_id: str, update: dict) -> None:
        result = Global.user_c.update_one(filter={"_id": _id}, update=update)
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")

