import math

from server.pojo.user import User
from server.control.util import get_user_attack_pojo
from server.pojo.attack import SeaMonsterCombatPojo
from server.service.combat import CombatService
from server.service.user import UserService
from server.util import filter_num

def coin_fairy_land(params: list, user: User) -> str:
    if user.coin_fairyland:
        return "你今天已经探索过金币秘境了"
    sea_monster_pojo = SeaMonsterCombatPojo("金钱鼠", 1)
    user_pojo = get_user_attack_pojo(user)
    user_pojo.current_blood = user_pojo.blood_max
    user_pojo.current_mana = user_pojo.mana_max
    _, _, _, total_attack = CombatService.attack(user_pojo, sea_monster_pojo)
    get_coin = int(max(((user.coin_add_cnt/100 + 1) * total_attack) // 50, 100))
    UserService.update_user(user.get_id(), {"$set": {"coin_fairyland": True},"$inc":{"coin": get_coin}})
    return f"在秘境中，遇到了{sea_monster_pojo.name}，随即开始进行战斗，最终对其共造成了{filter_num(total_attack)}点伤害，获得了{filter_num(get_coin)}个金币"

def exp_fairy_land(params: list, user: User) -> str:
    if user.exp_fairyland:
        return "你今天已经探索过经验秘境了"
    sea_monster_pojo = SeaMonsterCombatPojo("经验球集合体", 1)
    user_pojo = get_user_attack_pojo(user)
    user_pojo.current_blood = user_pojo.blood_max
    user_pojo.current_mana = user_pojo.mana_max
    _, _, _, total_attack = CombatService.attack(user_pojo, sea_monster_pojo)
    get_exp = int(max(((user.exp_add_cnt/100 + 1) * total_attack) // 50, 100))
    UserService.update_user(user.get_id(), {"$set": {"exp_fairyland": True},"$inc":{"exp": get_exp}})
    return f"在秘境中，遇到了{sea_monster_pojo.name}，随即开始进行战斗，最终对其共造成了{filter_num(total_attack)}点伤害，获得了{filter_num(get_exp)}点经验"

def weapon_stone_fairy_land(params: list, user: User) -> str:
    if user.weapon_stone_fairyland:
        return "你今天已经探索过强化石秘境了"
    sea_monster_pojo = SeaMonsterCombatPojo("所罗门的叹息", 1)
    user_pojo = get_user_attack_pojo(user)
    user_pojo.current_blood = user_pojo.blood_max
    user_pojo.current_mana = user_pojo.mana_max
    _, _, _, total_attack = CombatService.attack(user_pojo, sea_monster_pojo)
    get_stone = math.ceil(total_attack / 50000)
    if "SP1" in user.bag:
        user.bag["SP1"] += get_stone
    else:
        user.bag["SP1"] = get_stone
    UserService.update_user(user.get_id(), {"$set": {"weapon_stone_fairyland": True, "bag": user.bag}})
    return f"在秘境中，遇到了{sea_monster_pojo.name}，随即开始进行战斗，最终对其共造成了{filter_num(total_attack)}点伤害，获得了{get_stone}个强化石"

# def coin_fairy_land(params: list, user: User) -> str:
#     if user.coin_fairyland:
#         return "你今天已经探索过金币秘境了"
#     sea_monster_pojo = SeaMonsterCombatPojo("金钱鼠", 1)
#     user_pojo = get_user_attack_pojo(user)
#     user_pojo.current_blood = user_pojo.blood_max
#     user_pojo.current_mana = user_pojo.mana_max
#     _, _, _, total_attack = CombatService.attack(user_pojo, sea_monster_pojo)
#     get_coin = total_attack // 50
#     UserService.update_user(user.get_id(), {"$set": {"coin_fairyland": True},"$inc":{"coin": get_coin}})
#     return f"在秘境中，遇到了{sea_monster_pojo.name}，随即开始进行战斗，最终对其共造成了{filter_num(total_attack)}点伤害，获得了{filter_num(get_coin)}个金币"