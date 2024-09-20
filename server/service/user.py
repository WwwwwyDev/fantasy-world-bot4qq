from server.error import LFError
from server.default_params import get_default_user
from server.pojo.user import User
from server.util import RandomUtil
from server.dao.user import UserDao


class UserService:
    @staticmethod
    def register(_id: str) -> str:
        user_new_name = RandomUtil.random_name_str()
        cnt = 5
        while UserDao.get_user_by_name(user_new_name) and cnt:
            user_new_name = RandomUtil.random_name_str()
            cnt -= 1
        if not UserDao.get_user_by_name(user_new_name):
            UserDao.insert_user_one(get_default_user(_id, user_new_name))
            return user_new_name
        else:
            raise LFError("[error] 尝试多次未随机到非重复姓名")

    @staticmethod
    def change_name(_id: str) -> str:
        user_new_name = RandomUtil.random_name_str()
        cnt = 5
        while UserDao.get_user_by_name(user_new_name) and cnt:
            user_new_name = RandomUtil.random_name_str()
            cnt -= 1
        if not UserDao.get_user_by_name(user_new_name):
            UserDao.update_user(_id, {"$set":{"name": user_new_name}})
            return user_new_name
        else:
            raise LFError("[error] 尝试多次未随机到非重复姓名")

    @staticmethod
    def get_user_by_id_with_up(_id: str) -> User | None:
        return UserDao.get_user_by_id_with_up(_id)

    @staticmethod
    def get_user_by_name_with_up(name: str) -> User | None:
        return UserDao.get_user_by_name_with_up(name)

    @staticmethod
    def get_user_by_id(_id: str) -> User | None:
        return UserDao.get_user_by_id(_id)

    @staticmethod
    def get_user_by_name(name: str) -> User | None:
        return UserDao.get_user_by_name(name)

    @staticmethod
    def update_user(_id: str, update: dict) -> None:
        UserDao.update_user(_id, update)