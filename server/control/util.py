from server.pojo.user import User
from server.pojo.attack import UserCombatPojo, Attribute
from server.service.item import ItemService
from server.pojo.item import ItemEquip
from server.base_params import bs_rate

equip_mp = {
    "武器": "weapon_level",
    "头盔": "head_level",
    "上装": "body_level",
    "下装": "pants_level",
    "鞋子": "foot_level",
    "护符": "talisman_level",
}

equip_name_mp = {
    "weapon_equip": "武器",
    "head_equip": "头盔",
    "body_equip": "上装",
    "pants_equip": "下装",
    "foot_equip": "鞋子",
    "talisman_equip": "护符"
}

equip_level_mp = {
    "weapon_equip": "weapon_level",
    "head_equip": "head_level",
    "body_equip": "body_level",
    "pants_equip": "pants_level",
    "foot_equip": "foot_level",
    "talisman_equip": "talisman_level"
}


def get_user_attack_pojo(user: User) -> UserCombatPojo:
    attr = Attribute()
    for k, v in equip_level_mp.items():
        eq_id = user.mongo_dict[k]["id"]
        if not eq_id:
            continue
        eq_item: ItemEquip = ItemService.get_item_by_id(eq_id)
        if not eq_item:
            continue
        eq_level = user.mongo_dict[v]
        attr.blood_max += eq_item.add_status.blood_max + int(eq_level * eq_item.add_status.blood_max * bs_rate)
        attr.mana_max += eq_item.add_status.mana_max + int(eq_level * eq_item.add_status.mana_max * bs_rate)
        attr.attack += eq_item.add_status.attack + int(eq_level * eq_item.add_status.attack * bs_rate)
        attr.defense += eq_item.add_status.defense + int(eq_level * eq_item.add_status.defense * bs_rate)
        attr.critical_strike += eq_item.add_status.critical_strike
        attr.critical_damage += eq_item.add_status.critical_damage + eq_level * eq_item.add_status.critical_damage * bs_rate
        attr.defense_strike += eq_item.add_status.defense_strike
        attr.hurt_percentage_add += eq_item.add_status.hurt_percentage_add
        attr.attack_percentage_add += eq_item.add_status.attack_percentage_add
        attr.defense_percentage_add += eq_item.add_status.defense_percentage_add
        attr.speed += eq_item.add_status.speed
    on_attack = None
    if user.skill["id"]:
        sk_item = ItemService.get_item_by_id(user.skill["id"])
        if sk_item:
            on_attack = ItemService.get_item_by_id(user.skill["id"]).on_attack
    return UserCombatPojo(user.name, user.level, user.blood, user.mana, attr, on_attack)

