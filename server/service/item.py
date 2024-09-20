from server.dao.item import items_mp_by_name, items_mp_by_id, store_items, store_items_mp_by_name
from server.pojo.item import Item
class ItemService:

    @staticmethod
    def get_item_by_id(item_id) -> Item | None:
        if item_id not in items_mp_by_id:
            return None
        return items_mp_by_id[item_id]

    @staticmethod
    def get_item_by_name(item_name) -> Item | None:
        if item_name not in items_mp_by_name:
            return None
        return items_mp_by_name[item_name]

    @staticmethod
    def get_store_list() -> list[Item]:
        return store_items

    @staticmethod
    def get_store_item_by_name(item_name) -> Item | None:
        if item_name not in store_items_mp_by_name:
            return None
        return store_items_mp_by_name[item_name]
