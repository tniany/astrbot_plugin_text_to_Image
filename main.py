from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import aiohttp
import urllib.parse

@register("upload_text_to_image", "浅月tniay", "使bot以图片形式返回内容，将文本以图片的形式发送", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config=None):
        super().__init__(context)
        self.image_mode = False  # 默认为关闭图片模式
        # API配置
        self.api_url = "https://api.suyanw.cn/api/zdytwhc.php"
        self.image_url = "https://api.suyanw.cn/api/comic.php"  # 默认值
        self.text_size = 85
        
        # 从配置中读取image_url
        try:
            if config and "image_url" in config:
                self.image_url = config["image_url"]
                logger.info(f"从配置中读取图片模板地址：{self.image_url}")
        except Exception as e:
            logger.error(f"读取配置失败：{e}")
        
        logger.info(f"文本转图片插件初始化，当前图片模式：{self.image_mode}")

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        logger.info("文本转图片插件初始化成功")

    # 注册指令的装饰器。指令名为 p。注册成功后，发送 `/p 文本` 就会触发这个指令，并将文本转换为图片返回
    @filter.command("p")
    async def text_to_image(self, event: AstrMessageEvent):
        """将文本转换为图片并发送"""
        message_str = event.message_str # 用户发的纯文本消息字符串
        logger.info(f"收到/p指令，message_str: '{message_str}'")
        if not message_str:
            async for result in self.send_message(event, "请输入要转换为图片的文本，例如：/p 你好世界"):
                yield result
            return
        
        # 去除"p"字符和空格，只保留用户输入的文本内容
        user_text = message_str.strip()
        if user_text.startswith('p '):
            user_text = user_text[2:].strip()
        logger.info(f"处理后的文本: '{user_text}'")
        
        if not user_text:
            async for result in self.send_message(event, "请输入要转换为图片的文本，例如：/p 你好世界"):
                yield result
            return
        
        try:
            # 构建API请求URL
            text = urllib.parse.quote(user_text)
            api_url = f"https://api.suyanw.cn/api/zdytwhc.php?image={self.image_url}&size=85&text={text}&color=true"
            
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
    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("tp")
    async def toggle_image_mode(self, event: AstrMessageEvent):
        """切换图片模式，开启后bot返回的内容全部使用图片形式返回"""
        self.image_mode = not self.image_mode
        status = "开启" if self.image_mode else "关闭"
        logger.info(f"图片模式已{status}，当前状态：{self.image_mode}")
        # 发送状态消息，会根据当前图片模式决定是发送图片还是文字
        async for result in self.send_message(event, f"图片模式已{status}。\n开启后，bot返回的所有内容都会自动转换为图片形式。"):
            yield result

    # 注册指令的装饰器。指令名为 z。注册成功后，发送 `/z 图片地址` 就会触发这个指令，设置图片模板地址
    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("z")
    async def set_image_url(self, event: AstrMessageEvent):
        """设置图片模板地址"""
        message_str = event.message_str # 用户发的纯文本消息字符串
        if not message_str:
            async for result in self.send_message(event, "请输入要设置的图片模板地址，例如：/z https://example.com/image.png"):
                yield result
            return
        
        try:
            # 更新图片模板地址
            self.image_url = message_str
            logger.info(f"图片模板地址已设置为：{self.image_url}")
            # 发送状态消息
            async for result in self.send_message(event, f"图片模板地址已设置为：{self.image_url}"):
                yield result
        except Exception as e:
            logger.error(f"设置图片模板地址时出错：{e}")
            async for result in self.send_message(event, f"设置图片模板地址时出错：{str(e)}"):
                yield result



    async def send_message(self, event: AstrMessageEvent, text: str):
        """发送消息，当图片模式开启时，将文本转换为图片发送"""
        logger.info(f"发送消息：{text[:50]}...，图片模式：{self.image_mode}")
        if self.image_mode:
            try:
                # 构建API请求URL
                text_encoded = urllib.parse.quote(text)
                api_url = f"https://api.suyanw.cn/api/zdytwhc.php?image={self.image_url}&size=85&text={text_encoded}&color=true"
                logger.info(f"构建图片API URL：{api_url}")
                
                # 直接发送API URL作为图片
                try:
                    logger.info("尝试发送图片消息")
                    yield event.image_result(api_url)
                    logger.info("图片消息发送成功")
                except Exception as e:
                    logger.error(f"发送图片消息时出错：{e}")
                    # 出错时发送纯文本
                    logger.info("图片发送失败，回退到纯文本")
                    yield event.plain_result(text)
            except Exception as e:
                logger.error(f"生成图片时出错：{e}")
                # 出错时发送纯文本
                logger.info("生成图片失败，回退到纯文本")
                yield event.plain_result(text)
        else:
            # 图片模式关闭时，发送纯文本
            logger.info("图片模式关闭，发送纯文本")
            yield event.plain_result(text)

    # 发送消息前的钩子，用于将文本消息转换为图片
    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent):
        """在发送消息前装饰消息，将文本转换为图片"""
        if self.image_mode:
            try:
                result = event.get_result()
                if result:
                    # 检查消息链中是否有文本消息
                    has_text = False
                    text_content = ""
                    for component in result.chain:
                        if hasattr(component, 'text'):
                            has_text = True
                            text_content += component.text
                    
                    if has_text:
                        # 构建API请求URL
                        text_encoded = urllib.parse.quote(text_content)
                        api_url = f"https://api.suyanw.cn/api/zdytwhc.php?image={self.image_url}&size=85&text={text_encoded}&color=true"
                        logger.info(f"将文本转换为图片：{text_content[:50]}...")
                        
                        # 直接使用event.image_result创建图片消息
                        # 注意：这里我们需要使用event.image_result的返回值
                        image_result = event.image_result(api_url)
                        # 设置新的结果
                        event.set_result(image_result)
            except Exception as e:
                logger.error(f"装饰消息时出错：{e}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        logger.info("文本转图片插件已卸载")
