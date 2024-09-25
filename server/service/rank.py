from server.dao.rank import RankDao


class RankService:

    @staticmethod
    def get_tower_rank() -> list[dict]:
        return RankDao.get_tower_rank()