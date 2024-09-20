class LFError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def get_msg(self) -> str:
        return self.msg
