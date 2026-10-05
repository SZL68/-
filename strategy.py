def choose_strategy(
    repayment_probability,
    overdue_days
):

    # 高还款意愿
    if repayment_probability >= 0.75:

        return {
            "customer_level": "high_intent",
            "strategy": "automatic_reminder",
            "channel": "sms"
        }


    # 中等还款意愿
    elif repayment_probability >= 0.40:

        return {
            "customer_level": "medium_intent",
            "strategy": "ai_dialogue",
            "channel": "ai_call"
        }


    # 低还款意愿
    else:

        return {
            "customer_level": "low_intent",
            "strategy": "human_review",
            "channel": "human_agent"
        }