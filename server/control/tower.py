import time
import random

from server.control import util
from server.default_params import Tower
from server.pojo.attack import TowerMonsterCombatPojo, UserCombatPojo
from server.pojo.user import User
from server.service.combat import CombatService
from server.service.user import UserService
from server.util import gen_ico, head, separate


def tower_info(params: list, user: User) -> str:
    ico_res = gen_ico(user.tower_level)
    monster_name = Tower.monster_name[(user.tower_level - 1) % Tower.tower_max]
    current_tower_level = user.tower_level
    return head(f"幻塔第{user.tower_level}层信息") + f"""[小怪] {monster_name}{ico_res}
[精英怪] {monster_name}{ico_res}(变异)
[首领] {monster_name}王{ico_res}""" + separate(f"首领属性") + CombatService.get_attribute_content(
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
    exp_add = user.exp_add_cnt * 0.01
    exp_num = int((normal_total_num * user.tower_level + advanced_total_num * user.tower_level * 3) * (1 + exp_add))
    coin = (advanced_total_num + normal_total_num) * user.tower_level
    UserService.update_user(user.get_id(),
                            {"$inc": {"exp": exp_num, "coin": coin}, "$set": {"last_balance": current_time}})
    return head(f"结算信息") + f"""[挂机时长] {hook_time}秒
[获得经验] {exp_num}点
[获得金币] {coin}个
[挂机报告] 斩杀了{normal_total_num}个{monster_name}，{advanced_total_num}个{monster_name}(变异)"""


def tower_wipe(params: list, user: User) -> str:
    return "开始扫荡|30|tower_wipe"


def tower_wipe_delay(user: User) -> str:
    m = 5
    monster_name = Tower.monster_name[(user.tower_level - 1) % Tower.tower_max] + gen_ico(user.tower_level)
    normal_total_num = int(m * random.uniform(0.9, 1.1))
    advanced_total_num = int(m * random.uniform(0.1, 0.45))
    exp_add = user.exp_add_cnt * 0.01
    exp_num = int((normal_total_num * user.tower_level + advanced_total_num * user.tower_level * 3) * (1 + exp_add))
    coin = (advanced_total_num + normal_total_num) * user.tower_level
    UserService.update_user(user.get_id(), {"$inc": {"exp": exp_num, "coin": coin}})
    return head(f"扫荡结果") + f"""[获得经验] {exp_num}点
[获得金币] {coin}个
[扫荡报告] 斩杀了{normal_total_num}个{monster_name}，{advanced_total_num}个{monster_name}(变异)"""


def tower_attack(params: list, user: User) -> str:
    if user.blood <= 0:
        return "血量为0,无法挑战"
    tmcp = TowerMonsterCombatPojo(user.tower_level)
    ucp = util.get_user_attack_pojo(user)
    is_win, res_content, attack_result = CombatService.attack(ucp, tmcp, user.get_id())
    add_content = ""
    if is_win:
        UserService.update_user(user.get_id(), {"$inc": {"tower_level": 1}})
        add_content = "成功进入下一层"
    UserService.update_user(user.get_id(), {"$set": {"blood": ucp.current_blood, "mana": ucp.current_mana}})
    return head("战斗报告") + res_content + separate("战斗结果") + attack_result + add_content
