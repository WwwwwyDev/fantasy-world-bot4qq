import copy
import math

from gv import Global
from server.error import LFError
from server.pojo.item import StatusAdd, ItemEquip, ItemSpecial, ItemNormal, ItemSkill, Item
from server.pojo.user import User
from server.pojo.attack import CombatPojo
from server.util import make_decision, filter_num
import random


def N1(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"exp": 200 * cnt}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"增加了{filter_num(200 * cnt)}点经验", cnt


def N2(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    if user.exp_add_cnt + cnt > 30:
        cnt = 30 - user.exp_add_cnt
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"exp_add_cnt": cnt}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"经验丹最多可以使用30次，当前已使用次数:{user.exp_add_cnt}次", cnt
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"exp_add_cnt": cnt}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"提升了{filter_num(cnt)}%经验加成", cnt

def N10(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    if user.coin_add_cnt + cnt > 30:
        cnt = 30 - user.coin_add_cnt
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"coin_add_cnt": cnt}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"金币丹最多可以使用30次，当前已使用次数:{user.coin_add_cnt}次", cnt
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"coin_add_cnt": cnt}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"提升了{filter_num(cnt)}%金币加成", cnt

def N3(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    add_blood = (user_combat_pojo.blood_max * 0.1) * cnt
    current_blood = user.blood
    if current_blood == user_combat_pojo.blood_max:
        return "你的生命已满，无需使用生命药剂", 0
    if current_blood + add_blood >= user_combat_pojo.blood_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"blood": user_combat_pojo.blood_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的生命已回满，恢复了{filter_num(user_combat_pojo.blood_max - current_blood)}点生命", math.ceil((user_combat_pojo.blood_max - current_blood) / (user_combat_pojo.blood_max * 0.1))
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"blood": add_blood}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{filter_num(add_blood)}点生命", cnt


def N4(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    add_mana = (user_combat_pojo.mana_max * 0.1) * cnt
    current_mana = user.mana
    if current_mana == user_combat_pojo.mana_max:
        return "你的魔力已满，无需使用魔力药剂", 0
    if current_mana + add_mana >= user_combat_pojo.mana_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"mana": user_combat_pojo.mana_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的魔力已回满，恢复了{filter_num(user_combat_pojo.mana_max - current_mana)}点魔力", math.ceil((user_combat_pojo.mana_max - current_mana) / (user_combat_pojo.mana_max * 0.1))
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"mana": add_mana}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{filter_num(add_mana)}点魔力", cnt


def N5(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    add_blood = (user_combat_pojo.blood_max * 0.3) * cnt
    current_blood = user.blood
    if current_blood == user_combat_pojo.blood_max:
        return "你的生命已满，无需使用生命药剂", 0
    if current_blood + add_blood >= user_combat_pojo.blood_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"blood": user_combat_pojo.blood_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的生命已回满，恢复了{filter_num(user_combat_pojo.blood_max - current_blood)}点生命", math.ceil((user_combat_pojo.blood_max - current_blood) / (user_combat_pojo.blood_max * 0.3))
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"blood": add_blood}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{filter_num(add_blood)}点生命", cnt


def N6(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    add_mana = (user_combat_pojo.mana_max * 0.3) * cnt
    current_mana = user.mana
    if current_mana == user_combat_pojo.mana_max:
        return "你的魔力已满，无需使用魔力药剂", 0
    if current_mana + add_mana >= user_combat_pojo.mana_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"mana": user_combat_pojo.mana_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的魔力已回满，恢复了{filter_num(user_combat_pojo.mana_max - current_mana)}点魔力",  math.ceil((user_combat_pojo.mana_max - current_mana) / (user_combat_pojo.mana_max * 0.3))
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"mana": add_mana}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{filter_num(add_mana)}点魔力", cnt


def N7(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    add_blood = (user_combat_pojo.blood_max * 0.7) * cnt
    current_blood = user.blood
    if current_blood == user_combat_pojo.blood_max:
        return "你的生命已满，无需使用生命药剂", 0
    if current_blood + add_blood >= user_combat_pojo.blood_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"blood": user_combat_pojo.blood_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的生命已回满，恢复了{filter_num(user_combat_pojo.blood_max - current_blood)}点生命", math.ceil((user_combat_pojo.blood_max - current_blood) / (user_combat_pojo.blood_max * 0.7))
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"blood": add_blood}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{filter_num(add_blood)}点生命", cnt


