from server.pojo.item import ItemNormal, ItemSkill, ItemEquip
from server.pojo.user import User
from server.service.item import ItemService
from server.util import head
from server.service.user import UserService


def see_item(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误"
    item_name = params[0]
    item = ItemService.get_item_by_name(item_name)
    if not item:
        return "不存在该物品"
    return head(item.name + f"({item.type})") + item.description


def sale_item(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误"
    if "+" not in params[0]:
        item_name = params[0]
        cnt = 1
    else:
        item_name, cnt = params[0].split("+")
    try:
        cnt = int(cnt)
    except:
        return "指令错误"
    item = ItemService.get_item_by_name(item_name)
    if not item:
        return "不存在该物品"
    if item.id not in user.bag:
        return "背包中没有该物品"
    remain_cnt = user.bag[item.id]
    if remain_cnt < cnt:
        return f"出售物品个数大于背包中剩余物品个数，背包中剩余数量为{remain_cnt}"
    user.bag[item.id] -= cnt
    if user.bag[item.id] == 0:
        del user.bag[item.id]
    get_coin = int(cnt * item.price * 0.6)
    UserService.update_user(user.get_id(),
                            {"$set": {"bag": user.bag}, "$inc": {"coin": get_coin}})
    return f"出售{cnt}个{item_name}成功，获得{get_coin}💰"


def use_normal_item(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误"
    if "+" not in params[0]:
        item_name = params[0]
        cnt = 1
    else:
        item_name, cnt = params[0].split("+")
    try:
        cnt = int(cnt)
    except:
        return "指令错误"
    item: ItemNormal = ItemService.get_item_by_name(item_name)
    if not item:
        return "不存在该物品"
    if item.type_id != 3:
        return "无法使用该物品"
    if item.id not in user.bag:
        return "背包中没有该物品"
    if cnt > user.bag[item.id]:
        return "物品数量不够"
    user.bag[item.id] -= cnt
    if user.bag[item.id] == 0:
        del user.bag[item.id]
    UserService.update_user(user.get_id(), {"$set": {"bag": user.bag}})
    return item.after_use(user, cnt)


def use_skill_item(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误"
    item_name = params[0]
    item: ItemSkill = ItemService.get_item_by_name(item_name)
    if not item:
        return "不存在该物品"
    if item.type_id != 2:
        return "无法学习该物品"
    if item.id not in user.bag:
        return "背包中没有该物品"
    user.bag[item.id] -= 1
    if user.bag[item.id] == 0:
        del user.bag[item.id]
    UserService.update_user(user.get_id(), {"$set": {"bag": user.bag, "skill": {"id": item.id, "name": item.name}}})
    return f"学习 {item.name} 成功"


position_mp = ["weapon_equip", "head_equip", "body_equip", "pants_equip", "foot_equip", "talisman_equip"]


def use_equip_item(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误"
    item_name = params[0]
    item: ItemEquip = ItemService.get_item_by_name(item_name)
    if not item:
        return "不存在该物品"
    if item.type_id != 1:
        return "无法装备该物品"
    if item.id not in user.bag:
        return "背包中没有该物品"
    user.bag[item.id] -= 1
    if user.bag[item.id] == 0:
        del user.bag[item.id]
    if user.mongo_dict[position_mp[item.position]]["id"]:
        if user.mongo_dict[position_mp[item.position]]["id"] in user.bag:
            user.bag[user.mongo_dict[position_mp[item.position]]["id"]] += 1
        else:
            user.bag[user.mongo_dict[position_mp[item.position]]["id"]] = 1
    UserService.update_user(user.get_id(),
                            {"$set": {"bag": user.bag, position_mp[item.position]: {"id": item.id, "name": item.name}}})
    return f"装备 {item.name} 成功"


def off_equip_item(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误"
    item_name = params[0]
    f_p = -1
    for i, e in enumerate(position_mp):
        if item_name == user.mongo_dict[e]["name"]:
            f_p = i
    if f_p == -1:
        return "身上没有这件装备"
    item_id = user.mongo_dict[position_mp[f_p]]["id"]
    if item_id:
        if item_id in user.bag:
            user.bag[item_id] += 1
        else:
            user.bag[item_id] = 1
    UserService.update_user(user.get_id(), {"$set": {"bag": user.bag, position_mp[f_p]: {"id": "", "name": ""}}})
    return f"卸下 {item_name} 成功"
