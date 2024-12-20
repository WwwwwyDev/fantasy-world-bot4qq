from botpy.ext.cog_yaml import read
import os
import pymongo


class Global:
    config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
    mongo_client = pymongo.MongoClient(
        f"mongodb://{config['mongodb']['user']}:{config['mongodb']['password']}@{config['mongodb']['host']}:{config['mongodb']['port']}/{config['mongodb']['database']}")
    mongo_db = mongo_client[config['mongodb']['database']]
    user_c = mongo_db["user"]
    combat_c = mongo_db["combat"]
    cache_c = mongo_db["cache"]


if __name__ == "__main__":
    db = Global.mongo_client["tl-botqq"]
    c = db["test"]
