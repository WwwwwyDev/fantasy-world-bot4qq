from gv import Global
from server.error import LFError
from server.pojo.item import StatusAdd, ItemEquip, ItemSpecial, ItemNormal, ItemSkill
from server.pojo.user import User


def N1(user: User, cnt: int) -> str:
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"exp": 100 * cnt}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"增加了{100 * cnt}点经验"


def N2(user: User, cnt: int) -> str:
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"exp_add_cnt": cnt}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"提升了{cnt}%经验加成"


all_items = [ItemSpecial("SP1", "强化石", "用来强化身上的部位，前往铁匠铺使用", 200, True),
             ItemNormal("N1", "经验药水", "获得100点经验", 1000, True, N1),
             ItemNormal("N2", "经验丹", "永久提升1%的经验加成", 500000, True, N2),
             ItemEquip("EQ1", "树棍", "地上捡的树枝做的棍子", 1000, True, 0, StatusAdd(attack=10)),
             ItemEquip("EQ2", "草帽", "用草编织而成的帽子", 1000, True, 1, StatusAdd(defense=5)),
             ItemEquip("EQ3", "兽皮衣", "用野兽的皮做的衣服", 1000, True, 2, StatusAdd(defense=10)),
             ItemEquip("EQ4", "兽皮裤", "用野兽的皮做的裤子", 1000, True, 3, StatusAdd(defense=10)),
             ItemEquip("EQ5", "草鞋", "用草编织而成的鞋子", 1000, True, 4, StatusAdd(speed=1)),
             ItemEquip("EQ6", "薰衣草护符", "用薰衣草做的护符，有一股淡淡的清香", 100000, True, 5,
                       StatusAdd(critical_strike=0.01, critical_damage=0.1, speed=1)),
             ItemEquip("EQ7", "法棍", "怎么可以拿面包做武器！", 50000, True, 0, StatusAdd(attack=50)),
             ItemSkill("SK1", "全力一击", "触发概率:10%\n消耗魔力:50\n伤害加成:10%", 20000, True, need_mono=50,
                       attack_add_pct=0.1, probability=0.1),
             ItemSkill("SK1", "全力一闪", "触发概率:5%\n消耗魔力:50\n躲避一次攻击", 50000, True, need_mono=50,
                       attack_add_pct=-1, probability=0.05),
             ]

store_items = []
items_mp_by_name = {}
store_items_mp_by_name = {}
items_mp_by_id = {}
for item in all_items:
    items_mp_by_name[item.name] = item
    items_mp_by_id[item.id] = item
    if item.is_on_store:
        store_items_mp_by_name[item.name] = item
        store_items.append(item)
