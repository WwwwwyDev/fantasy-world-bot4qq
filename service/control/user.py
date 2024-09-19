from service.pojo.user import User, UserDao
from service.pojo.combat import UserCombatPojo, get_attribute_content
from service.base_params import max_exp_base
from service.util import head

def user_info(params: list, user: User) -> str:
    return head("我的信息") +f"""[昵称] {user.name}
[等级] {user.level}
[经验] {user.exp} / {user.level * max_exp_base}
[金币] {user.coin}
[幻想之塔层数] 第{user.tower_level}层"""

def user_id(params: list, user: User) -> str:
    return user.get_id()

def user_attribute(params: list, user: User) -> str:
    status = UserDao.get_user_status_by_id(user.get_id())
    attribute = UserCombatPojo(user.level, status)
    return head("我的属性") + get_attribute_content(attribute)

def user_update(params: list, user: User) -> str:
    need_exp = user.level * max_exp_base
    if user.exp < need_exp:
        return f"升级失败，还需{need_exp - user.exp}点经验才能升级"
    UserDao.update_user(user.get_id(), {"$inc":{"exp": -need_exp, "level": 1}})
    return f"升级成功, {user.level-1}级->{user.level}级"
