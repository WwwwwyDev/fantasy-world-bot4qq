from server.dao.item import items_mp_by_name, items_mp_by_id, store_items, store_items_mp_by_name, \
    tower_monster_dropping, tower_monster_dropping_p, equip_dropping, equip_dropping_p
from server.pojo.item import Item, ItemNormal, ItemEquip, ItemSkill, ItemSpecial


class ItemService:

    @staticmethod
    def get_item_by_id(item_id) -> Item | ItemNormal | ItemEquip | ItemSkill | ItemSpecial | None:
        if item_id not in items_mp_by_id:
            return None
        return items_mp_by_id[item_id]

    @staticmethod
    def get_item_by_name(item_name) -> Item | ItemNormal | ItemEquip | ItemSkill | ItemSpecial | None:
        if item_name not in items_mp_by_name:
            return None
        return items_mp_by_name[item_name]

    @staticmethod
    def get_store_list() -> list[Item]:
        return store_items

    @staticmethod
    def get_store_item_by_name(item_name) -> Item | ItemNormal | ItemEquip | ItemSkill | ItemSpecial | None:
        if item_name not in store_items_mp_by_name:
            return None
        return store_items_mp_by_name[item_name]

    @staticmethod
    def get_tower_monster_dropping_items_list() -> (list[Item], list[float]):
        return tower_monster_dropping, tower_monster_dropping_p

    @staticmethod
    def get_equip_dropping_items_list() -> (list[Item], list[float]):
        return equip_dropping, equip_dropping_p

