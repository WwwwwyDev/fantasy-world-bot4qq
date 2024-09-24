from server.pojo.user import User
from server.util import head, separate

hm_l = ["冒险菜单 - 查看冒险相关指令", "幻塔菜单 - 挂机获取资源", "商店菜单 - 购买物品", "铁匠铺菜单 - 强化装备",
        "幻庄菜单 - 存取金币"]
HM = head("帮助菜单")
for i, e in enumerate(hm_l):
    HM += f"{[i + 1]} {e}\n"
HM = HM[:-1]

am_l = ["我的信息 - 查看个人信息", "id - 查看冒险者id", "我的属性 - 查看个人属性", "我的装备 - 查看个人装备",
        "我的背包 1 - 查看个人背包的第1页",
        "查看 物品名字 - 查看物品信息",
        "使用 消耗品名字+1 - 使用1个消耗品", "学习 技能名字 - 学习技能后，原有技能会被遗忘",
        "装备 装备名字 - 如果该部位已有装备，会自动换装",
        "卸下 装备名字 - 卸下该装备", "出售 物品名字+1 - 出售1个物品获取金币", "升级 - 消耗经验值升级等级", "切磋 冒险者名字 - 与xx友好切磋",
        "查看战斗报告 1 - 查看上一次的战斗记录的第1页", "改名 - 随机获得一个新的名字"]
AM = head("冒险菜单")
for i, e in enumerate(am_l):
    AM += f"{[i + 1]} {e}\n"
AM = AM[:-1]

tm_l = ["幻塔结算 - 获得自上一次结算至今的战利品", "查看幻塔信息 - 查看当前层的幻塔信息", "幻塔扫荡 - 在当前层扫荡一次",
        "挑战幻塔首领 - 挑战当前层的首领"]
TM = head("幻塔菜单")
for i, e in enumerate(tm_l):
    TM += f"{[i + 1]} {e}\n"
TM = TM[:-1]

sm_l = ["查看商店 1 - 查看商店的第1页", "购买 物品名字+1 - 购买1个物品"]
SM = head("商店菜单")
for i, e in enumerate(sm_l):
    SM += f"{[i + 1]} {e}\n"
SM = SM[:-1]

fm_l = ["强化 部位名字 - 消耗强化石对改部位进行强化"]
FM = head("铁匠铺菜单")
for i, e in enumerate(fm_l):
    FM += f"{[i + 1]} {e}\n"
FM = FM[:-1]

bm_l = ["查看幻庄 - 查看幻庄账户信息", "幻庄存金币 金币数量 - 存入幻庄", "幻庄取金币 金币数量 - 从幻庄取出", "幻庄结算 - 结算利息", "幻庄会员升级 - 升级幻庄会员以提升利率"]
BM = head("幻庄菜单")
for i, e in enumerate(bm_l):
    BM += f"{[i + 1]} {e}\n"
BM = BM[:-1]

def help_menu(params: list, user: User) -> str:
    return HM


def adventure_menu(params: list, user: User) -> str:
    return AM


def tower_menu(params: list, user: User) -> str:
    return TM  + separate("帮助") + "幻塔层数越高，所获得的资源越多\n挑战首领有概率获得装备"


def store_menu(params: list, user: User) -> str:
    return SM + separate("帮助") + "只有在商店中的物品才能购买"


def forge_menu(params: list, user: User) -> str:
    return FM + separate("帮助") + "强化装备以获得装备属性提升"


def bank_menu(params: list, user: User) -> str:
    return BM + separate("帮助") + "利息只结算1亿💰，超过1亿部分不结算"
