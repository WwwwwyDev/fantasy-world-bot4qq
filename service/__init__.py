from gv import Global
from pojo import User
def work_message(user_id: str, content: str):
    user = Global.user_db.find_one({"_id": user_id})
    print(user)
    print(type(user))
    if content == "开始冒险" and not user:
        Global.user_db.insert_one({"_id": user_id, })
    if not user:
        return "未在冒险者公会注册，输入\"开始冒险\"，注册成为冒险者"

if __name__ == '__main__':
    work_message("wwww","22")