from server.pojo.user import User
from server.service.rank import RankService
from server.util import filter_num, head, separate


def tower_rank(params: list, user: User) -> str:
    if len(params) < 1:
        page = 1
    else:
        try:
            page = int(params[0])
        except:
            return "指令错误"
        if page <= 0:
            return "指令错误"
    rank_list = RankService.get_tower_rank()
    offset = 10
    if not len(rank_list) % offset:
        total = len(rank_list) // offset
    else:
        total = len(rank_list) // offset + 1
    if page > total:
        return f"共{total}页，第{filter_num(page)}页不存在"
    res_content = ""
    for i in range((page - 1) * offset, min(page * offset, len(rank_list))):
        res_content += f"[{i + 1}] {rank_list[i]['name']}  第{rank_list[i]['tower_level']}层\n"
    return head("幻塔排名") + res_content + separate(
        f"第{page}页  共{total}页")