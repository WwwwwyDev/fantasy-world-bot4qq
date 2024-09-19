from service.pojo.user import User
from service.control.help import help_menu, adventure_menu, tower_menu
from service.control.user import user_info, user_update, user_id, user_attribute
from service.control.tower import tower_info
command_mp = {
    "帮助菜单": help_menu,
    "冒险菜单": adventure_menu,
    "幻想之塔菜单": tower_menu,
    "查看当前层信息": tower_info,
    "我的信息": user_info,
    "id": user_id,
    "升级": user_update,
    "我的属性": user_attribute
}


def main_control(command: str, params: list, user: User) -> str:
    if command not in command_mp:
        return "指令错误"
    return command_mp[command](params, user)
