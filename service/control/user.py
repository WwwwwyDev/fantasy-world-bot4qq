from service.pojo.user import User, UserDao
from service.share_params import level_base


def user_info(params: list, user: User) -> str:
    return f"[昵称] {user.name}\n[等级] {user.level}\n[经验] {user.exp} / {user.level * level_base}\n[幻想币] {user.coin}"


def user_update(params: list, user: User) -> str:
    need_exp = user.level * level_base
    if user.exp < need_exp:
        return f"升级失败，还需{need_exp - user.exp}点经验才能升级"
    user.level += 1
    user.exp -= need_exp
    UserDao.update_user(user.get_id(), {"exp": user.exp, "level": user.level})
    return f"升级成功, {user.level-1}级->{user.level}级"
