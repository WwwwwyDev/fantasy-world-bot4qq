import random

from server.dao.combat import CombatDao
from server.pojo.combat import CombatPojo
from server.util import make_decision


class CombatService:
    @staticmethod
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

    @staticmethod
    def attack(pojo1: CombatPojo, pojo2: CombatPojo, user_id: str) -> (bool, str, str):
        max_attack = 30
        current_attack = 1
        record_content_list = []
        speed1 = pojo1.speed
        speed2 = pojo2.speed
        while pojo1.current_blood > 0 and pojo2.current_blood > 0 and max_attack:
            add_content = ""
            if pojo1.speed > pojo2.speed:
                add_content += f"{CombatService.attack_one(pojo1, pojo2)}"
                pojo1.speed -= speed2
            elif pojo2.speed > pojo1.speed:
                add_content += f"{CombatService.attack_one(pojo2, pojo1)}"
                pojo2.speed -= speed1
            else:
                if make_decision(0.5):
                    add_content += f"{CombatService.attack_one(pojo1, pojo2)}"
                    pojo1.speed -= speed2
                else:
                    add_content += f"{CombatService.attack_one(pojo2, pojo1)}"
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
            attack_result = "30回合内未分出胜负"
        if pojo1.current_blood <= 0:
            attack_result = f"{pojo2.name}获胜!"
        if pojo2.current_blood <= 0:
            attack_result = f"{pojo1.name}获胜!"
            is_win = True
        record_content_list.append(attack_result)
        CombatDao.record_combat(record_content_list, user_id)
        return is_win, res_content, attack_result

    @staticmethod
    def get_attribute_content(attribute: CombatPojo):
        return f"""[血量] {attribute.current_blood} / {attribute.blood_max}
[魔力] {attribute.current_mana} / {attribute.mana_max}
[攻击] {attribute.attack}
[防御] {attribute.defense}
[速度] {attribute.speed}
[暴击率] {attribute.critical_strike * 100:.1f}%
[暴击伤害] {attribute.critical_damage * 100:.1f}%"""

    @staticmethod
    def get_combat_record(user_id: str) -> dict | None:
        return CombatDao.get_combat_record(user_id)
