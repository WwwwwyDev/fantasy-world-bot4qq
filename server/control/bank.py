import time

from server import UserService
from server.pojo.user import User
from server.util import filter_num, head

bank_level_mp = ["普通会员", "白银会员", "黄金会员", "铂金会员", "钻石会员", "金钻会员", "黑钻会员", "璀璨会员", "至尊会员"]


def see_bank(params: list, user: User) -> str:
    hook_time, interest = count_interest(user)
    return head("幻行账户") + f"""[金币💰] {filter_num(user.bank_coin)}
[当前利息] {filter_num(interest)}
[会员等级] {bank_level_mp[user.bank_level]}
[一秒日化利率] {(0.00000039 + 0.00000005 * (user.bank_level + 1)) * 86400 * 100:.4f}%
[距离上一次利息结算时间] {filter_num(hook_time)}秒"""


def set_bank_coin(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误，请输入你需要存的金币数量"
    num = params[0]
    try:
        num = int(num)
    except:
        return "指令错误"
    hook_time, interest = count_interest(user)
    UserService.update_user(user.get_id(), {
        "$inc": {"coin": interest - num, "bank_coin": num, "last_bank_balance": hook_time}})
    return f"存入幻行账户{filter_num(num)}💰，并获得{filter_num(hook_time)}秒的利息{filter_num(interest)}💰"


def get_bank_coin(params: list, user: User) -> str:
    if len(params) < 1:
        return "指令错误，请输入你需要取的金币数量"
    num = params[0]
    try:
        num = int(num)
    except:
        return "指令错误"
    if num > user.bank_coin:
        return "你的幻行账户中没有那么多金币"
    hook_time, interest = count_interest(user)
    UserService.update_user(user.get_id(), {
        "$inc": {"coin": interest + num, "bank_coin": -num, "last_bank_balance": hook_time}})
    return f"从幻行账户中取出{filter_num(num)}💰，并获得{filter_num(hook_time)}秒的利息{filter_num(interest)}💰"


def get_bank_interest(params: list, user: User) -> str:
    hook_time, interest = count_interest(user)
    UserService.update_user(user.get_id(), {
        "$inc": {"coin": interest, "last_bank_balance": hook_time}})
    return f"时长{filter_num(hook_time)}秒，共获得利息{filter_num(interest)}💰"


def up_bank_level(params: list, user: User) -> str:
    if user.bank_level >= len(bank_level_mp) - 1:
        return "已达到最高会员等级"
    need_num = (user.bank_level + 1) * 2000000
    if need_num > user.coin:
        return f"你的金币不足，升级到{bank_level_mp[user.bank_level + 1]}所需{filter_num(need_num)}💰"
    UserService.update_user(user.get_id(), {
        "$inc": {"coin": -need_num, "bank_level": 1}})
    return f"升级到{bank_level_mp[user.bank_level + 1]}成功，共花费{filter_num(need_num)}💰"


def count_interest(user: User) -> (int, int):
    current_time = int(time.time())
    hook_time = current_time - user.last_bank_balance
    interest = int(min(user.bank_coin, 100000000) * hook_time * (0.00000039 + 0.00000005 * (user.bank_level + 1)))
    return hook_time, interest
