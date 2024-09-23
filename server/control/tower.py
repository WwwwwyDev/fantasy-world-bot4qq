import time
import random

from server.control import util
from server.default_params import Tower
from server.pojo.attack import TowerMonsterCombatPojo, UserCombatPojo
from server.pojo.user import User
from server.service.combat import CombatService
from server.service.item import ItemService
from server.service.user import UserService
from server.util import gen_ico, head, separate, filter_num, make_decision_list


def tower_info(params: list, user: User) -> str:
    ico_res = gen_ico(user.tower_level)
    monster_name = Tower.monster_name[(user.tower_level - 1) % Tower.tower_max]
    current_tower_level = user.tower_level
    return head(f"幻塔第{filter_num(user.tower_level)}层信息") + f"""[小怪] {monster_name}{ico_res}
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
    cnt = hook_time // 420
    if user.tower_level >= 100:
        cnt = hook_time // 360
    elif user.tower_level >= 1000:
        cnt = hook_time // 300
    elif user.tower_level >= 10000:
        cnt = hook_time // 240
    items = make_decision_list(Tower.monster_dropping, Tower.monster_dropping_p, cnt)
    item_get_mp = {}
    for i, item_id in enumerate(items):
        if item_id:
            if item_id in user.bag:
                user.bag[item_id] += 1
            else:
                user.bag[item_id] = 1
            if item_id in item_get_mp:
                item_get_mp[item_id] += 1
            else:
                item_get_mp[item_id] = 1
    get_content = ""
    for item_id, cnt in item_get_mp.items():
        get_content += f"{ItemService.get_item_by_id(item_id).name}:{cnt}个 "
    UserService.update_user(user.get_id(),
                            {"$inc": {"exp": exp_num, "coin": coin}, "$set": {"last_balance": current_time, "bag":user.bag}})
    return head(f"结算信息") + f"""[挂机时长] {filter_num(hook_time)}秒
[获得经验] {filter_num(exp_num)}点
[获得金币] {filter_num(coin)}个
[获得物品] {get_content if get_content else '空空如也'}
[挂机报告] 斩杀了{filter_num(normal_total_num)}个{monster_name}，{filter_num(advanced_total_num)}个{monster_name}(变异)"""


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
    cnt = 1
    if user.tower_level >= 100:
        cnt = 2
    elif user.tower_level >= 1000:
        cnt = 3
    elif user.tower_level >= 10000:
        cnt = 5
    items = make_decision_list(Tower.monster_dropping, Tower.monster_dropping_p, cnt)
    item_get_mp = {}
    for i, item_id in enumerate(items):
        if item_id:
            if item_id in user.bag:
                user.bag[item_id] += 1
            else:
                user.bag[item_id] = 1
            if item_id in item_get_mp:
                item_get_mp[item_id] += 1
            else:
                item_get_mp[item_id] = 1
    get_content = ""
    for item_id, cnt in item_get_mp.items():
        get_content += f"{ItemService.get_item_by_id(item_id).name}:{cnt}个 "
    UserService.update_user(user.get_id(), {"$set":{"bag":user.bag},"$inc": {"exp": exp_num, "coin": coin}})
    return head(f"扫荡结果") + f"""[获得经验] {filter_num(exp_num)}点
[获得金币] {filter_num(coin)}个
[获得物品] {get_content if get_content else '空空如也'}
[扫荡报告] 斩杀了{filter_num(normal_total_num)}个{monster_name}，{filter_num(advanced_total_num)}个{monster_name}(变异)"""


def tower_attack(params: list, user: User) -> str:
    if user.blood <= 0:
        return "血量为0,无法挑战"
    tmcp = TowerMonsterCombatPojo(user.tower_level)
    ucp = util.get_user_attack_pojo(user)
    is_win, res_content, attack_result = CombatService.attack(ucp, tmcp, user.get_id())
    add_content = ""
    if is_win:
        UserService.update_user(user.get_id(), {"$inc": {"tower_level": 1}})
        add_content = f"成功进入第{filter_num(user.tower_level+1)}层"
    UserService.update_user(user.get_id(), {"$set": {"blood": max(ucp.current_blood, 0), "mana": max(ucp.current_mana, 0)}})
    return head("战斗报告") + res_content + separate("战斗结果") + attack_result + add_content

if __name__ == '__main__':
    print(make_decision_list(Tower.monster_dropping, Tower.monster_dropping_p, 0))