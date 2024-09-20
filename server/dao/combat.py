from gv import Global


class CombatDao:

    @staticmethod
    def record_combat(combat_record: list, user_id: str):
        Global.combat_c.update_one({'_id': user_id}, {'$set': {"last_record": combat_record}}, upsert=True)

    @staticmethod
    def get_combat_record(user_id: str) -> dict | None:
        return Global.combat_c.find_one({'_id': user_id})