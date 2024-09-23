from gv import Global
from server.error import LFError
from server.pojo.item import StatusAdd, ItemEquip, ItemSpecial, ItemNormal, ItemSkill
from server.pojo.user import User
from server.pojo.attack import CombatPojo
from server.util import make_decision
import random


def N1(user: User, user_combat_pojo: CombatPojo, cnt: int) -> str:
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"exp": 100 * cnt}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"增加了{100 * cnt}点经验"


def N2(user: User, user_combat_pojo: CombatPojo, cnt: int) -> str:
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"exp_add_cnt": cnt}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"提升了{cnt}%经验加成"


def N3(user: User, user_combat_pojo: CombatPojo, cnt: int) -> str:
    add_blood = (user_combat_pojo.blood_max * 0.1) * cnt
    current_blood = user.blood
    if current_blood == user_combat_pojo.blood_max:
        return "你的生命已满，无需使用生命药剂"
    if current_blood + add_blood >= user_combat_pojo.blood_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"blood": user_combat_pojo.blood_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的生命已回满，恢复了{user_combat_pojo.blood_max - current_blood}点生命"
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"blood": add_blood}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{add_blood}点生命"


def N4(user: User, user_combat_pojo: CombatPojo, cnt: int) -> str:
    add_mana = (user_combat_pojo.mana_max * 0.1) * cnt
    current_mana = user.mana
    if current_mana == user_combat_pojo.mana_max:
        return "你的魔力已满，无需使用魔力药剂"
    if current_mana + add_mana >= user_combat_pojo.mana_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"mana": user_combat_pojo.mana_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的魔力已回满，恢复了{user_combat_pojo.mana_max - current_mana}点魔力"
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"mana": add_mana}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{add_mana}点生命"

def N5(user: User, user_combat_pojo: CombatPojo, cnt: int) -> str:
    add_blood = (user_combat_pojo.blood_max * 0.3) * cnt
    current_blood = user.blood
    if current_blood == user_combat_pojo.blood_max:
        return "你的生命已满，无需使用生命药剂"
    if current_blood + add_blood >= user_combat_pojo.blood_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"blood": user_combat_pojo.blood_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的生命已回满，恢复了{user_combat_pojo.blood_max - current_blood}点生命"
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"blood": add_blood}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{add_blood}点生命"


def N6(user: User, user_combat_pojo: CombatPojo, cnt: int) -> str:
    add_mana = (user_combat_pojo.mana_max * 0.3) * cnt
    current_mana = user.mana
    if current_mana == user_combat_pojo.mana_max:
        return "你的魔力已满，无需使用魔力药剂"
    if current_mana + add_mana >= user_combat_pojo.mana_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"mana": user_combat_pojo.mana_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的魔力已回满，恢复了{user_combat_pojo.mana_max - current_mana}点魔力"
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"mana": add_mana}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{add_mana}点生命"

def N7(user: User, user_combat_pojo: CombatPojo, cnt: int) -> str:
    add_blood = (user_combat_pojo.blood_max * 0.7) * cnt
    current_blood = user.blood
    if current_blood == user_combat_pojo.blood_max:
        return "你的生命已满，无需使用生命药剂"
    if current_blood + add_blood >= user_combat_pojo.blood_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"blood": user_combat_pojo.blood_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的生命已回满，恢复了{user_combat_pojo.blood_max - current_blood}点生命"
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"blood": add_blood}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{add_blood}点生命"


def N8(user: User, user_combat_pojo: CombatPojo, cnt: int) -> str:
    add_mana = (user_combat_pojo.mana_max * 0.7) * cnt
    current_mana = user.mana
    if current_mana == user_combat_pojo.mana_max:
        return "你的魔力已满，无需使用魔力药剂"
    if current_mana + add_mana >= user_combat_pojo.mana_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"mana": user_combat_pojo.mana_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的魔力已回满，恢复了{user_combat_pojo.mana_max - current_mana}点魔力"
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"mana": add_mana}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{add_mana}点生命"


