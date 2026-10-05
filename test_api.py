import requests


# FastAPI 服务地址
url = "http://127.0.0.1:8000/collection/predict"


# 模拟一个客户
customer_data = {
    "overdue_days": 5,
    "overdue_count": 1,
    "repayment_rate": 0.95,
    "contact_count": 2,
    "promise_count": 1,
    "promise_kept": 1,
    "app_active_days": 6
}


# 调用 API
response = requests.post(
    url,
    json=customer_data
)


# 判断请求是否成功
if response.status_code == 200:
    result = response.json()

    print("API 调用成功")
    print("客户数据：")
    print(customer_data)

    print("\n模型与策略返回结果：")
    print(f"7天还款概率：{result['repayment_probability']}")
    print(f"客户分层：{result['customer_level']}")
    print(f"执行策略：{result['strategy']}")
    print(f"执行渠道：{result['channel']}")

else:
    print("API 调用失败")
    print("状态码：", response.status_code)
    print("错误信息：", response.text)