# plugin_upload_text_to_Image 插件

AstrBot 插件，使bot以图片形式返回内容，将文本以图片的形式发送。基于外部API的二次元风格文转图，提供更美观的文本展示效果。

## 功能介绍

- **单次文本转图片**：使用 `/p 文本` 指令将指定文本转换为图片并发送
- **图片模式切换**：使用 `/tp` 指令切换图片模式，开启后所有返回内容都会转换为图片
- **自动错误处理**：当图片生成失败时，会自动回退到发送纯文本
- **二次元风格**：基于外部API生成的图片具有美观的二次元风格

## 技术实现

- 使用 `aiohttp` 库进行异步HTTP请求
- 调用外部API生成图片：`https://api.suyanw.cn/api/zdytwhc.php`
- 支持文本URL编码和完整的错误处理机制
- 兼容多种聊天平台

## 支持平台

- QQ
- Telegram
- 飞书
- 钉钉
- Slack
- Line
- Discord
- Matrix

## 安装方法

1. 克隆或下载本插件到 AstrBot 的插件目录
   ```bash
   git clone https://github.com/tniany/plugin_upload_text_to_Image.git
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 重启 AstrBot 即可使用

## 使用示例

### 单次文本转图片

```
/p 你好，这是一条测试消息
```

### 切换图片模式

```
/tp
# 回复：图片模式已开启

/tp
# 回复：图片模式已关闭
```

## 依赖

- Python 3.7+
- aiohttp

## 许可证

[MIT](LICENSE)

## 作者

浅月tniay

## 版本

v1.0.6

## 仓库地址

[GitHub](https://github.com/tniany/plugin_upload_text_to_Image)
