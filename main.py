from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random

# 美食/饮品候选列表（可自行扩展）
FOOD_LIST = [
    "火锅", "烤肉", "寿司", "麻辣烫", "炸鸡", "螺蛳粉",
    "牛肉面", "披萨", "饺子", "汉堡", "盖浇饭", "酸菜鱼"
]
DRINK_LIST = [
    "奶茶", "咖啡", "可乐", "果汁", "柠檬水", "气泡水",
    "茶", "酸奶", "椰汁", "奶昔", "果茶", "苏打水"
]

@register(
    "astrbot_plugin_eat-drink", 
    "Cybercat",
    "随机推荐吃什么、喝什么，选择困难症救星～", 
    "1.0.0",
    "https://github.com/Newbie-L/astrbot_plugin_eat-drink"
)
class RandomFoodDrinkPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        logger.info("随机推荐插件初始化完成～")

    # 推荐吃的指令
    @filter.command("吃什么", alias={"推荐吃的", "随机吃"})
    async def recommend_food(self, event: AstrMessageEvent):
        '''发送 /吃什么 随机获取美食建议'''
        random_food = random.choice(FOOD_LIST)
        logger.info(f"为用户 {event.get_sender_name()} 推荐美食：{random_food}")
        yield event.plain_result(f"🍚 推荐你吃：{random_food}\n（发送 /吃什么 可重新随机）")

    # 推荐喝的指令
    @filter.command("喝什么", alias={"推荐喝的", "随机喝"})
    async def recommend_drink(self, event: AstrMessageEvent):
        '''发送 /什么 随机获取饮品建议'''
        random_drink = random.choice(DRINK_LIST)
        logger.info(f"为用户 {event.get_sender_name()} 推荐饮品：{random_drink}")
        yield event.plain_result(f"🥤 推荐你喝：{random_drink}\n（发送 /推什么 可重新随机）")

    # 合并指令（可选，支持 /推荐 吃的/喝的 格式）
    @filter.command("推荐")
    async def recommend_all(self, event: AstrMessageEvent, type_str: str):
        '''发送 /推荐 吃的 或 /推荐 喝的，获取对应推荐'''
        type_str = type_str.strip()
        if type_str in ["吃的", "吃", "美食"]:
            random_food = random.choice(FOOD_LIST)
            yield event.plain_result(f"🍚 推荐你吃：{random_food}")
        elif type_str in ["喝的", "喝", "饮品"]:
            random_drink = random.choice(DRINK_LIST)
            yield event.plain_result(f"🥤 推荐你喝：{random_drink}")
        else:
            yield event.plain_result("❌ 格式错误！请输入：\n/推荐 吃的\n或\n/推荐 喝的")

    async def terminate(self):
        '''插件卸载时执行'''
        logger.info("随机推荐插件已卸载～")