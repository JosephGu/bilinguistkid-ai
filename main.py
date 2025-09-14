from asyncio.windows_events import NULL
import os
from fastapi import FastAPI, status
import sys
from dashscope.audio.tts import SpeechSynthesizer
from openai import OpenAI
import dashscope

app = FastAPI()
dashscope.api_key = os.getenv("ALIBABA_API_KEY")


@app.get("/getFact", status_code=status.HTTP_200_OK)
def get_fact(country: str, age: int, gender: str):
    try:
        # logger.info(f"接收到请求: country={country}, age={age}, gender={gender}")

        # 获取API密钥
        api_key = os.getenv("DEEPSEEK_API_KEY")
        ali_key = os.getenv("ALIBABA_API_KEY")
        if not api_key:
            # logger.error("API密钥未找到")
            return {
                "code": 400,
                "message": "API key not found",
                "error_code": "API_KEY_MISSING",
            }, status.HTTP_400_BAD_REQUEST

        # 创建OpenAI客户端
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        genderChinese = "小男孩" if gender == "Male" else "小女孩"
        # logger.info(f"准备调用OpenAI API: 为{age}岁{genderChinese}生成关于{country}的有趣事实")

        # 调用API
        response = client.chat.completions.create(
            model="deepseek-chat",
            temperature=1,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的英语老师，你了解世界各国的有趣的事实，你会根据孩子的年龄和性别用英语讲一个给定国家的有趣的事实,并且只专注一个事情",
                },
                {
                    "role": "user",
                    "content": f"我是{age}岁{genderChinese}，我想知道关于{country}的有趣的事实，请根据我的年龄用英语给出我的认知以内的小趣事，最多50个单词",
                },
            ],
            stream=False,
        )

        # 提取结果
        content = response.choices[0].message.content
        # logger.info(f"API调用成功，返回结果长度: {len(content)}字符")

        if not ali_key:
            return {
                "code": 200,
                "message": content,
                "audio": "",
            }

        result = SpeechSynthesizer.call(
            model="sambert-eva-v1", text=content, sample_rate=16000, format="wav"
        )
        if result.get_audio_data() is not None:
            # 保存音频文件，添加时间戳防止并发冲突
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            output_file = f"output_{timestamp}.wav"
            with open(output_file, "wb") as f:
                f.write(result.get_audio_data())

            # 将二进制音频数据转换为Base64编码的字符串
            import base64

            audio_base64 = base64.b64encode(result.get_audio_data()).decode("utf-8")

            print(
                "SUCCESS: get audio data: %dbytes in %s"
                % (sys.getsizeof(result.get_audio_data()), output_file)
            )

            print("content:", content)

            # 返回Base64编码的音频数据
            return {
                "code": 200,
                "message": content,
                "audio": audio_base64,  # 返回Base64编码的音频数据
            }
        else:
            print("ERROR: response is %s" % (result.get_response()))
            return {
                "code": 200,
                "message": content,
                "audio": "",
            }

    except Exception as e:
        # logger.error(f"处理请求时发生错误: {str(e)}", exc_info=True)
        # 捕获所有异常并返回错误响应
        return {
            "code": 500,
            "message": str(e),
            "error_code": "SERVER_ERROR",
        }, status.HTTP_500_INTERNAL_SERVER_ERROR
