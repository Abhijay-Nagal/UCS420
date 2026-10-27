import os
import re
import string
import random
import hashlib
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, LancasterStemmer, RegexpStemmer, WordNetLemmatizer
from nltk import pos_tag

ROLL_NO = 1024170013
NAME = "Abhijay Nagal"
STOP = set(stopwords.words("english"))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_dataset(roll_no):
    rng = random.Random(int(roll_no))

    subjects = [("LMS", ["LMS", "lms"]), ("Wi-Fi", ["Wi-Fi", "WiFi", "wifi"]), ("VPN", ["VPN"]),
                ("email", ["email", "e-mail"]), ("password", ["password"]), ("portal", ["student portal"]),
                ("projector", ["projector"]), ("laptop", ["laptop"]), ("MATLAB", ["MATLAB", "Matlab"]),
                ("Python", ["Python"]), ("printer", ["printer"]), ("server", ["server"])]
    actions = ["is not working", "keeps disconnecting", "failed to open", "is running slowly",
               "crashes while opening", "stopped responding", "is showing an error", "was working yesterday",
               "has stopped syncing", "keeps asking for login"]
    user_actions = ["cannot access", "can't open", "couldn't connect to", "am unable to use",
                    "tried restarting", "was locked out of", "keep getting logged out of", "reinstalled"]
    contexts = ["after resetting my password", "during the lab", "on my laptop", "since yesterday",
                "after the latest update", "when I use mobile hotspot", "before the assignment deadline",
                "while uploading the file", "after restarting the system", "when connected to campus Wi-Fi"]
    endings = ["Please help.", "Can you check this?", "I have tried several times!", "It worked yesterday.",
               "I don't know what changed.", "The same problem occurs again.", "Is there another solution?",
               "It works on another computer.", "This is urgent.", "Please resolve it."]
    challenges = {
        "negation": ["The Wi-Fi works, but the VPN doesn't.", "Why isn't the portal opening?",
                     "I can't login and I didn't change anything.", "It's not the laptop; it's the server.",
                     "Nothing works and nobody has replied.", "The printer won't print; it isn't jammed."],
        "numbers": ["Python 3.12 was installed yesterday.", "The file is 95.5% uploaded.",
                    "Error code 0x80070005 appears.", "I need Windows 11 by 5.30 p.m. today.",
                    "Only 2 of 30 PCs boot after 3.5 hours.", "Version 2.0.1 crashes at 99%."],
        "identifiers": ["Email me at helpdesk@university.edu.", "See https://lms.thapar.edu/help for details.",
                        "My roll no. is 1023-03-021.", "Ticket #4521 is still open.",
                        "Call me on +91 98765 43210 or 0175-239-3201.",
                        "Write to it.helpdesk@thapar.edu or visit www.thapar.edu/it."],
        "punctuation": ["I tried again... still no response!!!", "The LMS says 'Not Submitted'.",
                        "Dr. Rao's lab PC (No. 14) is down.", "Is it fixed?? Pls reply ASAP :(",
                        "The state-of-the-art lab (Lab-3) is closed.", "Re-installing didn't help; log-in still fails!"],
    }

    tickets = []
    for _ in range(8 + int(roll_no) % 5):
        _, variants = rng.choice(subjects)
        s = rng.choice(variants)
        template = rng.randrange(3)
        if template == 0:
            text = f"{s} {rng.choice(actions)} {rng.choice(contexts)}. {rng.choice(endings)}"
        elif template == 1:
            text = f"I {rng.choice(user_actions)} the {s} {rng.choice(contexts)}. {rng.choice(endings)}"
        else:
            text = f"The {s} {rng.choice(actions)}. {rng.choice(endings)}"
        tickets.append(text[0].upper() + text[1:])
    for category in ["negation", "numbers", "identifiers", "punctuation"]:
        tickets.append(rng.choice(challenges[category]))
    rng.shuffle(tickets)

    df = pd.DataFrame({"Ticket_ID": [f"T{i + 1:02d}" for i in range(len(tickets))], "Ticket_Text": tickets})
    focus = [f"T{i:02d}" for i in sorted(rng.sample(range(1, len(tickets) + 1), 2))]
    fingerprint = hashlib.md5(("|".join(tickets) + str(int(roll_no))).encode()).hexdigest()[:8].upper()
    return df, focus, fingerprint

