from server.pojo.user import User
from server.service.item import ItemService
from server.util import head, separate
from server.service.user import UserService
from server.util import filter_num


def see_store(params: list, user: User) -> str:
    if len(params) < 1:
        page = 1
    else:
        try:
            page = int(params[0])
        except:
            return "指令错误"
        if page <= 0:
            return "指令错误"
    store_list = ItemService.get_store_list()
    offset = 10
    if not len(store_list) % offset:
        total = len(store_list) // offset
    else:
        total = len(store_list) // offset + 1
    if page > total:
        return f"共{total}页，第{filter_num(page)}页不存在"
    res_content = ""
    for i in range((page - 1) * offset, min(page * offset, len(store_list))):
        res_content += f"[{i + 1}] {store_list[i].name}({store_list[i].type})  {filter_num(store_list[i].price)}💰\n"
    return head("商店列表") + res_content + separate("你的资产") + f"💰:{filter_num(user.coin)}" + separate(
        f"第{page}页  共{total}页")


def buy_item(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误，请输入你想要购买的商品名字及数量"
    if "+" not in params[0]:
        item_name = params[0]
        cnt = 1
    else:
        item_name, cnt = params[0].split("+")
    try:
        cnt = int(cnt)
    except:
        return "指令错误"
    item = ItemService.get_store_item_by_name(item_name)
    if not item:
        return "该物品无法从商店购买"
    if user.coin - item.price * cnt < 0:
        return f"你的💰不足以购买{filter_num(cnt)}个{item_name}"
    if item.id in user.bag:
        user.bag[item.id] += cnt
    else:
        user.bag[item.id] = cnt
    UserService.update_user(user.get_id(), {"$set": {"bag": user.bag}, "$inc": {"coin": -item.price * cnt}})
    return f"购买{filter_num(cnt)}个 {item_name} 成功，花费{filter_num(item.price * cnt)}💰"
