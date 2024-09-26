from server.pojo.user import User
from server.util import head, separate


def get_menu_content(l):
    content = ""
    for i, e in enumerate(l):
        content += f"{[i + 1]} {e}\n"
    return content[:-1]

hm_l = ["冒险菜单 - 查看冒险常用功能", "幻塔菜单 - 挂机获取资源", "商店菜单 - 购买物品", "铁匠铺菜单 - 强化装备",
        "幻行菜单 - 存取金币","幻海菜单 - 挑战秘境，获取特定资源" , "幻殿菜单 - 排行榜", "新手帮助 - 新手攻略"]
HM = head("帮助菜单") + get_menu_content(hm_l)

am_l = ["我的信息 - 查看个人信息", "id - 查看冒险者id", "我的属性 - 查看个人属性", "我的装备 - 查看个人装备",
        "我的背包 1 - 查看个人背包的第1页",
        "查看 物品名字 - 查看物品信息",
        "金币 - 查看金币数量",
        "使用 消耗品名字+1 - 使用1个消耗品", "学习 技能名字 - 学习技能后，原有技能会被遗忘",
        "装备 装备名字 - 如果该部位已有装备，会自动换装",
        "卸下 装备名字 - 卸下该装备", "出售 物品名字+1 - 出售1个物品获取金币", "升级 - 消耗经验值升级等级",
        "切磋 冒险者名字 - 与别的冒险者友好切磋", "查看冒险者 冒险者名字 - 查看别的冒险者信息",
        "查看战斗报告 1 - 查看上一次的战斗记录的第1页", "改名 - 随机获得一个新的名字"]
AM = head("冒险菜单") + get_menu_content(am_l)

tm_l = ["幻塔结算 - 获得自上一次结算至今的战利品", "查看幻塔信息 - 查看当前层的幻塔信息", "幻塔扫荡 - 在当前层扫荡一次",
        "挑战幻塔首领 - 挑战当前层的首领"]
TM = head("幻塔菜单") + get_menu_content(tm_l) + separate("帮助") + "幻塔层数越高，所获得的资源越多，获得稀有物品的概率越高"

sm_l = ["查看商店 1 - 查看商店的第1页", "购买 物品名字+1 - 购买1个物品"]
SM = head("商店菜单") + get_menu_content(sm_l) + separate("帮助") + "只有在商店中的物品才能购买"

fm_l = ["强化 部位名字 - 消耗强化石对改部位进行强化"]
FM = head("铁匠铺菜单") + get_menu_content(fm_l) + separate("帮助") + "强化装备以获得装备属性提升"

bm_l = ["查看幻行 - 查看幻行账户信息", "幻行存金币 金币数量 - 存入幻行", "幻行取金币 金币数量 - 从幻行取出",
        "幻行结算 - 结算利息", "幻行会员升级 - 升级幻行会员以提升利率"]
BM = head("幻行菜单") + get_menu_content(bm_l) + separate("帮助") + "利息只结算1亿💰，超过1亿部分不结算"

sam_l = ["探索金币秘境 - 获取金币", "探索经验秘境 - 获取经验", "探索强化石秘境 - 获取强化石", "探索圣灵洞穴 - 掉落装备技能概率up"]
SAM = head("幻海菜单") + get_menu_content(sam_l) + separate("帮助") + "造成伤害越高，获得的资源越多\n每日只能探索一次，4点刷新"

rm_l = ["幻塔排名 1 - 查看幻塔排名的第1页"]
RM = head("幻殿菜单") + get_menu_content(rm_l) + separate("帮助") + "排行榜整点刷新"


NH = head("新手帮助") + """欢迎你来到幻想世界！幻想世界是一款挂机升级文字游戏。你需要在游戏内挑战各种怪物，来获取各种资源，提升自己的属性。
"""

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


def bank_menu(params: list, user: User) -> str:
    return BM

def sea_menu(params: list, user: User) -> str:
    return SAM

def rank_menu(params: list, user: User) -> str:
    return RM

def new_help(params: list, user: User) -> str:
    return NH

