from service.pojo import User, UserDao
from service.error import LFError
from service.control import main_control, delay_control


async def work_message(user_id: str, content: str) -> (str, bool):
    user = UserDao.get_user_by_id(user_id)
    if content == "开始冒险" and not user:
        name = UserDao.register(user_id)
        return f"恭喜{name}成为冒险者", False
    if content == "开始冒险" and user:
        return "你已经是冒险者了", False
    if not user:
        return "未在冒险者公会注册，输入\"开始冒险\"，注册成为冒险者", False
    content_list = content.split(" ")
    if len(content_list) == 0:
        return "指令错误", False
    command = content_list[0]
    if len(content_list) == 1:
        params = []
    else:
        params = content_list[1:]
    return main_control(command, params, user)


async def work_delay_command(command: str, user_id: str) -> str:
    user = UserDao.get_user_by_id(user_id)
    return delay_control(command, user)


if __name__ == '__main__':
    work_message("wwww", "22")
