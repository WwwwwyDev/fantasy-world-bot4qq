from service.pojo.user import User, UserDao
from service.util import head, separate, gen_ico
from service.default_params import Tower
from service.pojo.combat import TowerMonsterCombatPojo, get_attribute_content, UserCombatPojo, attack
import time
import random


def tower_info(params: list, user: User) -> str:
    ico_res = gen_ico(user.tower_level)
    monster_name = Tower.monster_name[(user.tower_level - 1) % Tower.tower_max]
    current_tower_level = user.tower_level
    return head(f"幻塔第{user.tower_level}层信息") + f"""[小怪] {monster_name}{ico_res}
[精英怪] {monster_name}{ico_res}(变异)
[首领] {monster_name}王{ico_res}""" + separate(f"首领属性") + get_attribute_content(
        TowerMonsterCombatPojo(current_tower_level))


def tower_balance(params: list, user: User) -> str:
    current_time = int(time.time())
    hook_time = current_time - user.last_balance
    if hook_time <= 60:
        return "距离上一次结算少于1分钟"
    monster_name = Tower.monster_name[(user.tower_level - 1) % Tower.tower_max] + gen_ico(user.tower_level)
    m = hook_time // 60
    normal_total_num = int(m * random.uniform(0.9, 1.1))
    advanced_total_num = int(m * random.uniform(0.2, 0.4))
    exp_add = UserCombatPojo(user).exp_add
    exp_num = int((normal_total_num * user.tower_level + advanced_total_num * user.tower_level * 3) * (1 + exp_add))
    coin = (advanced_total_num + normal_total_num) * user.tower_level
    UserDao.update_user(user.get_id(), {"$inc": {"exp": exp_num, "coin": coin}, "$set": {"last_balance": current_time}})
    return head(f"结算信息") + f"""[挂机时长] {hook_time}秒
[获得经验] {exp_num}点
[获得金币] {coin}个
[挂机报告] 斩杀了{normal_total_num}个{monster_name}，{advanced_total_num}个{monster_name}(变异)"""


def tower_wipe(params: list, user: User) -> str:
    return "开始扫荡|30|tower_wipe"


def tower_wipe_delay(user: User) -> str:
    m = 6
    monster_name = Tower.monster_name[(user.tower_level - 1) % Tower.tower_max] + gen_ico(user.tower_level)
    normal_total_num = int(m * random.uniform(0.9, 1.1))
    advanced_total_num = int(m * random.uniform(0.1, 0.5))
    exp_add = UserCombatPojo(user).exp_add
    exp_num = int((normal_total_num * user.tower_level + advanced_total_num * user.tower_level * 3) * (1 + exp_add))
    coin = (advanced_total_num + normal_total_num) * user.tower_level
    UserDao.update_user(user.get_id(), {"$inc": {"exp": exp_num, "coin": coin}})
    return head(f"扫荡结果") + f"""[获得经验] {exp_num}点
[获得金币] {coin}个
[扫荡报告] 斩杀了{normal_total_num}个{monster_name}，{advanced_total_num}个{monster_name}(变异)"""


def tower_attack(params: list, user: User) -> str:
    tmcp = TowerMonsterCombatPojo(user.tower_level)
    ucp = UserCombatPojo(user)
    is_win, res_content, attack_result = attack(ucp, tmcp, user.get_id())
    add_content = ""
    if is_win:
        UserDao.update_user(user.get_id(), {"$inc": {"tower_level": 1}})
        add_content = "成功进入下一层"
    return head("战斗报告") + res_content + separate("战斗结果") + attack_result + add_content
