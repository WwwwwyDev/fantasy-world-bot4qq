from service.pojo.user import User
from service.control.help import help_menu
from service.control.user import user_info, user_update

command_mp = {
    "帮助": help_menu,
    "冒险帮助": help_menu,
    "冒险菜单": help_menu,
    "菜单": help_menu,
    "个人信息": user_info,
    "我的信息": user_info,
    "升级": user_update
}


def main_control(command: str, params: list, user: User) -> str:
    if command not in command_mp:
        return "指令错误"
    return command_mp[command](params, user)
