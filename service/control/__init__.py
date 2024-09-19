from service.pojo.user import User
from service.control.help import help_menu, adventure_menu, tower_menu
from service.control.user import user_info, user_update, user_id, user_attribute, user_attack, last_attack_record
from service.control.tower import tower_info, tower_balance, tower_wipe, tower_wipe_delay, tower_attack

command_mp = {
    "主菜单": help_menu,
    "冒险菜单": adventure_menu,
    "幻塔菜单": tower_menu,
    "查看当层信息": tower_info,
    "我的信息": user_info,
    "id": user_id,
    "升级": user_update,
    "我的属性": user_attribute,
    "切磋": user_attack,
    "查看战斗报告": last_attack_record,
    "幻塔结算": tower_balance,
    "幻塔扫荡": tower_wipe,
    "挑战当层首领": tower_attack
}

add_mp = {}
for command_k in command_mp.keys():
    add_mp["/" + command_k] = command_mp[command_k]

command_mp.update(add_mp)

need_delay_command = {"幻塔扫荡"}


def main_control(command: str, params: list, user: User) -> (str, bool):
    if command not in command_mp:
        return "指令错误", False
    if command in need_delay_command:
        return command_mp[command](params, user), True
    return command_mp[command](params, user), False


delay_command_mp = {
    "tower_wipe": tower_wipe_delay
}


def delay_control(command: str, user: User) -> str:
    if command not in delay_command_mp:
        return "延迟指令错误"
    return delay_command_mp[command](user)
