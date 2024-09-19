from service.pojo.user import User
from service.util import head

def help_menu(params: list, user: User) -> str:
    return head("帮助菜单") + "1、冒险菜单\n2、幻想之塔菜单"

def adventure_menu(params: list, user: User) -> str:
    return head("冒险菜单") + "1、我的信息 - 查看个人信息\n2、我的属性 - 查看个人属性\n3、升级 - 消耗经验值升级等级\n"

def tower_menu(params: list, user: User) -> str:
    return head("幻想之塔菜单") + "1、挂机\n2、结束挂机\n3、查看当前层信息"