from server.pojo.user import User
from server.control.help import help_menu, adventure_menu, tower_menu, store_menu, forge_menu
from server.control.user import (user_info, user_update, user_id, user_attribute, user_attack, last_attack_record,
                                 change_name, user_bag, user_equip)
from server.control.tower import tower_info, tower_balance, tower_wipe, tower_wipe_delay, tower_attack
from server.control.item import see_item, use_normal_item, use_skill_item, use_equip_item, off_equip_item, sale_item
from server.control.store import see_store, buy_item
from server.control.blacksmith import strengthen_equip, strengthen_equip_true
command_mp = {
    "帮助菜单": help_menu,
    "帮助": help_menu,
    "冒险菜单": adventure_menu,
    "幻塔菜单": tower_menu,
    "商店菜单": store_menu,
    "铁匠铺菜单": forge_menu,
    "查看幻塔信息": tower_info,
    "我的信息": user_info,
    "我的装备": user_equip,
    "id": user_id,
    "升级": user_update,
    "我的属性": user_attribute,
    "切磋": user_attack,
    "查看战斗报告": last_attack_record,
    "幻塔结算": tower_balance,
    "幻塔扫荡": tower_wipe,
    "挑战幻塔首领": tower_attack,
    "改名": change_name,
    "查看商店": see_store,
    "我的背包": user_bag,
    "购买": buy_item,
    "查看": see_item,
    "使用": use_normal_item,
    "学习": use_skill_item,
    "装备": use_equip_item,
    "卸下": off_equip_item,
    "出售": sale_item,
    "强化": strengthen_equip,
    "确认强化": strengthen_equip_true
}

add_mp = {}
for command_k in command_mp.keys():
    add_mp["/" + command_k] = command_mp[command_k]

command_mp.update(add_mp)

need_delay_command = {"幻塔扫荡", "/幻塔扫荡"}


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
