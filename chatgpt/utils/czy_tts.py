from loguru import logger
from aiohttp import ClientSession, ClientTimeout
from constants import config

class CzyAPI:
    def __init__(self):
        self.lang = 'zh'
        self.id = None # 大概是角色语音的id
        self.initialized = False

    async def initialize(self, new_id=None):
        # if new_id is not None:
        #     await self.set_id(new_id)
        # elif self.id is None:
        #     self.id = await self.voice_speakers_check()

        self.initialized = True

    async def get_voice_data(self, text, lang, voice_type):
        url = config.gptsolvits.api_url
        
        data = {
            "text": text,
            "text_language": lang,
        }

        async with ClientSession(timeout=ClientTimeout(total=config.gptsolvits.timeout)) as session:
            try:
                async with session.post(url, json=data) as response:
                    if response.status != 200:
                        logger.error(f"请求失败：{response.status}")
                        return None
                    return await response.read()
            except TimeoutError as e:
                logger.error(f"请求语音超时：{text}")
                return None
            except Exception as e:
                logger.error(f"请求失败：{str(e)}")
                return None


    def save_voice_file(self, content, save_path):
        try:
            with open(save_path, 'wb') as f:
                f.write(content)
            logger.success(f"[VITS TTS] 文件已保存到：{save_path}")
        except IOError as e:
            logger.error(f"[VITS TTS] 文件写入失败：{str(e)}")
            return None

        return save_path

    async def response(self, text, voice_type, path):
        content = await self.get_voice_data(text, self.lang, voice_type)
        if content is not None:
            return self.save_voice_file(content, path)

    async def process_message(self, message, path, voice_type):
        if not self.initialized:
            await self.initialize()
        return await self.response(message, voice_type, path)

czy_api_instance = CzyAPI()
