import os
from fastapi import FastAPI, status
from openai import OpenAI

app = FastAPI()

@app.get("/getFact", status_code=status.HTTP_200_OK)
def get_fact(country: str, age: int, gender: str):
    try:
        # logger.info(f"接收到请求: country={country}, age={age}, gender={gender}")
        
        # 获取API密钥
        api_key = os.getenv("DEEPSEEK_API_KEY")
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
                    "content": "你是一个专业的英语老师，你了解世界各国的有趣的事实，你会根据孩子的年龄和性别用英语讲一个给定国家的有趣的事实",
                },
                {
                    "role": "user",
                    "content": f"我是{age}岁{genderChinese}，我想知道关于{country}的有趣的事实，请根据我的年龄用英语给出我的认知以内的小趣事，最多80个单词",
                }
            ],
            stream=False,
        )

        # 提取结果
        content = response.choices[0].message.content
        # logger.info(f"API调用成功，返回结果长度: {len(content)}字符")
        
        # 返回成功响应
        return {"code": 200, "message": content}

    except Exception as e:
        # logger.error(f"处理请求时发生错误: {str(e)}", exc_info=True)
        # 捕获所有异常并返回错误响应
        return {
            "code": 500,
            "message": str(e),
            "error_code": "SERVER_ERROR",
        }, status.HTTP_500_INTERNAL_SERVER_ERROR
