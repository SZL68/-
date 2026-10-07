# 智能催收决策 Demo

一个面向金融业务场景的智能催收策略 Demo，用于演示从**客户数据 → 还款概率预测 → 客户分层 → 催收策略 → API 服务**的完整 AI 工程流程。

> 本项目仅用于学习、技术演示和面试项目展示，使用的是模拟数据，不涉及真实客户信息，也不用于实际催收业务。

---

## 1. 项目简介

传统催收系统通常依赖固定规则，例如：

- 逾期超过一定天数 → 电话联系
- 多次逾期 → 人工跟进
- 有还款意愿 → 短信提醒

本项目尝试将机器学习模型与业务策略结合：

```text
客户历史数据
      ↓
还款概率预测模型
      ↓
预测未来 7 天还款概率
      ↓
客户分层
      ↓
业务策略决策
      ↓
选择触达方式
      ↓
FastAPI API
      ↓
外部业务系统调用
项目重点不在于构建一个复杂的金融模型，而在于展示：

如何将一个机器学习模型封装成可以被业务系统调用的 AI 服务。

2. 核心功能

目前项目包含以下功能：

2.1 客户还款概率预测

使用客户历史行为数据训练 Logistic Regression 模型，预测客户未来 7 天内的还款概率。

主要输入特征包括：

特征	含义
overdue_days	当前逾期天数
overdue_count	历史逾期次数
repayment_rate	历史还款率
contact_count	历史联系次数
promise_count	历史承诺还款次数
promise_kept	承诺还款后实际履约情况
app_active_days	App 活跃天数

模型输出：

7天还款概率
2.2 客户分层

根据模型预测的还款概率，将客户划分为不同层级：

还款概率 >= 0.75
        ↓
    高意向客户
        ↓
  自动提醒

0.40 <= 还款概率 < 0.75
        ↓
    中意向客户
        ↓
   AI 对话

还款概率 < 0.40
        ↓
    低意向客户
        ↓
   人工审核
2.3 策略决策

模型和业务策略进行了分离。

机器学习模型
     ↓
预测还款概率

业务策略模块
     ↓
根据概率选择执行策略

这样可以在不重新训练模型的情况下调整业务规则。

例如：

if repayment_probability >= 0.75:
    strategy = "automatic_reminder"
elif repayment_probability >= 0.40:
    strategy = "ai_dialogue"
else:
    strategy = "human_review"
2.4 FastAPI 服务

使用 FastAPI 将模型和策略封装为 HTTP API。

接口：

POST /collection/predict

外部业务系统只需要发送客户数据，即可获得：

{
    "repayment_probability": 0.86,
    "customer_level": "high_intent",
    "strategy": "automatic_reminder",
    "channel": "sms"
}
3. 项目结构
smart_collection/
│
├── data/
│   └── customers.csv
│
├── train.py
├── model.joblib
├── strategy.py
├── app.py
├── test_api.py
├── requirements.txt
├── Dockerfile
└── README.md
文件说明
train.py

负责：

生成模拟客户数据
构造训练标签
划分训练集和测试集
训练 Logistic Regression
评估模型
保存模型

最终生成：

customers.csv
model.joblib
model.joblib

保存训练完成的机器学习模型。

FastAPI 服务启动后会加载该模型，用于在线预测。

strategy.py

负责业务策略决策。

输入：

repayment_probability
overdue_days

输出：

customer_level
strategy
channel

将模型预测和业务规则进行解耦。

app.py

基于 FastAPI 构建模型服务。

主要负责：

接收 HTTP 请求
      ↓
解析 JSON
      ↓
构造模型输入
      ↓
调用模型
      ↓
获得还款概率
      ↓
调用策略模块
      ↓
返回 JSON
test_api.py

模拟外部业务系统调用 FastAPI。

通过 Python requests 发送 HTTP POST 请求：

requests.post(
    "http://127.0.0.1:8000/collection/predict",
    json=customer_data
)

用于验证整个 API 服务链路。

4. 技术栈
Machine Learning
Python
scikit-learn
Logistic Regression
pandas
joblib
Backend
FastAPI
Uvicorn
Pydantic
API Testing
requests
FastAPI Swagger / OpenAPI
Deployment
Docker（计划/基础部署）
5. 当前版本没有使用 LangChain

本项目当前版本没有使用 LangChain、RAG 或 Agent。

原因是当前版本主要解决的是：

机器学习模型如何完成训练，并通过 API 服务化。

整体架构比较简单：

ML Model
   ↓
Python
   ↓
FastAPI
   ↓
HTTP API
   ↓
Business System

后续如果引入大语言模型，可以进一步扩展：

客户数据
   ↓
还款概率模型
   ↓
客户分层
   ↓
策略引擎
   ↓
LLM
   ↓
RAG
   ↓
Agent / Tool Calling
   ↓
FastAPI
   ↓
业务系统
6. 环境配置

推荐 Python 3.10+。

安装依赖：

pip install -r requirements.txt

如果没有 requirements.txt，可以安装：

pip install pandas scikit-learn joblib fastapi uvicorn requests
7. 运行项目
Step 1：训练模型

运行：

python train.py

训练完成后会生成：

customers.csv
model.joblib

同时输出模型评估结果，例如：

Accuracy: 0.80
ROC-AUC: 0.87

注意：由于训练数据为模拟数据，模型指标仅用于演示完整机器学习流程，不代表真实金融业务中的预测能力。

Step 2：启动 FastAPI

运行：

uvicorn app:app --reload

启动成功后：

Uvicorn running on http://127.0.0.1:8000
Step 3：访问 API 文档

浏览器打开：

http://127.0.0.1:8000/docs

FastAPI 会自动生成 Swagger API 测试页面。

可以直接测试：

POST /collection/predict
Step 4：使用 Python 调用 API

另外打开一个终端：

python test_api.py

该脚本会模拟外部业务系统调用模型 API。

8. API 示例
Request

接口：

POST /collection/predict

请求：

{
    "overdue_days": 5,
    "overdue_count": 1,
    "repayment_rate": 0.95,
    "contact_count": 2,
    "promise_count": 1,
    "promise_kept": 1,
    "app_active_days": 6
}
Response

示例：

{
    "repayment_probability": 0.86,
    "customer_level": "high_intent",
    "strategy": "automatic_reminder",
    "channel": "sms"
}
9. 系统架构
                ┌──────────────────┐
                │  Customer Data   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    train.py      │
                │ LogisticRegression│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  model.joblib    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │     FastAPI      │
                │      app.py      │
                └────────┬─────────┘
                         │
                         ▼
              /collection/predict
                         │
                         ▼
                ┌──────────────────┐
                │ Prediction Model │
                └────────┬─────────┘
                         │
                         ▼
                Repayment Probability
                         │
                         ▼
                ┌──────────────────┐
                │  Strategy Engine │
                │   strategy.py    │
                └────────┬─────────┘
                         │
                         ▼
                Customer Segmentation
                         │
                         ▼
                Business Strategy
                         │
                         ▼
                JSON API Response
10. AI 工程链路

本项目重点练习了一个完整的模型服务化过程：

模型训练
   ↓
模型保存
   ↓
Python 模型加载
   ↓
FastAPI 封装
   ↓
HTTP API
   ↓
外部系统调用

对应实际企业中的典型架构：

AI Model
   ↓
Python Inference
   ↓
FastAPI
   ↓
Docker
   ↓
Server
   ↓
HTTP API
   ↓
ERP / CRM / Business System
11. 项目特点
模型与业务策略解耦

模型负责：

“这个客户未来 7 天还款的概率是多少？”

策略模块负责：

“根据这个概率应该采取什么业务策略？”

两者职责不同，可以独立调整。

API 服务化

模型不再只是一个：

model.predict()

而是被封装成一个可以被其他系统调用的 HTTP 服务：

POST /collection/predict

这使模型具备实际工程应用的基本形式。