def N9(user: User, user_combat_pojo: CombatPojo, cnt: int) -> str:
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={
        "$set": {"blood": user_combat_pojo.blood_max, "mana": user_combat_pojo.mana_max}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"你的血量和魔力已回满"


def SK1(pojo_proactive: CombatPojo, pojo_reactive: CombatPojo) -> (str, bool):
    if not make_decision(0.5):
        return "", False
    content = ""
    base_attack = max(pojo_proactive.attack - pojo_reactive.defense, 1) * random.uniform(1.1, 1.2) * 1.5
    content += f"{pojo_proactive.name}触发技能全力一击,"
    is_critical =  make_decision(min(pojo_proactive.critical_strike, 1))
    if is_critical:
        content += "并造成了暴击,"
        base_attack = (1 + pojo_proactive.critical_damage) * base_attack
    base_attack = int(base_attack)
    pojo_reactive.current_blood -= base_attack
    pojo_proactive.current_mana -= 100
    if pojo_reactive.current_blood < 0:
        pojo_reactive.current_blood = 0
    content += f"对{pojo_reactive.name}造成{base_attack}点伤害"
    return content, True

normal_items = [ItemNormal("N1", "经验药水", "获得100点经验", 500, True, N1),
             ItemNormal("N2", "经验丹", "永久提升1%的经验加成", 500000, True, N2),
             ItemNormal("N3", "小生命药水", "恢复10%血量", 100, True, N3),
             ItemNormal("N4", "小魔力药水", "恢复10%魔力", 100, True, N4),
            ItemNormal("N5", "中生命药水", "恢复30%血量", 300, True, N5),
            ItemNormal("N6", "中魔力药水", "恢复30%魔力", 300, True, N6),
            ItemNormal("N7", "大生命药水", "恢复70%血量", 700, True, N7),
            ItemNormal("N8", "大魔力药水", "恢复70%魔力", 700, True, N8),
             ItemNormal("N9", "圣水", "回满血量和魔力", 1000, True, N9),]

equip_items = [ItemEquip("EQ1", "树棍", "地上捡的树枝做的棍子", 1000, True, 0, StatusAdd(attack=50)),
             ItemEquip("EQ2", "草帽", "用草编织而成的帽子", 1000, True, 1, StatusAdd(defense=20)),
             ItemEquip("EQ3", "兽皮衣", "用野兽的皮做的衣服", 1000, True, 2, StatusAdd(defense=30, blood_max=100)),
             ItemEquip("EQ4", "兽皮裤", "用野兽的皮做的裤子", 1000, True, 3, StatusAdd(defense=20)),
             ItemEquip("EQ5", "草鞋", "用草编织而成的鞋子", 1000, True, 4, StatusAdd(speed=1)),
             ItemEquip("EQ6", "薰衣草护符", "用薰衣草做的护符，有一股淡淡的清香", 100000, True, 5,
                       StatusAdd(critical_strike=0.01, critical_damage=0.1, speed=1)),
             ItemEquip("EQ7", "法棍", "怎么可以拿面包做武器！", 10000, True, 0, StatusAdd(attack=100)),
             ItemEquip("EQ8", "圣剑", "传说中的勇者用过的剑", 10000000, False, 0,
                       StatusAdd(attack=2000, critical_strike=0.5, critical_damage=2)),
             ItemEquip("EQ9", "圣盔", "传说中的勇者戴过的头盔", 10000000, False, 1, StatusAdd(defense=500)),
             ItemEquip("EQ10", "圣者上装", "传说中的勇者穿过的衣服", 10000000, False, 2, StatusAdd(defense=1000, blood_max=5000)),
             ItemEquip("EQ11", "圣者下装", "传说中的勇者穿过的裤子", 10000000, False, 3, StatusAdd(defense=500)),
             ItemEquip("EQ12", "圣速鞋", "传说中的勇者穿过的鞋子", 10000000, False, 4, StatusAdd(speed=20)),
             ItemEquip("EQ13", "女神护符", "传说中女神赐予勇者的护符", 100000000, False, 5,
                       StatusAdd(critical_strike=0.2, critical_damage=1, speed=10)),
             ItemEquip("EQ14", "神剑", "只有神才能用的剑🗡️上面充满着神秘的气息", 500000000, False, 0,
                       StatusAdd(attack=5000, critical_strike=0.6, critical_damage=4)),
            ItemEquip("EQ15", "雷霆枪", "蕴含雷霆神力的枪", 500000, False, 0, StatusAdd(attack=250,critical_strike=0.1, critical_damage=0.2)),
            ItemEquip("EQ16", "雷霆战盔", "覆盖着雷霆之力的头盔", 500000, False, 1, StatusAdd(defense=80, blood_max=200, speed=1)),
            ItemEquip("EQ17", "雷霆战铠", "蕴含雷霆神力的战铠", 500000, False, 2, StatusAdd(defense=100, blood_max=400, speed=1)),
            ItemEquip("EQ18", "雷霆护腿", "蕴含雷霆神力的护腿", 500000, False, 3, StatusAdd(defense=80, speed=1)),
            ItemEquip("EQ19", "雷霆战鞋", "迅捷如闪电的战靴", 500000, False, 4, StatusAdd(speed=7)) ]

special_items = [ItemSpecial("SP1", "强化石", "用来强化身上的部位，前往铁匠铺使用", 200, True),]
skill_items = [ItemSkill("SK1", "全力一击", "攻击时触发,触发概率:20%\n消耗魔力:100\n伤害加成:50%", 20000, True,
                       on_attack=SK1)]
all_items = [*special_items,*normal_items, *skill_items, *equip_items]

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
