import os
import pandas as pd

roll_number = 1024170013
folder = os.path.dirname(os.path.abspath(__file__))

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

target_idx = 1
new_kw = input("Enter a new keyword: ").strip()

df.loc[target_idx, "keywords"] = df.loc[target_idx, "keywords"] + " " + new_kw

csv_file = os.path.join(folder, f"{roll_number}_faq_data.csv")
df.to_csv(csv_file, index=False)
print("Updated entry:")
print(df.loc[target_idx])
