from gv import Global
from server.error import LFError
from server.pojo.item import  StatusAdd, ItemEquip, ItemSpecial, ItemNormal, ItemSkill
def SP1(user_id: str) -> str:
    pass

def N1(user_id: str) -> bool:
    result = Global.user_c.update_one(filter={"_id": user_id}, update={"$inc": {"exp": 100}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return True

def N2(user_id: str) -> bool:
    result = Global.user_c.update_one(filter={"_id": user_id}, update={"$inc": {"exp_add_cnt": 1}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return True


all_items = [ItemSpecial("SP1","强化石","用来强化身上的部位", 100, True, SP1),
             ItemNormal("N1","经验药水","获得100点经验", 1000, True, N1),
              ItemNormal("N2", "经验丹", "永久提升1%的经验加成", 500000, True, N1),
              ItemEquip("EQ1","树枝","攻击:10", 1000, True, 0,StatusAdd(attack=10)),
              ItemEquip("EQ2", "兽皮衣", "防御:10", 1000, True, 2,StatusAdd(defense=10)),
              ItemEquip("EQ3", "草鞋", "速度:1", 1000, True, 3,StatusAdd(speed=1)),
              ItemEquip("EQ4", "草帽", "防御:5", 1000, True, 1,StatusAdd(defense=5)),
              ItemEquip("EQ5", "薰衣草护符", "暴击率:1%, 暴击伤害: 10%, 速度：1", 100000, True,4, StatusAdd(critical_strike=0.01, critical_damage=0.1, speed=1)),
              ItemSkill("SK1", "全力一击", "触发概率:10%, 消耗魔力:50, 伤害加成：10%", 20000, True, need_mono= 50,attack_add_pct=0.1, probability=0.1),
             ItemSkill("SK1", "全力一闪", "触发概率:5%, 消耗魔力:50, 躲避一次攻击", 50000, True, need_mono=50, attack_add_pct=-1, probability=0.05),
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