def is_punct(token):
    return all(ch in string.punctuation for ch in token)

def process_ticket(text):
    sentences = sent_tokenize(text)
    tokens = [t.lower() for s in sentences for t in word_tokenize(s)]
    punct = [t for t in tokens if is_punct(t)]
    stops = [t for t in tokens if t in STOP]
    final = [t for t in tokens if not is_punct(t) and t not in STOP]
    return {"sentences": sentences, "tokens": tokens, "punct": punct, "stops": stops, "final": final}

# 1. Dataset Generation & Preprocessing
df, FOCUS, FINGERPRINT = generate_dataset(ROLL_NO)
print("Roll Number:", ROLL_NO)
print("Name:", NAME)
print("Fingerprint:", FINGERPRINT)
print("Focus Tickets:", FOCUS)
print(df)

csv_path = os.path.join(OUTPUT_DIR, f"{ROLL_NO}_generated_dataset.csv")
df.to_csv(csv_path, index=False)

q1_rows = []
processed_dict = {}

for _, row in df.iterrows():
    tid = row["Ticket_ID"]
    res = process_ticket(row["Ticket_Text"])
    processed_dict[tid] = res
    q1_rows.append({
        "Ticket_ID": tid,
        "Sentences": len(res["sentences"]),
        "Tokens": len(res["tokens"]),
        "Punctuation": len(res["punct"]),
        "Stopwords": len(res["stops"]),
        "Unique_Tokens": len(set(res["tokens"])),
        "Final_Tokens": len(res["final"])
    })

q1_table = pd.DataFrame(q1_rows)
print(q1_table)

sel_id = FOCUS[0]
sel_res = processed_dict[sel_id]
print("Breakdown for", sel_id)
print(sel_res["sentences"])
print(sel_res["tokens"])
print(sel_res["punct"])
print(sel_res["stops"])
print(sel_res["final"])

all_final_tokens = [t for res in processed_dict.values() for t in res["final"]]
non_alpha = sorted(list(set(t for t in all_final_tokens if not t.isalpha())))
print("Non-alpha tokens:", non_alpha)

# 2. Regex Extraction and Replacement
all_text = " ".join(df["Ticket_Text"].tolist())

words_gt_5 = re.findall(r'\b[a-zA-Z]{6,}\b', all_text)
numbers = re.findall(r'\b\d+(?:\.\d+)*\b', all_text)
cap_words = re.findall(r'\b[A-Z][a-zA-Z]*\b', all_text)
vowel_words = re.findall(r'\b[aeiouAEIOU][a-zA-Z]*\b', all_text)

print("Words > 5 chars:", sorted(list(set(words_gt_5))))
print("Numbers:", numbers)
print("Capitalized words:", Counter(cap_words))
print("Vowel starting words:", Counter(vowel_words))

TEST_LINES = [
    "Mail it.helpdesk@thapar.edu or a.b-c@dept.univ.ac.in; visit https://lms.thapar.edu/help or www.thapar.edu/it.",
    "Call +91 98765 43210, +91-98765-43210 or 0175-239-3201. Version 2.0.1 is 95.5% done; fee Rs 1,250.",
    "The state-of-the-art lab isn't open; log-in at 5.30 p.m. didn't work.",
]

email_re = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
url_re = r'https?://[a-zA-Z0-9_./-]+(?<![.,;])|www\.[a-zA-Z0-9_./-]+(?<![.,;])'
phone_re = r'\+?\d{1,3}[- ]?\d{5}[- ]?\d{5}|\d{4}-\d{3}-\d{4}'

for line in TEST_LINES:
    cleaned = re.sub(email_re, '<EMAIL>', line)
    cleaned = re.sub(url_re, '<URL>', cleaned)
    cleaned = re.sub(phone_re, '<PHONE>', cleaned)
    print(cleaned)

