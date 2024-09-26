from server.pojo.user import User
from server.control.help import help_menu, adventure_menu, tower_menu, store_menu, forge_menu, bank_menu, rank_menu, sea_menu, new_help
from server.control.user import (user_info, user_update, user_id, user_attribute, user_attack, last_attack_record,
                                 change_name, user_bag, user_equip, see_other_user_info, see_coin)
from server.control.tower import tower_info, tower_balance, tower_wipe, tower_wipe_delay, tower_attack
from server.control.item import see_item, use_normal_item, use_skill_item, use_equip_item, off_equip_item, sale_item
from server.control.store import see_store, buy_item
from server.control.blacksmith import strengthen_equip
from server.control.bank import see_bank, set_bank_coin, get_bank_coin, get_bank_interest, up_bank_level
from server.control.rank import tower_rank
from server.control.sea import coin_fairy_land, exp_fairy_land, weapon_stone_fairy_land, god_fairy_land

command_mp = {
    "帮助菜单": help_menu,
    "帮助": help_menu,
    "冒险菜单": adventure_menu,
    "幻塔菜单": tower_menu,
    "商店菜单": store_menu,
    "铁匠铺菜单": forge_menu,
    "幻行菜单": bank_menu,
    "幻海菜单": sea_menu,
    "幻殿菜单": rank_menu,
    "新手帮助": new_help,
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
    "查看冒险者": see_other_user_info,
    "金币": see_coin,
    "查看幻行": see_bank,
    "幻行存金币": set_bank_coin,
    "幻行取金币": get_bank_coin,
    "幻行结算": get_bank_interest,
    "幻行会员升级": up_bank_level,
    "幻塔排名": tower_rank,
    "探索金币秘境": coin_fairy_land,
    "探索经验秘境": exp_fairy_land,
    "探索强化石秘境": weapon_stone_fairy_land,
    "探索圣灵洞穴": god_fairy_land
}

add_mp = {}
sorted_command = []
for command_k in command_mp.keys():
    add_mp["/" + command_k] = command_mp[command_k]
    sorted_command.append(command_k)
    sorted_command.append("/" + command_k)

command_mp.update(add_mp)

sorted_command = sorted(sorted_command, key=lambda string: len(string), reverse=True)

need_delay_command = {"幻塔扫荡", "/幻塔扫荡"}


def main_control(command: str, params: list, user: User) -> (str, bool):
    if command not in command_mp:
        f = False
        for e in sorted_command:
            if command.startswith(e):
                params.insert(0, command[len(e):])
                command = e
                f = True
                break
        if not f:
            return "没有该指令，请查看帮助菜单", False
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
