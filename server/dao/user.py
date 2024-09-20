from gv import Global
from server.error import LFError
from server.default_params import get_default_user
from server.pojo.user import User


class UserDao:


    @staticmethod
    def get_user_by_id(_id: str) -> User | None:
        mongo_dict = Global.user_c.find_one({"_id": _id})
        if not mongo_dict:
            return None
        return User(mongo_dict)

    @staticmethod
    def get_user_by_name(name: str) -> User | None:
        mongo_dict = Global.user_c.find_one({"name": name})
        if not mongo_dict:
            return None
        return User(mongo_dict)

    @staticmethod
    def get_user_by_id_with_up(_id: str) -> User | None:
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
    def get_user_by_name_with_up(name: str) -> User | None:
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

    @staticmethod
    def insert_user_one(self, mongo_dict: dict) -> None:
        result = Global.user_c.insert_one(mongo_dict)
        if not result:
            raise LFError("[error] 数据库更新失败")


