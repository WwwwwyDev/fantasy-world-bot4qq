import time
import threading
from botpy.types.message import Ark, ArkKv
import schedule

from gv import Global
import botpy
from botpy import logging
from botpy.message import GroupMessage
from botpy.manage import GroupManageEvent
from server import work_message, work_delay_command
from server.task import rank_task, every_day_task
import asyncio

from server.error import LFError


_log = logging.get_logger()
config = Global.config

async def work(message: GroupMessage):
    user_id = message.author.member_openid
    content = message.content.strip()
    try:
        resp, is_need_delay = await work_message(user_id=user_id, content=content)
    except LFError:
        resp = "后台异常"
        is_need_delay = False
    delay_time = 0
    delay_command = ""
    if is_need_delay:
        current_content, delay_time, delay_command = resp.split("|")
    else:
        current_content = resp
    await message._api.post_group_message(
        group_openid=message.group_openid,
        msg_type=0,
        msg_id=message.id,
        content=current_content)
    if is_need_delay:
        await asyncio.sleep(int(delay_time))
        delay_content = await work_delay_command(delay_command, user_id)
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            msg_seq=2,
            content=delay_content)

class FLClient(botpy.Client):

    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_add_robot(self, event: GroupManageEvent):
        await self.api.post_group_message(
            group_openid=event.group_openid,
            msg_type=0,
            event_id=event.event_id,
            content=f"""欢迎来到幻想世界！🌟
亲爱的冒险者们，欢迎你们踏入这片充满奇迹与梦幻的土地！✨ 在这里，你可以尽情释放你的想象力，探索无尽的奇妙领域，与各种神秘生物相遇，展开一场场惊心动魄的冒险！💪""",
        )

    async def on_group_at_message_create(self, message: GroupMessage):
        # payload: Ark = Ark(
        #     template_id=24,
        #     kv=[
        #         ArkKv(key="#DESC#", value="通知提醒"),
        #         ArkKv(key="#PROMPT#", value="标题"),
        #         ArkKv(key="#TITLE#", value="标题"),
        #     ],
        # )
        # a = await self.api.post_group_message(
        #     group_openid=message.group_openid,
        #     msg_type=3,
        #     ark=payload,)
        await work(message)

def schedule_work():
    schedule.clear()
    schedule.every().hour.at(":00").do(rank_task)
    schedule.every().day.at("04:00").do(every_day_task)
    # schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_schedule_thread():
    job_thread = threading.Thread(target=schedule_work)
    job_thread.daemon = True
    job_thread.start()

if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = FLClient(intents=intents)
    run_schedule_thread()
    client.run(appid=str(config["appid"]), secret=str(config["secret"]))
