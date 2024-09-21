from server.pojo.user import User
from server.service.user import UserService
from server.control import main_control, delay_control
from server.control.help import help_menu

async def work_message(user_id: str, content: str) -> (str, bool):
    user = UserService.get_user_by_id_with_up(user_id)
    if content == "开始冒险" and not user:
        name = UserService.register(user_id)
        return f"恭喜{name}成为冒险者", False
    if content == "开始冒险" and user:
        return "你已经是冒险者了", False
    if not user:
        return "未在冒险者公会注册，输入\"开始冒险\"，注册成为冒险者", False
    if not content:
        return help_menu([], user), False
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
    user = UserService.get_user_by_id_with_up(user_id)
    return delay_control(command, user)


if __name__ == '__main__':
    work_message("wwww", "22")
