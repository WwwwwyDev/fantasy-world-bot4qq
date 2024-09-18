from gv import  Global
import botpy
from botpy import logging
from botpy.message import GroupMessage
from botpy.manage import GroupManageEvent

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
        user_id = message.author.member_openid
        content = message.content
        await self.api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0,
              msg_id=message.id,
              content="22")


if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = FLClient(intents=intents)
    client.run(appid=str(config["appid"]), secret=str(config["secret"]))
