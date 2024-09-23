from gv import Global
import botpy
from botpy import logging
from botpy.message import GroupMessage
from botpy.manage import GroupManageEvent
from server import work_message, work_delay_command
import asyncio

from server.error import LFError

_log = logging.get_logger()
config = Global.config


class FLClient(botpy.Client):

    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_add_robot(self, event: GroupManageEvent):
        await self.api.post_group_message(
            group_openid=event.group_openid,
            msg_type=0,
            event_id=event.event_id,
            content=f"robot 「{self.robot.name}」 on_ready!",
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
        #     msg_seq=1,
        #     ark=payload,)
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
        await self.api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=current_content)
        if is_need_delay:
            await asyncio.sleep(int(delay_time))
            delay_content = await work_delay_command(delay_command, user_id)
            await self.api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                msg_seq=2,
                content=delay_content)


if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = FLClient(intents=intents, is_sandbox=True)
    client.run(appid=str(config["appid"]), secret=str(config["secret"]))
