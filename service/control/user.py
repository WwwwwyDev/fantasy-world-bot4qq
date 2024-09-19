from service.pojo.user import User, UserDao
from service.pojo.combat import UserCombatPojo, get_attribute_content, attack, CombatDao
from service.base_params import max_exp_base
from service.util import head, separate


def user_info(params: list, user: User) -> str:
    return head("我的信息") + f"""[昵称] {user.name}
[等级] {user.level}
[经验] {user.exp} / {user.level * max_exp_base}
[金币] {user.coin}
[幻塔层数] 第{user.tower_level}层"""


def user_id(params: list, user: User) -> str:
    return user.get_id()


def user_attribute(params: list, user: User) -> str:
    attribute = UserCombatPojo(user)
    return head("我的属性") + get_attribute_content(attribute)


def user_update(params: list, user: User) -> (str, bool):
    need_exp = user.level * max_exp_base
    if user.exp < need_exp:
        return f"升级失败，还需{need_exp - user.exp}点经验才能升级"
    UserDao.update_user(user.get_id(), {"$inc": {"exp": -need_exp, "level": 1}})
    return f"升级成功, {user.level}级->{user.level + 1}级"


def user_attack(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误"
    user_name = params[0]
    if user.name == user_name:
        return "无法与自己切磋"
    another_user = UserDao.get_user_by_name(user_name)
    if not another_user:
        return f"冒险者\"{user_name}\"不存在"
    me = UserCombatPojo(user)
    me.current_blood = me.blood_max
    me.current_mana = me.mana_max
    another = UserCombatPojo(another_user)
    _, res_content, attack_result = attack(me, another, user.get_id())
    return head("战斗报告") + res_content + separate("战斗结果") + attack_result


def last_attack_record(params: list, user: User) -> str:
    if len(params) < 1:
        page = 1
    else:
        try:
            page = int(params[0])
        except:
            return "指令错误"
        if page <= 0:
            return "指令错误"
    combat_record = CombatDao.get_combat_record(user.get_id())
    if not combat_record:
        return "近期没有战斗记录"
    last_combat_record_list = combat_record["last_record"]
    if len(last_combat_record_list) < 1:
        return "近期没有战斗记录"
    offset = 6
    total = len(last_combat_record_list)//offset+1
    if page > total:
        return f"共{total}页报告，第{page}页不存在"
    res_content = ""
    for i in range((page - 1) * offset, min(page * offset, len(last_combat_record_list))):
        res_content += last_combat_record_list[i]
    return head("战斗详细报告") + res_content + separate(f"第{page}页  共{total}页")
