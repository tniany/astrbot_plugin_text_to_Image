from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import aiohttp
import urllib.parse

@register("upload_text_to_image", "浅月tniay", "使bot以图片形式返回内容，将文本以图片的形式发送", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.image_mode = False  # 默认为关闭图片模式
        # API配置
        self.api_url = "https://api.suyanw.cn/api/zdytwhc.php"
        self.image_url = "https://api.suyanw.cn/api/comic.php"
        self.text_size = 85

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        logger.info("文本转图片插件初始化成功")

    # 注册指令的装饰器。指令名为 p。注册成功后，发送 `/p 文本` 就会触发这个指令，并将文本转换为图片返回
    @filter.command("p")
    async def text_to_image(self, event: AstrMessageEvent):
        """将文本转换为图片并发送""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        message_str = event.message_str # 用户发的纯文本消息字符串
        if not message_str:
            async for result in self.send_message(event, "请输入要转换为图片的文本，例如：/p 你好世界"):
                yield result
            return
        
        try:
            # 构建API请求URL
            text = urllib.parse.quote(message_str)
            api_url = f"https://api.suyanw.cn/api/zdytwhc.php?image=https://api.suyanw.cn/api/comic.php&size=85&text={text}&color=true"
            
            # 直接发送API URL作为图片
            try:
                yield event.image_result(api_url)
            except Exception as e:
                logger.error(f"发送图片消息时出错：{e}")
                async for result in self.send_message(event, f"发送图片失败：{str(e)}"):
                    yield result
        except Exception as e:
            logger.error(f"生成图片时出错：{e}")
            async for result in self.send_message(event, f"生成图片时出错：{str(e)}"):
                yield result

    # 注册指令的装饰器。指令名为 tp。注册成功后，发送 `/tp` 就会触发这个指令，切换图片模式
    @filter.command("tp")
    async def toggle_image_mode(self, event: AstrMessageEvent):
        """切换图片模式，开启后bot返回的内容全部使用图片形式返回"""
        self.image_mode = not self.image_mode
        status = "开启" if self.image_mode else "关闭"
        logger.info(f"图片模式已{status}")
        async for result in self.send_message(event, f"图片模式已{status}"):
            yield result



    async def send_message(self, event: AstrMessageEvent, text: str):
        """发送消息，当图片模式开启时，将文本转换为图片发送"""
        if self.image_mode:
            try:
                # 构建API请求URL
                text_encoded = urllib.parse.quote(text)
                api_url = f"https://api.suyanw.cn/api/zdytwhc.php?image=https://api.suyanw.cn/api/comic.php&size=85&text={text_encoded}&color=true"
                
                # 直接发送API URL作为图片
                try:
                    yield event.image_result(api_url)
                except Exception as e:
                    logger.error(f"发送图片消息时出错：{e}")
                    # 出错时发送纯文本
                    yield event.plain_result(text)
            except Exception as e:
                logger.error(f"生成图片时出错：{e}")
                # 出错时发送纯文本
                yield event.plain_result(text)
        else:
            # 图片模式关闭时，发送纯文本
            yield event.plain_result(text)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        logger.info("文本转图片插件已卸载")
