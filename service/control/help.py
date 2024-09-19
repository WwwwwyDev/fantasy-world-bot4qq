from service.pojo.user import User
from service.util import head

HM = head("帮助菜单") + "1、冒险菜单\n2、幻想之塔菜单"
AM = head("冒险菜单") + (
    "1、我的信息 - 查看个人信息\n2、我的属性 - 查看个人属性\n3、id - 查看冒险者id\n4、升级 - 消耗经验值升级等级\n5、切磋 xx - 与xx友好切磋\n"
    "6、查看战斗报告 1 - 查看上一次的战斗记录的第1页")
TM = head("幻塔菜单") + "1、幻塔结算 - 获得自上一次结算至今的战利品\n2、查看当层信息\n3、幻塔扫荡 - 在当前层扫荡一次\n4、挑战当层首领"


def help_menu(params: list, user: User) -> str:
    return HM


def adventure_menu(params: list, user: User) -> str:
    return AM


def tower_menu(params: list, user: User) -> str:
    return TM
