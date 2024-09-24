import math
import time
import random

from server.control import util
from server.default_params import Tower
from server.pojo.attack import TowerMonsterCombatPojo
from server.pojo.item import Item
from server.pojo.user import User
from server.service.combat import CombatService
from server.service.item import ItemService
from server.service.user import UserService
from server.util import gen_ico, head, separate, filter_num, make_decision_list


def tower_info(params: list, user: User) -> str:
    current_tower_level = user.tower_level
    combat_tower_pojo = TowerMonsterCombatPojo(current_tower_level)
    return head(f"幻塔第{filter_num(user.tower_level)}层信息") + f"""[小怪] {combat_tower_pojo.name}
[精英怪] 变异的{combat_tower_pojo.name}
[首领] {combat_tower_pojo.name}王""" + separate(f"首领属性") + CombatService.get_attribute_content(
        combat_tower_pojo) + f"\n[战斗力] {filter_num(CombatService.get_combat_score(combat_tower_pojo))}"


def tower_balance(params: list, user: User) -> str:
    current_time = int(time.time())
    hook_time = current_time - user.last_tower_balance
    if hook_time <= 60:
        return "距离上一次结算少于1分钟"
    monster_name = Tower.monster_name[(user.tower_level - 1) % Tower.tower_max] + gen_ico(user.tower_level)
    m = hook_time // 60
    normal_total_num = m * random.uniform(0.9, 1.1)
    advanced_total_num = m * random.uniform(0.2, 0.4)
    exp_add = user.exp_add_cnt * 0.01
    coin_add = user.coin_add_cnt * 0.01
    exp_num = int((normal_total_num * user.tower_level + advanced_total_num * user.tower_level * 3) * (1 + exp_add))
    coin = int(((advanced_total_num + normal_total_num) * user.tower_level) * (1 + coin_add))
    total_cnt = (m // 5) * math.ceil(user.tower_level / 1000)
    tower_monster_dropping, tower_monster_dropping_p = ItemService.get_tower_monster_dropping_items_list()
    equip_dropping, equip_dropping_p = ItemService.get_tower_boss_dropping_items_list()
    normal_items: list[Item] = make_decision_list(tower_monster_dropping, tower_monster_dropping_p, total_cnt)
    equip_items: list[Item] = make_decision_list(equip_dropping, equip_dropping_p, total_cnt // 2)
    items = [*normal_items, *equip_items]
    item_get_mp = {}
    for item in items:
        if item:
            if item.id in user.bag:
                user.bag[item.id] += 1
            else:
                user.bag[item.id] = 1
            if item in item_get_mp:
                item_get_mp[item] += 1
            else:
                item_get_mp[item] = 1
    get_content = ""
    for item, cnt in item_get_mp.items():
        get_content += f"{item.name}:{cnt}个 "
    UserService.update_user(user.get_id(),
                            {"$inc": {"exp": exp_num, "coin": coin},
                             "$set": {"last_tower_balance": current_time, "bag": user.bag}})
    return head(f"结算信息") + f"""[挂机时长] {filter_num(hook_time)}秒
[获得经验] {filter_num(exp_num)}点
[获得金币] {filter_num(coin)}个
[获得物品] {get_content if get_content else '空空如也'}
[挂机报告] 斩杀了{filter_num(round(normal_total_num))}个{monster_name}，{filter_num(round(advanced_total_num))}个{monster_name}(变异)"""


def tower_wipe(params: list, user: User) -> str:
    return "开始扫荡|30|tower_wipe"


def tower_wipe_delay(user: User) -> str:
    m = 5
    monster_name = Tower.monster_name[(user.tower_level - 1) % Tower.tower_max] + gen_ico(user.tower_level)
    normal_total_num = m * random.uniform(0.9, 1.1)
    advanced_total_num = m * random.uniform(0.1, 0.45)
    exp_add = user.exp_add_cnt * 0.01
    coin_add = user.coin_add_cnt * 0.01
    exp_num = int((normal_total_num * user.tower_level + advanced_total_num * user.tower_level * 3) * (1 + exp_add))
    coin = int(((advanced_total_num + normal_total_num) * user.tower_level) * (1 + coin_add))
    total_cnt = 2 + math.ceil(user.tower_level / 1000)
    tower_monster_dropping, tower_monster_dropping_p = ItemService.get_tower_monster_dropping_items_list()
    equip_dropping, equip_dropping_p = ItemService.get_tower_boss_dropping_items_list()
    normal_items: list[Item] = make_decision_list(tower_monster_dropping, tower_monster_dropping_p, total_cnt)
    equip_items: list[Item] = make_decision_list(equip_dropping, equip_dropping_p, total_cnt // 2)
    items = [*normal_items, *equip_items]
    item_get_mp = {}
    for item in items:
        if item:
            if item.id in user.bag:
                user.bag[item.id] += 1
            else:
                user.bag[item.id] = 1
            if item in item_get_mp:
                item_get_mp[item] += 1
            else:
                item_get_mp[item] = 1
    get_content = ""
    for item, cnt in item_get_mp.items():
        get_content += f"{item.name}:{cnt}个 "
    UserService.update_user(user.get_id(), {"$set": {"bag": user.bag}, "$inc": {"exp": exp_num, "coin": coin}})
    return head(f"扫荡结果") + f"""[获得经验] {filter_num(exp_num)}点
[获得金币] {filter_num(coin)}个
[获得物品] {get_content if get_content else '空空如也'}
[扫荡报告] 斩杀了{round(normal_total_num)}个{monster_name}，{round(advanced_total_num)}个{monster_name}(变异)"""


def tower_attack(params: list, user: User) -> str:
    if user.blood <= 0:
        return "血量为0，无法挑战"
    tmcp = TowerMonsterCombatPojo(user.tower_level)
    ucp = util.get_user_attack_pojo(user)
    is_win, res_content, attack_result, total = CombatService.attack(ucp, tmcp, user.get_id())
    add_content = ""
    get_exp_cnt = 0
    get_coin_cnt = 0
    if is_win:
        tower_boss_dropping, tower_boss_dropping_p = ItemService.get_tower_boss_dropping_items_list()
        items: list[Item] = make_decision_list(tower_boss_dropping, tower_boss_dropping_p,
                                               max(user.tower_level // 100, 1))
        item_get_mp = {}
        for item in items:
            if item:
                if item.id in user.bag:
                    user.bag[item.id] += 1
                else:
                    user.bag[item.id] = 1
                if item in item_get_mp:
                    item_get_mp[item] += 1
                else:
                    item_get_mp[item] = 1
        get_content = ""
        for item, cnt in item_get_mp.items():
            get_content += f"{item.name}:{cnt}个 "
        get_exp_cnt = int(200 * user.tower_level * (1 + user.exp_add_cnt / 100))
        get_coin_cnt = int(150 * user.tower_level * (1 + user.coin_add_cnt / 100))
        add_content = f"成功进入第{filter_num(user.tower_level + 1)}层\n[获得经验] {get_exp_cnt}\n[获得金币] {get_coin_cnt}\n[获得物品] {get_content if get_content else '空空如也'}"
    if is_win:
        UserService.update_user(user.get_id(), {
            "$set": {"bag": user.bag, "blood": max(ucp.current_blood, 0), "mana": max(ucp.current_mana, 0)},
            "$inc": {"tower_level": 1, "exp": get_exp_cnt, "coin": get_coin_cnt}})
    else:
        UserService.update_user(user.get_id(),
                                {"$set": {"blood": max(ucp.current_blood, 0), "mana": max(ucp.current_mana, 0)}})
    return head("战斗报告") + res_content + separate("战斗结果") + attack_result + add_content
