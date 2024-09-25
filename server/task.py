import time

from gv import Global
import  pymongo

def rank_task():
    docs = Global.user_c.find().sort('tower_level', pymongo.DESCENDING).limit(100)
    res = []
    for doc in docs:
        res.append({"name": doc["name"], "tower_level": doc["tower_level"]})
    Global.cache_c.update_one({'name': "tower_rank"}, {'$set': {"cache": res, "last_fresh_time": int(time.time())}}, upsert=True)
    print("幻塔排行榜刷新成功")


def every_day_task():
    Global.user_c.update_many({},{"$set":{"weapon_stone_fairyland": False, "coin_fairyland": False, "exp_fairyland": False, "god_fairyland": False}})
    print("每日秘境次数刷新成功")