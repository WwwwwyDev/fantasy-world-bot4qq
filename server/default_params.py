import time


def get_default_user(_id, name):
    return {"_id": _id,
            "name": name,
            "exp": 0,
            "level": 1,
            "coin": 0,
            "tower_level": 1,
            "blood": 500,
            "mana": 100,
            "exp_add_cnt": 0,
            "coin_add_cnt": 0,
            "head_equip": {"id": "", "name": ""},
            "body_equip": {"id": "", "name": ""},
            "pants_equip": {"id": "", "name": ""},
            "foot_equip": {"id": "", "name": ""},
            "weapon_equip": {"id": "", "name": ""},
            "talisman_equip": {"id": "", "name": ""},
            "head_level": 0,
            "body_level": 0,
            "pants_level": 0,
            "foot_level": 0,
            "weapon_level": 0,
            "talisman_level": 0,
            "skill": {"id": "", "name": ""},
            "bag": {"N11": 1},
            "last_tower_balance": int(time.time()),
            "last_bank_balance": int(time.time()),
            "bank_coin": 0,
            "bank_level": 0,
            "weapon_stone_fairyland": False,
            "coin_fairyland": False,
            "exp_fairyland": False,
            "god_fairyland": False
            }


class Tower:
    monster_name = ["蓝史莱姆", "红史莱姆", "哥布林", "石头人", "黄金史莱姆", "麒麟", "冰麒麟", "火麒麟", "金焱圣狮",
                    "冰焰魔狮", "狂暴火狮",
                    "双头狮虎兽", "嗜血狂狮", "碧睛狂狮", "碧眼火狮", "紫火魔狮", "双翼银狮", "冰雪白狮", "紫晶翼狮",
                    "风魔妖虎", "圣光虎", "剑齿虎", "暗月白虎", "赤炎虎", "幽冥白虎", "暴风虎", "黑暗翼虎", "刀角虎",
                    "烈焰焱虎", "铁甲爆炎虎", "疾风魔狼", "沙漠土狼", "血翎天狼", "暗黑魔狼", "冰霜巨狼", "啸月天狼",
                    "影月魔狼", "血月魔狼", "火域狂狼", "幽冥暗狼", "夜刃豹", "赤血雷豹", "双头猎豹", "雪斑黑豹",
                    "踏云魔豹", "风刃豹", "暗影豹", "幽冥豹", "赤豹", "火山云豹", "黑冥血炼豹", "狂暴魔熊", "铁背苍熊",
                    "狂暴魔熊", "冰雪暴熊", "炎魔熊", "狐熊", "大地冰熊", "赤金熊", "银环血鳞熊", "八银地熊",
                    "大地之熊", "烈焰土熊", "噬魂蚁王", "玄冰毒蚁", "烈血冰火蚕", "金丝蚕", "迅影斑斓豹", "风影豹",
                    "七翼暗金蝠", "魔音蝙蝠", "双翅紫尾貂", "紫尾貂", "深渊邪蛹", "堕落魔蛹", "九尾天狐",
                    "幽冥火狐", "不死雪狐", "极地冰狐", "八翼雷鹰"]
    exp_base = 200
    coin_base = 100
    tower_max = len(monster_name)


