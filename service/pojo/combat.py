from service.base_params import StatusBase
from service.default_params import Tower
from service.pojo.user import User
import random
from service.util import make_decision
from gv import Global


class CombatPojo:

    def __init__(self):
        self.name = ""
        self.current_blood = 0
        self.blood_max = 0
        self.current_mana = 0
        self.mana_max = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.critical_strike = 0
        self.critical_damage = 0
        self.exp_add = 0


class TowerMonsterCombatPojo(CombatPojo):

    def __init__(self, tower_level: int):
        super().__init__()
        self.name = Tower.monster_name[(tower_level - 1) % Tower.tower_max]
        self.current_blood = int(tower_level * StatusBase.blood_base * 1.5)
        self.blood_max = self.current_blood
        self.current_mana = int(tower_level * StatusBase.mono_base * 1.5)
        self.mana_max = self.current_mana
        self.attack = int(StatusBase.attack_base * tower_level * 1.2)
        self.defense = int(StatusBase.defense_base * tower_level * 1.2)
        self.speed = StatusBase.speed_base + tower_level // 1000
        self.critical_strike = min(StatusBase.critical_strike_base + tower_level / 15000, 1)
        self.critical_damage = StatusBase.critical_damage_base + tower_level / 10000
        self.exp_add = -1


class UserCombatPojo(CombatPojo):

    def __init__(self, user: User):
        super().__init__()
        self.name = user.name
        self.current_blood = user.blood
        self.blood_max = StatusBase.blood_base * user.level
        self.current_mana = user.mana
        self.mana_max = StatusBase.mono_base * user.level
        self.attack = StatusBase.attack_base * user.level
        self.defense = StatusBase.defense_base * user.level
        self.speed = StatusBase.speed_base
        self.critical_strike = StatusBase.critical_strike_base
        self.critical_damage = StatusBase.critical_damage_base
        self.exp_add = StatusBase.exp_add_base


class CombatDao:

    @staticmethod
    def record_combat(combat_record: list, user_id: str):
        Global.combat_c.update_one({'_id': user_id}, {'$set': {"last_record": combat_record}}, upsert=True)

    @staticmethod
    def get_combat_record(user_id: str) -> dict | None:
        return Global.combat_c.find_one({'_id': user_id})


def attack_one(pojo_proactive: CombatPojo, pojo_reactive: CombatPojo) -> str:
    base_attack = max(pojo_proactive.attack - pojo_reactive.defense, 1) * random.uniform(1.1, 1.2)
    is_critical = make_decision(pojo_proactive.critical_strike)
    if is_critical:
        base_attack = (1 + pojo_proactive.critical_damage) * base_attack
    base_attack = int(base_attack)
    pojo_reactive.current_blood -= base_attack
    if pojo_reactive.current_blood < 0:
        pojo_reactive.current_blood = 0
    content = f"{pojo_proactive.name}发动普通攻击，对{pojo_reactive.name}造成{base_attack}点伤害"
    return content


def attack(pojo1: CombatPojo, pojo2: CombatPojo, user_id: str) -> (bool, str, str):
    max_attack = 20
    current_attack = 1
    record_content_list = []
    speed1 = pojo1.speed
    speed2 = pojo2.speed
    while pojo1.current_blood > 0 and pojo2.current_blood > 0 and max_attack:
        add_content = ""
        if pojo1.speed > pojo2.speed:
            add_content += f"{attack_one(pojo1, pojo2)}"
            pojo1.speed -= speed2
        elif pojo2.speed > pojo1.speed:
            add_content += f"{attack_one(pojo2, pojo1)}"
            pojo2.speed -= speed1
        else:
            if make_decision(0.5):
                add_content += f"{attack_one(pojo1, pojo2)}"
                pojo1.speed -= speed2
            else:
                add_content += f"{attack_one(pojo2, pojo1)}"
                pojo2.speed -= speed1
        if pojo1.speed < 0:
            pojo1.speed = speed1
        if pojo2.speed < 0:
            pojo2.speed = speed2
        if pojo2.speed == 0 and pojo1.speed == 0:
            pojo1.speed = speed1
            pojo2.speed = speed2
        add_content += f"\n{pojo1.name}:{pojo1.current_blood}🩸，{pojo2.name}:{pojo2.current_blood}🩸"
        record_content_list.append(add_content)
        max_attack -= 1
        current_attack += 1
    res_content = ""
    for idx, content in enumerate(record_content_list[0:5]):
        res_content += f"[{idx + 1}]{content}\n"
    if len(record_content_list) > 5:
        res_content += "......\n💡输入指令“查看战斗报告”获取完整报告"
    attack_result = ""
    is_win = False
    if max_attack == 0:
        attack_result = "你们战斗到天荒地老也没有分出结果"
    if pojo1.current_blood <= 0:
        attack_result = f"{pojo2.name}获胜!"
    if pojo2.current_blood <= 0:
        attack_result = f"{pojo1.name}获胜!"
        is_win = True
    record_content_list.append(attack_result)
    CombatDao.record_combat(record_content_list, user_id)
    return is_win, res_content, attack_result


def get_attribute_content(attribute: CombatPojo):
    base = f"""[血量] {attribute.current_blood} / {attribute.blood_max}
[魔力] {attribute.current_mana} / {attribute.mana_max}
[攻击] {attribute.attack}
[防御] {attribute.defense}
[速度] {attribute.speed}
[暴击率] {attribute.critical_strike * 100:.1f}%
[暴击伤害] {attribute.critical_damage * 100:.1f}%
"""
    if attribute.exp_add != -1:
        base = base + f"[经验加成] {attribute.exp_add * 100}%"
    return base
