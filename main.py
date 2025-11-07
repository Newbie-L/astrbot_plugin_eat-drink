from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register, StarTools
from astrbot.api import logger
import random
import shutil  # 用于复制文件
from pathlib import Path


PLUGIN_NAME = "astrbot_plugin_eatdrink"

@register(
    PLUGIN_NAME, 
    "Cybercat",
    "随机推荐吃什么、喝什么，选择困难症救星～", 
    "1.1.0", 
    "https://github.com/Newbie-L/astrbot_plugin_eatdrink"
)
class RandomFoodDrinkPlugin(Star):
    DEFAULT_FOODS = ["火锅", "烤肉", "寿司", "麻辣烫", "螺蛳粉", "牛肉面"]
    DEFAULT_DRINKS = ["奶茶", "咖啡", "可乐", "果汁", "柠檬水", "气泡水"]
    
    DEFAULT_LIST_MAP = {
        "food.txt": DEFAULT_FOODS,
        "drink.txt": DEFAULT_DRINKS,
    }

    def __init__(self, context: Context):
        super().__init__(context) 
        
        # 1. 定义路径
        self.plugin_name = PLUGIN_NAME
        self.target_data_dir = Path(StarTools.get_data_dir(self.plugin_name))  # 目标目录（用户数据目录）
        self.plugin_root_dir = Path(__file__).parent  # 插件根目录（main.py 所在目录）
        self.template_dir = self.plugin_root_dir / "templates"  # 模板文件目录（插件自带）

        # 2. 自动复制模板文件到目标目录（首次安装时）
        self._copy_template_files()

        # 3. 加载列表（从目标目录读取）
        self.food_list = self._load_list("food.txt")
        self.drink_list = self._load_list("drink.txt")
        
        logger.info(f"插件初始化完成，数据目录：{self.target_data_dir}")
        logger.info(f"加载食物 {len(self.food_list)} 种，饮品 {len(self.drink_list)} 种")

    def _copy_template_files(self):
        """将插件自带的 templates 目录中的文件复制到目标数据目录（仅当目标文件不存在时）"""
        # 确保目标目录存在
        self.target_data_dir.mkdir(parents=True, exist_ok=True)
        
        # 确保模板目录存在（如果用户下载的插件缺少 templates 文件夹，跳过复制）
        if not self.template_dir.exists():
            logger.warning(f"未找到模板目录 {self.template_dir}，跳过自动复制")
            return
        
        # 复制 templates 目录下的所有文件（这里只处理 food.txt 和 drink.txt）
        for filename in ["food.txt", "drink.txt"]:
            template_file = self.template_dir / filename  # 插件自带的模板文件
            target_file = self.target_data_dir / filename  # 目标路径的文件
            
            # 仅当目标文件不存在时，才复制模板文件
            if not target_file.exists() and template_file.exists():
                shutil.copy2(template_file, target_file)  # copy2 保留文件元信息
                logger.info(f"已自动创建 {target_file}（从模板复制）")
            elif not template_file.exists():
                logger.warning(f"模板文件 {template_file} 不存在，无法复制")

    def _load_list(self, filename: str) -> list:
        """从目标数据目录加载列表（兼容文件不存在/读取失败）"""
        file_path = self.target_data_dir / filename  
        default_list = self.DEFAULT_LIST_MAP.get(filename, [])
        
        if not file_path.exists():
            logger.warning(f"文件 {file_path} 不存在，使用默认列表")
            return default_list
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            return lines if lines else default_list
        except Exception as e:
            logger.error(f"读取 {file_path} 失败：{str(e)}，使用默认列表")
            return default_list

    # 指令方法（保持不变）
    @filter.command("吃什么", alias={"推荐吃的", "吃点啥"}, args=["event"])
    async def recommend_food(self, event: AstrMessageEvent):
        random_food = random.choice(self.food_list)
        logger.info(f"为用户 {event.get_sender_name()} 推荐美食：{random_food}")
        yield event.plain_result(f"🍚 推荐你吃：{random_food}")

    @filter.command("喝什么", alias={"推荐喝的", "喝点啥"}, args=["event"])
    async def recommend_drink(self, event: AstrMessageEvent):
        random_drink = random.choice(self.drink_list)
        logger.info(f"为用户 {event.get_sender_name()} 推荐饮品：{random_drink}")
        yield event.plain_result(f"🥤 推荐你喝：{random_drink}")

    @filter.command("吃喝什么", args=["event"])
    async def recommend_food_drink(self, event: AstrMessageEvent):
        random_food = random.choice(self.food_list)
        random_drink = random.choice(self.drink_list)
        logger.info(f"为用户 {event.get_sender_name()} 推荐搭配：{random_food} + {random_drink}")
        yield event.plain_result(
            f"🍽️  吃喝搭配推荐：\n"
            f"主食：{random_food}\n"
            f"饮品：{random_drink}"
        )

    async def terminate(self):
        logger.info("随机推荐插件已卸载～")