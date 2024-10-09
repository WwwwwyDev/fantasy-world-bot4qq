from server.base_params import max_exp_base
from server.pojo.item import ItemEquip
from server.pojo.user import User
from server.util import head, separate, filter_num, check_name
from server.service.combat import CombatService
from server.service.user import UserService
from server.service.item import ItemService
from server.control.util import equip_name_mp, equip_level_mp, get_user_attack_pojo


def user_info(params: list, user: User) -> str:
    return head("我的信息") + f"""[昵称] {user.name}
[等级] {filter_num(user.level)}
[经验] {filter_num(user.exp)} / {filter_num(user.level * max_exp_base)}
[金币💰] {filter_num(user.coin)}
[幻塔层数] 第{filter_num(user.tower_level)}层""" + separate(
        "装备与技能") + f"""[武器+{user.weapon_level}] {user.weapon_equip["name"] if user.weapon_equip["name"] else "未装备"}
[头盔+{user.head_level}] {user.head_equip["name"] if user.head_equip["name"] else "未装备"}
[上装+{user.body_level}] {user.body_equip["name"] if user.body_equip["name"] else "未装备"}
[下装+{user.pants_level}] {user.pants_equip["name"] if user.pants_equip["name"] else "未装备"}
[鞋子+{user.foot_level}] {user.foot_equip["name"] if user.foot_equip["name"] else "未装备"}
[饰品+{user.talisman_level}] {user.talisman_equip["name"] if user.talisman_equip["name"] else "未装备"}
[技能] {user.skill["name"] if user.skill["name"] else "未学习"}
"""

def see_coin(params: list, user: User) -> str:
    return f"金币💰:{filter_num(user.coin)}"

def see_other_user_info(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误，请输入冒险者名字"
    user_name = params[0]
    another_user = UserService.get_user_by_name_with_up(user_name)
    if not another_user:
        return f"冒险者\"{user_name}\"不存在"
    user = another_user
    return head("冒险者信息") + f"""[昵称] {user.name}
[等级] {filter_num(user.level)}
[幻塔层数] 第{filter_num(user.tower_level)}层""" + separate(
        "装备与技能") + f"""[武器+{user.weapon_level}] {user.weapon_equip["name"] if user.weapon_equip["name"] else "未装备"}
[头盔+{user.head_level}] {user.head_equip["name"] if user.head_equip["name"] else "未装备"}
[上装+{user.body_level}] {user.body_equip["name"] if user.body_equip["name"] else "未装备"}
[下装+{user.pants_level}] {user.pants_equip["name"] if user.pants_equip["name"] else "未装备"}
[鞋子+{user.foot_level}] {user.foot_equip["name"] if user.foot_equip["name"] else "未装备"}
[饰品+{user.talisman_level}] {user.talisman_equip["name"] if user.talisman_equip["name"] else "未装备"}
[技能] {user.skill["name"] if user.skill["name"] else "未学习"}
"""


def user_equip(params: list, user: User) -> str:
    content = head("我的装备")
    for equip_mongo_name, equip_name in equip_name_mp.items():
        name = user.mongo_dict[equip_mongo_name]["name"]
        if name:
            item_id = user.mongo_dict[equip_mongo_name]["id"]
            item: ItemEquip = ItemService.get_item_by_id(item_id)
            bs_level = user.mongo_dict[equip_level_mp[equip_mongo_name]]
            if not item:
                content += f"[{equip_name}] 未装备\n + {bs_level}"
            content += f"[{equip_name}] {name} (+{bs_level})\n"
            content += item.add_status.get_desc(bs_level) + "\n\n"
        else:
            content += f"[{equip_name}] 未装备\n\n"
    return content


def user_bag(params: list, user: User) -> str:
    if len(params) < 1:
        page = 1
    else:
        try:
            page = int(params[0])
        except:
            return "指令错误"
        if page <= 0:
            return "指令错误"
    bag_list = [[k, v] for k, v in user.bag.items()]
    offset = 10
    if not len(bag_list) % offset:
        total = len(bag_list) // offset
    else:
        total = len(bag_list) // offset + 1
    if page > total:
        return f"共{total}页，第{page}页不存在"
    res_content = ""
    for i in range((page - 1) * offset, min(page * offset, len(bag_list))):
        item = ItemService.get_item_by_id(bag_list[i][0])
        if item:
            res_content += f"[{i + 1}] {item.name}({item.type})  数量: {filter_num(bag_list[i][1])}\n"
    return head("我的背包") + res_content + separate("你的资产") + f"💰:{filter_num(user.coin)}" + separate(
        f"第{page}页  共{total}页")


def user_id(params: list, user: User) -> str:
    return user.get_id()


def user_attribute(params: list, user: User) -> str:
    attribute = get_user_attack_pojo(user)
    CombatService.get_combat_score(attribute)
    return head("我的属性") + CombatService.get_attribute_content(attribute) + f"\n[经验加成] {user.exp_add_cnt}%" +  f"\n[金币加成] {user.coin_add_cnt}%" + f"\n[战斗力] {filter_num(CombatService.get_combat_score(attribute))}"


def user_update(params: list, user: User) -> (str, bool):
    need_exp = user.level * max_exp_base
    if user.exp < need_exp:
        return f"升级失败，还需{filter_num(need_exp - user.exp)}点经验才能升级"
    user.level += 1
    attribute = get_user_attack_pojo(user)
    UserService.update_user(user.get_id(), {
        "$inc": {"exp": -need_exp, "level": 1, "blood": attribute.blood_max - attribute.current_blood,
                 "mana": attribute.mana_max - attribute.current_mana}})
    return f"升级成功, {filter_num(user.level)}级->{filter_num(user.level + 1)}级"


def user_attack(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误，请输入冒险者名字"
    user_name = params[0]
    if user.name == user_name:
        return "无法与自己切磋"
    another_user = UserService.get_user_by_name_with_up(user_name)
    if not another_user:
        return f"冒险者\"{user_name}\"不存在"
    me = get_user_attack_pojo(user)
    me.current_blood = me.blood_max
    me.current_mana = me.mana_max
    another = get_user_attack_pojo(another_user)
    _, res_content, attack_result, _ = CombatService.attack(me, another, user.get_id())
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
    combat_record = CombatService.get_combat_record(user.get_id())
    if not combat_record:
        return "近期没有战斗记录"
    last_combat_record_list = combat_record["last_record"]
    if len(last_combat_record_list) < 1:
        return "近期没有战斗记录"
    offset = 8
    if not len(last_combat_record_list) % offset:
        total = len(last_combat_record_list) // offset
    else:
        total = len(last_combat_record_list) // offset + 1
    if page > total:
        return f"共{total}页报告，第{filter_num(page)}页不存在"
    res_content = ""
    for i in range((page - 1) * offset, min(page * offset, len(last_combat_record_list))):
        res_content += f"[{i + 1}]" + last_combat_record_list[i] + "\n"
    return head("战斗详细报告") + res_content + separate(f"第{page}页  共{total}页")


def change_name(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误，请输入你想要改的名字"
    name = params[0]
    if len(name) > 6:
        return "昵称长度应小于等于6"
    if "SP2" not in user.bag:
        return "背包中没有改名卡"
    if not check_name(name):
        return "智能检测未通过，昵称中含有非法词"
    if UserService.is_exist_name(name):
        return "昵称重复"
    user.bag["SP2"] -= 1
    if user.bag["SP2"] == 0:
        del user.bag["SP2"]
    UserService.update_user(user.get_id(),
                            {"$set": {"bag": user.bag, "name": name}})
    return "消耗了一张改名卡，昵称改为:" + name
