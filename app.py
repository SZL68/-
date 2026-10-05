from fastapi import FastAPI
from pydantic import BaseModel
import joblib

from strategy import choose_strategy


app = FastAPI(
    title="Smart Collection API",
    version="1.0"
)


# ======================================
# 加载模型
# ======================================

model = joblib.load(
    "model.joblib"
)


# ======================================
# 定义输入
# ======================================

class CustomerData(BaseModel):

    overdue_days: int

    overdue_count: int

    repayment_rate: float

    contact_count: int

    promise_count: int

    promise_kept: int

    app_active_days: int


# ======================================
# 健康检查
# ======================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# ======================================
# 智能催收接口
# ======================================

@app.post("/collection/predict")
def collection_predict(
    data: CustomerData
):

    features = [[

        data.overdue_days,

        data.overdue_count,

        data.repayment_rate,

        data.contact_count,

        data.promise_count,

        data.promise_kept,

        data.app_active_days

    ]]


    # ==========================
    # 模型预测
    # ==========================

    probability = model.predict_proba(
        features
    )[0][1]


    # ==========================
    # 策略决策
    # ==========================

    strategy = choose_strategy(

        probability,

        data.overdue_days

    )


    # ==========================
    # 返回结果
    # ==========================

    return {

        "repayment_probability":
            round(
                float(probability),
                4
            ),

        "customer_level":
            strategy["customer_level"],

        "strategy":
            strategy["strategy"],

        "channel":
            strategy["channel"]

    }