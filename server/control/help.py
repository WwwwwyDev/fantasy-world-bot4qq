from server.pojo.user import User
from server.util import head

hm_l = ["冒险菜单","幻塔菜单","商店菜单", "铁匠铺菜单"]
HM = head("帮助菜单")
for i, e in enumerate(hm_l):
    HM += f"{[i+1]} {e}\n"
am_l = ["我的信息 - 查看个人信息", "我的属性 - 查看个人属性","我的背包 1 - 查看个人背包的第1页","id - 查看冒险者id", "升级 - 消耗经验值升级等级", "切磋 xx - 与xx友好切磋"
    "查看战斗报告 1 - 查看上一次的战斗记录的第1页","改名 - 随机获得一个新的名字"]
AM = head("冒险菜单")
for i, e in enumerate(am_l):
    AM += f"{[i+1]} {e}\n"
tm_l = ["幻塔结算 - 获得自上一次结算至今的战利品", "查看当层信息", "幻塔扫荡 - 在当前层扫荡一次", "挑战当层首领"]
TM = head("幻塔菜单")
for i, e in enumerate(tm_l):
    TM += f"{[i+1]} {e}\n"
sm_l = ["查看商店 1 - 查看商店的第1页", "购买 物品名字"]
SM = head("商店菜单")
for i, e in enumerate(sm_l):
    SM += f"{[i+1]} {e}\n"
fm_l = ["强化 部位名字"]
FM = head("商店菜单")
for i, e in enumerate(fm_l):
    FM += f"{[i]} {e}\n"

def help_menu(params: list, user: User) -> str:
    return HM


def adventure_menu(params: list, user: User) -> str:
    return AM


def tower_menu(params: list, user: User) -> str:
    return TM

def store_menu(params: list, user: User) -> str:
    return SM

def forge_menu(params: list, user: User) -> str:
    return FM