def N8(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    add_mana = (user_combat_pojo.mana_max * 0.7) * cnt
    current_mana = user.mana
    if current_mana == user_combat_pojo.mana_max:
        return "你的魔力已满，无需使用魔力药剂", 0
    if current_mana + add_mana >= user_combat_pojo.mana_max:
        result = Global.user_c.update_one(filter={"_id": user.get_id()},
                                          update={"$set": {"mana": user_combat_pojo.mana_max}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"你的魔力已回满，恢复了{filter_num(user_combat_pojo.mana_max - current_mana)}点魔力", math.ceil((user_combat_pojo.mana_max - current_mana) / (user_combat_pojo.mana_max * 0.7))
    else:
        result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={"$inc": {"mana": add_mana}})
        if result.matched_count == 0:
            raise LFError("[error] 数据库更新失败")
        return f"恢复了{filter_num(add_mana)}点魔力", cnt


def N9(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={
        "$set": {"blood": user_combat_pojo.blood_max, "mana": user_combat_pojo.mana_max}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"你的血量和魔力已回满", 1

new_items = {"N1": 50, "N3": 100, "SP1": 100,"N4": 100, "EQ1": 1, "EQ2": 1, "EQ3": 1,"EQ4": 1, "EQ5": 1}
def N11(user: User, user_combat_pojo: CombatPojo, cnt: int) -> (str, int):
    for k, v in new_items.items():
        if k in user.bag:
            user.bag[k] += v
        else:
            user.bag[k] = v
    result = Global.user_c.update_one(filter={"_id": user.get_id()}, update={
        "$set": {"bag": user.bag}, "$inc": {"coin": 1000000}})
    if result.matched_count == 0:
        raise LFError("[error] 数据库更新失败")
    return f"开启新手礼包。获得了 50个经验药水，100个小生命药水，100个小魔力药水，100个强化石，1套新手套装以及{filter_num(1000000)}💰", 1


def SK1(pojo_proactive: CombatPojo, pojo_reactive: CombatPojo) -> (str, bool, int):
    if not make_decision(0.2):
        return "", False, 0
    content = ""
    base_attack = max(pojo_proactive.attack - pojo_reactive.defense, 1) * random.uniform(1.1, 1.2) * 1.3 * (1 + pojo_proactive.hurt_percentage_add)
    content += f"{pojo_proactive.name}触发技能全力一击，"
    is_critical = make_decision(min(max(pojo_proactive.critical_strike - pojo_reactive.defense_strike, 0), 1))
    if is_critical:
        content += "并造成了暴击，"
        base_attack = (1 + pojo_proactive.critical_damage) * base_attack
    base_attack = int(base_attack)
    pojo_reactive.current_blood -= base_attack
    pojo_proactive.current_mana -= 100
    if pojo_reactive.current_blood < 0:
        pojo_reactive.current_blood = 0
    content += f"对{pojo_reactive.name}造成{filter_num(base_attack)}点伤害"
    return content, True, base_attack

def SK2(pojo_proactive: CombatPojo, pojo_reactive: CombatPojo) -> (str, bool, int):
    if not make_decision(0.3):
        return "", False, 0
    content = ""
    content += f"{pojo_proactive.name}触发技能翠绿之舞，"
    get_blood = int(pojo_proactive.blood_max * 0.3)
    pojo_proactive.current_blood += get_blood
    content += f"回复了{filter_num(get_blood)}点生命值"
    return content, True, 0

def SK3(pojo_proactive: CombatPojo, pojo_reactive: CombatPojo) -> (str, bool, int):
    if not make_decision(0.5):
        return "", False, 0
    content = ""
    base_attack = max(pojo_proactive.attack - pojo_reactive.defense, 1) * random.uniform(1.1, 1.2) * 2 * (1 + pojo_proactive.hurt_percentage_add)
    content += f"{pojo_proactive.name}触发技能‌雷霆万钧，"
    is_critical = make_decision(min(max(pojo_proactive.critical_strike - pojo_reactive.defense_strike, 0), 1))
    if is_critical:
        content += "并造成了暴击，"
        base_attack = (1 + pojo_proactive.critical_damage) * base_attack
    base_attack = int(base_attack)
    pojo_reactive.current_blood -= base_attack
    pojo_proactive.current_mana -= 100
    if pojo_reactive.current_blood < 0:
        pojo_reactive.current_blood = 0
    content += f"对{pojo_reactive.name}造成{filter_num(base_attack)}点伤害"
    return content, True, base_attack

def SK4(pojo_proactive: CombatPojo, pojo_reactive: CombatPojo) -> (str, bool, int):
    if not make_decision(0.4):
        return "", False, 0
    content = ""
    base_attack = max(pojo_proactive.attack - pojo_reactive.defense, 1) * random.uniform(1.1, 1.2) * 2 * (1 + pojo_proactive.hurt_percentage_add)
    content += f"{pojo_proactive.name}触发技能‌星罗秘术‌，"
    is_critical = make_decision(min(max(pojo_proactive.critical_strike - pojo_reactive.defense_strike + 0.2, 0), 1))
    if is_critical:
        content += "并造成了暴击，"
        base_attack = (1 + pojo_proactive.critical_damage) * base_attack
    base_attack = int(base_attack)
    pojo_reactive.current_blood -= base_attack
    pojo_proactive.current_mana -= 100
    if pojo_reactive.current_blood < 0:
        pojo_reactive.current_blood = 0
    get_blood = int(pojo_proactive.blood_max * 0.3)
    pojo_proactive.current_blood += get_blood
    content += f"对{pojo_reactive.name}造成{filter_num(base_attack)}点伤害，并回复了{filter_num(get_blood)}点生命值"
    return content, True, base_attack


normal_items = [ItemNormal("N1", "经验药水", "获得200点经验", 500,  N1),
                ItemNormal("N2", "经验丹", "永久提升1%的经验加成，单个账号最多使用30次", 5000000, N2),
                ItemNormal("N10", "金币丹", "永久提升1%的金币加成，单个账号最多使用30次", 10000000, N10),
                ItemNormal("N3", "小生命药水", "恢复10%血量", 100,  N3),
                ItemNormal("N4", "小魔力药水", "恢复10%魔力", 100,  N4),
                ItemNormal("N5", "中生命药水", "恢复30%血量", 300,  N5),
                ItemNormal("N6", "中魔力药水", "恢复30%魔力", 300,  N6),
                ItemNormal("N7", "大生命药水", "恢复70%血量", 700,  N7),
                ItemNormal("N8", "大魔力药水", "恢复70%魔力", 700,  N8),
                ItemNormal("N9", "圣水", "回满血量和魔力", 1000,  N9),
                ItemNormal("N11", "新手礼包", "里面有冒险家工会给予的新手物资", 0, N11),
                ]

equip_items = [ItemEquip("EQ1", "树棍", "地上捡的树枝做的棍子", 1000, 0, StatusAdd(attack=50)),
               ItemEquip("EQ2", "草帽", "用草编织而成的帽子", 1000, 1, StatusAdd(defense=20)),
               ItemEquip("EQ3", "兽皮衣", "用野兽的皮做的衣服", 1000, 2, StatusAdd(defense=30, blood_max=100)),
               ItemEquip("EQ4", "兽皮裤", "用野兽的皮做的裤子", 1000, 3, StatusAdd(defense=20)),
               ItemEquip("EQ5", "草鞋", "用草编织而成的鞋子", 1000, 4, StatusAdd(speed=1)),
               ItemEquip("EQ6", "薰衣草护符", "用薰衣草做的护符，有一股淡淡的清香", 100000, 5,
                         StatusAdd(critical_strike=0.05, critical_damage=0.2, speed=1)),
               ItemEquip("EQ7", "法棍", "怎么可以拿面包做武器！", 10000,  0, StatusAdd(attack=100)),
               ItemEquip("EQ8", "勇者剑", "传说中的勇者用过的剑", 50000000, 0,
                         StatusAdd(attack=2000, critical_strike=0.5, critical_damage=2, hurt_percentage_add=0.2, attack_percentage_add=0.5)),
               ItemEquip("EQ9", "勇者盔", "传说中的勇者戴过的头盔", 50000000, 1, StatusAdd(defense=500, defense_percentage_add=0.05, blood_max_percentage_add=0.05)),
               ItemEquip("EQ10", "勇者上装", "传说中的勇者穿过的衣服", 50000000,  2,
                         StatusAdd(defense=1000, blood_max=5000, defense_percentage_add=0.1, blood_max_percentage_add=0.1)),
               ItemEquip("EQ11", "勇者下装", "传说中的勇者穿过的裤子", 50000000,  3, StatusAdd(defense=500, defense_percentage_add=0.1, mana_max=1000, blood_max_percentage_add=0.05)),
               ItemEquip("EQ12", "勇者鞋", "传说中的勇者穿过的鞋子", 50000000,  4, StatusAdd(speed=20, defense=200, defense_percentage_add=0.05, blood_max_percentage_add=0.05)),
               ItemEquip("EQ13", "女神护符", "传说中女神赐予勇者的护符", 100000000,  5,
                         StatusAdd(critical_strike=0.3, critical_damage=1, speed=10, defense_strike=0.2, mana_max_percentage_add=0.1)),
               ItemEquip("EQ14", "神剑", "只有神才能用的剑🗡️上面充满着神秘的气息", 500000000, 0,
                         StatusAdd(attack=5000, critical_strike=8, critical_damage=4, hurt_percentage_add=0.5, attack_percentage_add=1)),
               ItemEquip("EQ15", "萤草之荷光", "用于「斩草」的薙刀。对向此物之军势，也会如苇草般倒下吧...", 5000000, 0,
                         StatusAdd(attack=1000, critical_strike=0.2, critical_damage=2, attack_percentage_add=0.1, hurt_percentage_add=0.1)),
               ItemEquip("EQ16", "雪猎的荒神兜帽", "密林卧雪的猎人穿过的兜帽", 1000000,  1,
                         StatusAdd(defense=300, blood_max=2000, speed=1, blood_max_percentage_add=0.05)),
               ItemEquip("EQ17", "雪猎的巨蜥上装", "密林卧雪的猎人穿过的上装", 2000000,  2,
                         StatusAdd(defense=600, blood_max=4000, speed=1, defense_percentage_add=0.05, blood_max_percentage_add=0.05)),
               ItemEquip("EQ18", "雪猎的冰龙下装", "密林卧雪的猎人穿过的下装", 1500000,  3, StatusAdd(defense=300, speed=1, defense_percentage_add=0.05)),
               ItemEquip("EQ19", "雪猎的鹿皮软靴", "密林卧雪的猎人穿过的靴子", 1000000,  4, StatusAdd(speed=7)),
                ItemEquip("EQ20", "繁星位面球", "据说拥有它可以实现跨越不同维度或空间的移动", 100000000,  5, StatusAdd(speed=20)),
               ItemEquip("EQ21", "狼的末日", "狼的骑士所使的大剑。原本只是城中铁匠赠予的厚重的铁片，却在他与狼的情谊中，获得神话般的力量", 5000000, 0,
                         StatusAdd(attack=1000, critical_strike=0.5, critical_damage=1, attack_percentage_add=0.2,
                                   hurt_percentage_add=0.05)),
                ItemEquip("EQ22", "铁剑", "普通的铁制大剑", 10000, 0, StatusAdd(attack=200)),
               ItemEquip("EQ23", "护卫头盔", "用铁制成的头盔", 10000, 1, StatusAdd(defense=80)),
               ItemEquip("EQ24", "铁制胸甲", "用铁制成的胸甲", 10000, 2, StatusAdd(defense=100, blood_max=500)),
               ItemEquip("EQ25", "铁制胫甲", "用铁制成的胫甲", 10000, 3, StatusAdd(defense=80)),
               ItemEquip("EQ26", "布鞋", "用布编织而成的鞋子", 10000, 4, StatusAdd(speed=3)),
               ItemEquip("EQ27", "将军长枪", "将军的枪，锋利无比", 100000, 0, StatusAdd(attack=500, attack_percentage_add=0.01)),
               ItemEquip("EQ28", "将军头盔", "将军的头盔，坚固无比", 100000, 1, StatusAdd(defense=180)),
               ItemEquip("EQ29", "将军胸甲", "将军的的胸甲，坚无可催", 100000, 2, StatusAdd(defense=200, blood_max=1000, blood_max_percentage_add=0.01)),
               ItemEquip("EQ30", "将军胫甲", "将军的胫甲，坚固无比", 100000, 3, StatusAdd(defense=180)),
               ItemEquip("EQ31", "将军鞋", "将军的鞋子，速度极快", 100000, 4, StatusAdd(speed=5)),
               ItemEquip("EQ32", "狂龙的怒火", "你可以惹恼我，只要你能承担后果", 1000000, 0,
                         StatusAdd(attack=1000, attack_percentage_add=0.1, critical_strike=0.1, critical_damage=0.2)),
               ItemEquip("EQ33", "古拉德头帽", "也许是熟悉了波动的热度，我已经忘记被火烧伤是什么感觉了", 1000000, 1, StatusAdd(defense=300, defense_percentage_add=0.05, blood_max_percentage_add=0.05)),
               ItemEquip("EQ34", "古拉德胸甲", "这胸甲让我有一种到处放火的冲动", 1000000, 2,
                         StatusAdd(defense=500, blood_max=2000, blood_max_percentage_add=0.1, defense_percentage_add=0.1)),
               ItemEquip("EQ35", "古拉德胫甲", "火这东西，当你熟悉后就不会觉得可怕了", 1000000, 3, StatusAdd(defense=300, defense_percentage_add=0.05, blood_max_percentage_add=0.05)),
               ItemEquip("EQ36", "古拉德短靴", "穿它在火焰中行走，保证不会被烫伤", 1000000, 4, StatusAdd(speed=10, defense_percentage_add=0.05)),
               ItemEquip("EQ36", "骸骨的戒指", "看起来阴森可怕", 2000000, 5,
                         StatusAdd(defense_percentage_add=0.2, blood_max_percentage_add=0.2, attack_percentage_add=0.2)),
               ItemEquip("EQ37", "疾风鞋", "比风还快", 1000000, 4, StatusAdd(speed=10)),
               ]

special_items = [ItemSpecial("SP1", "强化石", "用来强化身上的部位，前往铁匠铺使用", 200)]
skill_items = [ItemSkill("SK1", "全力一击", "汇集全身力量发动一次攻击，触发概率:20%\n消耗魔力:100\n伤害加成:30%", 200000, on_attack=SK1),
               ItemSkill("SK2", "翠绿之舞‌", "给人一种生机勃勃的感觉，可能是某种治愈或恢复类技能，触发概率:20%\n消耗魔力:100\n生命回复:30%", 1000000, on_attack=SK2),
               ItemSkill("SK3", "雷霆万钧‌", "充满力量感，代表强大的雷电攻击技能，能够瞬间造成巨大伤害，令人感受到技能的威力与震撼，触发概率:50%\n消耗魔力:500\n伤害加成:100%", 2000000, on_attack=SK3),
               ItemSkill("SK4", "‌星罗秘术‌", "充满神秘感，可能代表某种高阶技能或秘技，蕴含深不可测的力量，代表角色实力的巅峰，触发概率:40%\n消耗魔力:1000\n生命回复:30%\n伤害加成:100%\n暴击率提升:20%", 5000000, on_attack=SK3)]
all_items = [*special_items, *normal_items, *skill_items, *equip_items]

# 上架商店的物品
on_store_items = {"SP1", "N1", "N2", "N10", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "EQ1", "EQ2", "EQ3", "EQ4", "EQ5", "EQ6", "EQ7"}
store_items = []
store_items_mp_by_name = {}


items_mp_by_name = {}
items_mp_by_id = {}
for item in all_items:
    items_mp_by_name[item.name] = item
    items_mp_by_id[item.id] = item
    if item.id in on_store_items:
        store_items_mp_by_name[item.name] = item
        store_items.append(item)

# 幻塔挂机与扫荡掉落
tower_monster_dropping = ["N1", "N2","N10", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "SP1"]
tower_monster_dropping_p = []
for i in range(len(tower_monster_dropping)):
    item_temp: Item = items_mp_by_id[tower_monster_dropping[i]]
    tower_monster_dropping[i] = item_temp
    tower_monster_dropping_p.append(10/item_temp.price)

# 装备掉落
tower_boss_dropping = [*copy.deepcopy(equip_items[7:]), *copy.deepcopy(skill_items)]
tower_boss_dropping_p = []
for item_temp in tower_boss_dropping:
    tower_boss_dropping_p.append(100/item_temp.price)
#
# print(sum(tower_boss_dropping_p))
# print(sum(tower_monster_dropping_p))

# 圣灵洞穴掉落
god_fairy_land_dropping = [*copy.deepcopy(equip_items[7:]), *copy.deepcopy(skill_items)]
god_fairy_land_dropping_p = []
for item_temp in god_fairy_land_dropping:
    god_fairy_land_dropping_p.append(500/item_temp.price)


