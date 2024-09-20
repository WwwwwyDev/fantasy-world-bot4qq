max_exp_base = 1000  # 下一级所需经验值
bs_rate = 0.2  # 强化基准加成倍率

class StatusBase:
    blood_base = 500  # 血量
    mono_base = 100  # 魔力
    attack_base = 50  # 攻击力
    defense_base = 30  # 攻击力
    critical_strike_base = 0.1  # 暴击率
    critical_damage_base = 0.2  # 暴击伤害
    speed_base = 10  # 速度


UserStatus = ["正在扫荡中"]
