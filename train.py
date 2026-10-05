import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score


np.random.seed(42)


# ======================================
# 1. 生成模拟客户数据
# ======================================

n = 2000

data = pd.DataFrame({

    "overdue_days": np.random.randint(1, 90, n),

    "overdue_count": np.random.randint(0, 8, n),

    "repayment_rate": np.random.uniform(0.1, 1.0, n),

    "contact_count": np.random.randint(0, 10, n),

    "promise_count": np.random.randint(0, 5, n),

    "promise_kept": np.random.randint(0, 2, n),

    "app_active_days": np.random.randint(0, 8, n)
})


# ======================================
# 2. 构造模拟标签
# ======================================

score = (

    1.5 * data["repayment_rate"]

    + 0.8 * data["promise_kept"]

    + 0.1 * data["app_active_days"]

    - 0.02 * data["overdue_days"]

    - 0.2 * data["overdue_count"]

)


probability = 1 / (1 + np.exp(-score))

data["repaid_7d"] = (
    np.random.rand(n) < probability
).astype(int)


# ======================================
# 3. 保存模拟数据
# ======================================

data.to_csv(
    "customers.csv",
    index=False
)


# ======================================
# 4. 定义特征
# ======================================

features = [
    "overdue_days",
    "overdue_count",
    "repayment_rate",
    "contact_count",
    "promise_count",
    "promise_kept",
    "app_active_days"
]


X = data[features]

y = data["repaid_7d"]


# ======================================
# 5. 划分训练集和测试集
# ======================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y
)


# ======================================
# 6. 训练模型
# ======================================

model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train,
    y_train
)


# ======================================
# 7. 模型评估
# ======================================

pred = model.predict(X_test)

prob = model.predict_proba(X_test)[:, 1]


accuracy = accuracy_score(
    y_test,
    pred
)

auc = roc_auc_score(
    y_test,
    prob
)


print(
    f"Accuracy: {accuracy:.4f}"
)

print(
    f"AUC: {auc:.4f}"
)


# ======================================
# 8. 保存模型
# ======================================

joblib.dump(
    model,
    "model.joblib"
)

print(
    "Model saved."
)