# 3. Custom Tokenizer
custom_pattern = r'''(?x)
    (?:https?://|www\.)[a-zA-Z0-9_./-]+(?<![.,;:])
    | [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+
    | (?:\+\d{1,3}[- ]?)?\d{5}[- ]?\d{5}|\d{4}-\d{3}-\d{4}
    | \b\d+(?:\.\d+)+\b
    | \b[A-Za-z]+(?:-[A-Za-z]+)+\b
    | \b[A-Za-z]+['’][A-Za-z]+\b
    | \b\d{1,3}(?:,\d{3})+\b
    | \b\w+\b
    | [^\s\w]
'''

my_tokenizer = RegexpTokenizer(custom_pattern)
def my_tokenize(text):
    return my_tokenizer.tokenize(text)

for line in TEST_LINES:
    print("my_tokenize:", my_tokenize(line))
    print("word_tokenize:", word_tokenize(line))

# 4. Stemming and Lemmatization
unique_final_tokens = sorted(list(set(all_final_tokens)))
porter = PorterStemmer()
lancaster = LancasterStemmer()
regexp_stemmer = RegexpStemmer('ing$', min=4)
wnl = WordNetLemmatizer()

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN

pos_tagged = pos_tag(unique_final_tokens)
q4_rows = []

for word, tag in pos_tagged:
    p = porter.stem(word)
    l = lancaster.stem(word)
    r = regexp_stemmer.stem(word)
    w = wnl.lemmatize(word, get_wordnet_pos(tag))
    if len({p, l, r, w}) > 1:
        q4_rows.append({"Word": word, "POS": tag, "Porter": p, "Lancaster": l, "Regexp": r, "WordNet": w})

q4_df = pd.DataFrame(q4_rows)
print(q4_df)

# 5. Corpus Statistics & Zipf's Law
s1 = [t for res in processed_dict.values() for t in res["tokens"]]
s2 = [t for res in processed_dict.values() for t in res["tokens"] if not is_punct(t)]
s3 = [t for res in processed_dict.values() for t in res["final"]]
s4 = [porter.stem(t) for t in s3]

def calc_ttr(t_list):
    total = len(t_list)
    unique = len(set(t_list))
    return total, unique, (unique / total) if total > 0 else 0

stats_df = pd.DataFrame({
    "Corpus": ["S1", "S2", "S3", "S4"],
    "Total": [calc_ttr(s1)[0], calc_ttr(s2)[0], calc_ttr(s3)[0], calc_ttr(s4)[0]],
    "Unique": [calc_ttr(s1)[1], calc_ttr(s2)[1], calc_ttr(s3)[1], calc_ttr(s4)[1]],
    "TTR": [calc_ttr(s1)[2], calc_ttr(s2)[2], calc_ttr(s3)[2], calc_ttr(s4)[2]]
})
print(stats_df)

print("Top 10 S1:", Counter(s1).most_common(10))
print("Top 10 S3:", Counter(s3).most_common(10))
print("Top 5 Bigrams S1:", Counter(list(nltk.bigrams(s1))).most_common(5))
print("Top 5 Bigrams S3:", Counter(list(nltk.bigrams(s3))).most_common(5))

s3_counts = Counter(s3)
sorted_freqs = sorted(s3_counts.values(), reverse=True)
ranks = np.arange(1, len(sorted_freqs) + 1)
freqs = np.array(sorted_freqs)

log_ranks = np.log10(ranks)
log_freqs = np.log10(freqs)
slope, intercept = np.polyfit(log_ranks, log_freqs, 1)

plt.figure(figsize=(8, 5))
plt.plot(log_ranks, log_freqs, marker='o', label='S3 Tokens')
plt.plot(log_ranks, slope * log_ranks + intercept, 'r--', label=f'Fit (Slope = {slope:.2f})')
plt.title("Zipf's Law: log(Rank) vs log(Frequency)")
plt.xlabel("log10(Rank)")
plt.ylabel("log10(Frequency)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "log_rank_frequency_s3.png"))
plt.close()
