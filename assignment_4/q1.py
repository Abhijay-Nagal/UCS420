import pandas as pd

roll_number = 1024170013

d1 = int(str(roll_number)[-2])
d2 = int(str(roll_number)[-1])

categories = ["billing", "account", "general"]
category_1 = categories[d1 % 3]
category_2 = categories[d2 % 3]

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
        "category": category_1
    },
    {
        "question": "how can i download my fee receipt",
        "answer": "Log in to the student portal and navigate to Fee Details > Payment History to download the receipt.",
        "keywords": "receipt invoice download",
        "category": category_2
    }
]

df = pd.DataFrame(fixed_entries + personalized_entries)
print(df)
