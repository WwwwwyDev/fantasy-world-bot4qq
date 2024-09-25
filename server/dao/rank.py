from gv import Global

class RankDao:

    @staticmethod
    def get_tower_rank() -> list[dict]:
        doc =  Global.cache_c.find_one({"name": "tower_rank"})
        if not doc:
            return []
        else:
            return doc["cache"]

if __name__ == "__main__":
    print(RankDao.get_tower_rank())