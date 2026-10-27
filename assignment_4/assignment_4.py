import os
import re
import pandas as pd

roll_number = 1024170013
folder = os.path.dirname(os.path.abspath(__file__))

# Q1
d1 = int(str(roll_number)[-2])
d2 = int(str(roll_number)[-1])

categories = ["billing", "account", "general"]
cat1 = categories[d1 % 3]
cat2 = categories[d2 % 3]

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
    }
]

personalized_entries = [
    {
        "question": "how do i update my registered mobile number",
        "answer": "Go to Profile > Account Settings and update your phone number with OTP verification.",
        "keywords": "mobile phone update",
        "category": cat1
    },
    {
        "question": "how can i download my fee receipt",
        "answer": "Log in to the student portal and navigate to Fee Details > Payment History to download the receipt.",
        "keywords": "receipt invoice download",
        "category": cat2
    }
]

df = pd.DataFrame(fixed_entries + personalized_entries)
print(df)

# Q2
def score_hypotheses(query, kb_df):
    query_words = set(re.findall(r"\b\w+\b", query.lower()))
    matches = []

    for idx, row in kb_df.iterrows():
        kw_list = set(row["keywords"].lower().split())
        matched = query_words.intersection(kw_list)
        score = len(matched)
        if score > 0:
            confidence = round(score / len(kw_list), 2)
            matches.append({
                "question": row["question"],
                "answer": row["answer"],
                "category": row["category"],
                "score": score,
                "confidence": confidence
            })

    res = pd.DataFrame(matches)
    if not res.empty:
        res = res.sort_values(by=["confidence", "score"], ascending=[False, False]).reset_index(drop=True)
    return res

print(score_hypotheses("how can i pay my annual fee online", df))

# Q3
def same_category(category_name, kb_df):
    return kb_df[kb_df["category"] == category_name]["question"].tolist()

print(same_category(cat1, df))

# Q4
target_idx = 1
new_kw = input("Enter a new keyword: ").strip()
df.loc[target_idx, "keywords"] = df.loc[target_idx, "keywords"] + " " + new_kw

csv_file = os.path.join(folder, f"{roll_number}_faq_data.csv")
df.to_csv(csv_file, index=False)

# Q5
print(df.groupby("category").size())

# Q6
def score_with_tie_handling(query, kb_df):
    query_words = set(re.findall(r"\b\w+\b", query.lower()))
    matches = []

    for idx, row in kb_df.iterrows():
        kw_list = set(row["keywords"].lower().split())
        matched = query_words.intersection(kw_list)
        score = len(matched)
        if score > 0:
            confidence = round(score / len(kw_list), 2)
            matches.append({
                "question": row["question"],
                "answer": row["answer"],
                "category": row["category"],
                "score": score,
                "confidence": confidence
            })

    if not matches:
        print("No match")
        return

    results = pd.DataFrame(matches).sort_values(by=["score", "confidence"], ascending=[False, False])
    top_score = results["score"].max()
    top_matches = results[results["score"] == top_score]

    print(f"\nQuery: {query}")
    if len(top_matches) > 1:
        print("Tie detected:")
        print(top_matches[["question", "answer", "score", "confidence"]])
    else:
        print("Single match:")
        print(top_matches[["question", "answer", "score", "confidence"]])

score_with_tie_handling("fee", df)
score_with_tie_handling("how to reset password login", df)
