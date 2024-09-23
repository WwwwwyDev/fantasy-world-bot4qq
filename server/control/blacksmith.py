from server.service.user import UserService
from server.pojo.user import User
from server.util import make_decision
from server.control.util import equip_mp


def strengthen_equip(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误，请选择你需要强化的部位"
    equip = params[0]
    if equip not in equip_mp:
        return "没有该部位"
    mongo_equip = equip_mp[equip]
    current_level = user.mongo_dict[mongo_equip]
    num = (current_level + 1) * 12
    if "SP1" not in user.bag:
        return "背包中没有强化石"
    if user.bag["SP1"] < num:
        return f"强化所需{num}个强化石，还差{num - user.bag['SP1']}个"
    min_p = 0.03
    if current_level >= 20:
        min_p = 0.01
    p = max(1 - current_level * 0.07, min_p)
    add_level = 0
    if make_decision(p):
        add_level = 1
    user.bag["SP1"] -= num
    remain_stone = user.bag["SP1"]
    if user.bag["SP1"] == 0:
        del user.bag["SP1"]
    UserService.update_user(user.get_id(),
                            {"$set": {"bag": user.bag}, "$inc": {mongo_equip: add_level}})
    if add_level:
        return f"{equip}部位 {current_level}->{current_level + 1} 强化成功，剩余{remain_stone}个强化石，下一次强化成功率为{int(max(1 - (current_level+1) * 0.07, 0.03) * 100)}%"
    else:
        return f"{equip}部位强化失败，剩余{remain_stone}个强化石，成功率{int(p * 100)}%"

