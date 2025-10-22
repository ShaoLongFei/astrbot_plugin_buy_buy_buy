from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger


@register("buy_buy_buy", "LiuYue", "购物群惊喜价监控插件", "0.0.1")
class BuyBuyBuy(Star):
    master_id = '1371712979'
    monitored_groups = ['117074747', '1074207600']
    register_session_map = {}

    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.on_astrbot_loaded()
    async def on_astrbot_loaded(self):
        print("购物群惊喜价监控插件 加载成功~")

    @filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)
    async def on_private_message(self, event: AstrMessageEvent):
        message_str = event.message_str
        yield event.plain_result(f"收到了一条私聊消息。 {message_str}")

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        if event.get_group_id() in self.monitored_groups:
            message_str = event.message_str
            logger.info(f"{event.get_sender_name()}，{message_str}")

    @filter.command("register")
    async def register(self, event:AstrMessageEvent):
        self.register_session_map[event.unified_msg_origin] = []
        yield event.plain_result(f"{event.get_sender_name()}，您已注册成功~")

    @filter.command("add_keyword")
    async def add_keyword(self, event: AstrMessageEvent):
        logger.info(f"add_keyword 接收到，{event.get_message_str()}")
        list_keyword = event.get_message_str().split(" ")
        if len(list_keyword) < 2:
            logger.error("add_keyword 格式不对")
            return
        keyword = event.get_message_str().split(" ")[1]
        self.register_session_map[event.unified_msg_origin].append(keyword)
        yield event.plain_result(f"已为您添加关键词 {keyword}，当前的关键词列表为 {self.register_session_map[event.unified_msg_origin]}")

    @filter.command("list_keywords")
    async def list_keywords(self, event: AstrMessageEvent):
        """查询当前监控的关键词"""
        if not self.register_session_map.keys().__contains__(event.unified_msg_origin):
            event.plain_result("当前用户还未注册")
            return
        yield event.plain_result(f"当前的关键词列表 {self.register_session_map[event.unified_msg_origin]}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
