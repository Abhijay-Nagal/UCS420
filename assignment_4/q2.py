import re
import pandas as pd

fixed_entries = [
    {
        "question": "what is the annual fee",
        "answer": "The annual fee is Rs 500.",
        "keywords": "fee cost price charge",
        "category": "billing"
    },
    {
        "question": "how to reset password",
        "answer": "Go to Settings > Reset Password.",
        "keywords": "password reset login",
        "category": "account"
    },
    {
        "question": "what are your working hours",
        "answer": "We are open 9 AM to 5 PM.",
        "keywords": "hours timing open time",
        "category": "general"
    },
    {
        "question": "how can i pay the fee",
        "answer": "You can pay via UPI, card, or net banking.",
        "keywords": "pay payment upi fee",
        "category": "billing"
    },
    {
        "question": "how do i update my registered mobile number",
        "answer": "Go to Profile > Account Settings and update your phone number with OTP verification.",
        "keywords": "mobile phone update",
        "category": "account"
    },
    {
        "question": "how can i download my fee receipt",
        "answer": "Log in to the student portal and navigate to Fee Details > Payment History to download the receipt.",
        "keywords": "receipt invoice download",
        "category": "billing"
    }
]

df = pd.DataFrame(fixed_entries)

def score_hypotheses(query, kb_df):
    query_words = set(re.findall(r"\b\w+\b", query.lower()))
    results = []

    for idx, row in kb_df.iterrows():
        kw_list = set(row["keywords"].lower().split())
        matched = query_words.intersection(kw_list)
        score = len(matched)
        if score > 0:
            confidence = round(score / len(kw_list), 2)
            results.append({
                "question": row["question"],
                "answer": row["answer"],
                "category": row["category"],
                "matched_keywords": list(matched),
                "score": score,
                "confidence": confidence
            })

    res_df = pd.DataFrame(results)
    if not res_df.empty:
        res_df = res_df.sort_values(by=["confidence", "score"], ascending=[False, False]).reset_index(drop=True)
    return res_df

query = "how can i pay my annual fee online"
print(score_hypotheses(query, df))
