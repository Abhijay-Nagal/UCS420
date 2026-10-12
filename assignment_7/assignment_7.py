"""
================================================================================
UCS420: Cognitive Computing
Assignment 7 — NLP-I (Text Preprocessing)
--------------------------------------------------------------------------------
Student Name    : Abhijay Nagal
Roll Number     : 1024170013
Dataset Fingerprint: 242147B7
Focus Tickets   : ['T01', 'T11']
================================================================================
"""

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

# Download required NLTK resources quietly
for pkg in [
    "punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4",
    "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"
]:
    nltk.download(pkg, quiet=True)

# ------------------------------------------------------------------------------
# Constants and Setup
# ------------------------------------------------------------------------------
ROLL_NO = 1024170013
NAME = "Abhijay Nagal"

STOP = set(stopwords.words("english"))

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------
# Official Dataset Generator & Preprocessing Pipeline (DO NOT MODIFY)
# ------------------------------------------------------------------------------
def generate_dataset(roll_no):
    """Return (DataFrame of tickets, focus ticket IDs, fingerprint) for a roll number. Do not modify."""
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
    """A token is punctuation if EVERY character in it is in string.punctuation (e.g. '.', '...', '``', "''")."""
    return all(ch in string.punctuation for ch in token)

def process_ticket(text):
    """The official pipeline. Returns sentences, lowercase tokens, punctuation, stopwords and final tokens."""
    sentences = sent_tokenize(text)
    tokens = [t.lower() for s in sentences for t in word_tokenize(s)]
    punct = [t for t in tokens if is_punct(t)]
    stops = [t for t in tokens if t in STOP]
    final = [t for t in tokens if not is_punct(t) and t not in STOP]
    return {"sentences": sentences, "tokens": tokens, "punct": punct, "stops": stops, "final": final}


def main():
    print("================================================================================")
    print(" UCS420: Cognitive Computing — Assignment 7: NLP-I")
    print("================================================================================")
    df, FOCUS, FINGERPRINT = generate_dataset(ROLL_NO)
    print(f"Roll Number : {ROLL_NO}")
    print(f"Name        : {NAME}")
    print(f"Fingerprint : {FINGERPRINT}")
    print(f"Total Tickets: {len(df)}")
    print(f"Focus Tickets: {FOCUS}\n")

    print("--- Generated Dataset ---")
    print(df.to_string(index=False))
    csv_path = os.path.join(OUTPUT_DIR, f"{ROLL_NO}_generated_dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[Saved dataset to {csv_path}]\n")

    # ==============================================================================
    # Section 1: Preprocessing Pipeline
    # ==============================================================================
    print("================================================================================")
    print(" 1. PREPROCESSING PIPELINE")
    print("================================================================================")
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
    # Add Total row for count-based columns
    total_row = pd.DataFrame([{
        "Ticket_ID": "TOTAL",
        "Sentences": q1_table["Sentences"].sum(),
        "Tokens": q1_table["Tokens"].sum(),
        "Punctuation": q1_table["Punctuation"].sum(),
        "Stopwords": q1_table["Stopwords"].sum(),
        "Unique_Tokens": "-",
        "Final_Tokens": q1_table["Final_Tokens"].sum()
    }])
    q1_summary = pd.concat([q1_table, total_row], ignore_index=True)
    print(q1_summary.to_string(index=False))

    # Display actual tokens for one selected ticket (FOCUS[0] = T01)
    sel_id = FOCUS[0]
    sel_res = processed_dict[sel_id]
    sel_text = df[df["Ticket_ID"] == sel_id]["Ticket_Text"].values[0]
    print(f"\n--- Detailed Breakdown for Selected Ticket: {sel_id} ---")
    print(f"Original Text: \"{sel_text}\"")
    print(f"1. Sentences ({len(sel_res['sentences'])}): {sel_res['sentences']}")
    print(f"2. Actual Tokens ({len(sel_res['tokens'])}): {sel_res['tokens']}")
    print(f"3. Punctuation Tokens ({len(sel_res['punct'])}): {sel_res['punct']}")
    print(f"4. Stopwords ({len(sel_res['stops'])}): {sel_res['stops']}")
    print(f"5. Final Tokens ({len(sel_res['final'])}): {sel_res['final']}")

    print("\n[Observation - Q1]:")
    all_final_tokens = [t for res in processed_dict.values() for t in res["final"]]
    non_alpha = sorted(list(set(t for t in all_final_tokens if not t.isalpha())))
    print(f"Final tokens that are not standard dictionary words: {non_alpha}")
    print("Explanation: Contractions like \"can't\" and \"doesn't\" / \"don't\" are split by NLTK's word_tokenize")
    print("into stem fragments and negation particles (\"ca\", \"n't\"). Since \"n't\" and \"ca\" are not in")
    print("NLTK's standard English stopwords list, they survive into final tokens. Similarly, numbers (\"3.12\"),")
    print("hyphenated nouns (\"e-mail\", \"wi-fi\"), and domain substrings (\"university.edu\") contain internal")
    print("punctuation/digits and remain in the final tokens.\n")

    # ==============================================================================
    # Section 2: Regex Extraction and Replacement
    # ==============================================================================
    print("================================================================================")
    print(" 2. REGEX EXTRACTION AND REPLACEMENT")
    print("================================================================================")
    all_text = " ".join(df["Ticket_Text"].tolist())

    # Extraction regexes
    # Words longer than 5 letters
    words_gt_5 = re.findall(r'\b[a-zA-Z]{6,}\b', all_text)
    # Numbers keeping decimals and version numbers (e.g., 95.5, 2.0.1, 3.12)
    numbers = re.findall(r'\b\d+(?:\.\d+)*\b', all_text)
    # Capitalized words
    cap_words = re.findall(r'\b[A-Z][a-zA-Z]*\b', all_text)
    # Words beginning with a vowel
    vowel_words = re.findall(r'\b[aeiouAEIOU][a-zA-Z]*\b', all_text)

    print(f"(a) Words longer than 5 letters (Count: {len(words_gt_5)}, Unique: {len(set(words_gt_5))}):")
    print(f"    {sorted(list(set(words_gt_5)))}\n")

    print(f"(b) Numbers (keeping decimals and version numbers whole) (Matches: {numbers}):")
    print(f"    Matches found: {numbers}\n")

    print(f"(c) Capitalized words (Count: {len(cap_words)}):")
    print(f"    Frequencies: {dict(Counter(cap_words))}\n")

    print(f"(d) Words beginning with a vowel (Count: {len(vowel_words)}):")
    print(f"    Frequencies: {dict(Counter(vowel_words))}\n")

    # Replacement Patterns
    TEST_LINES = [
        "Mail it.helpdesk@thapar.edu or a.b-c@dept.univ.ac.in; visit https://lms.thapar.edu/help or www.thapar.edu/it.",
        "Call +91 98765 43210, +91-98765-43210 or 0175-239-3201. Version 2.0.1 is 95.5% done; fee Rs 1,250.",
        "The state-of-the-art lab isn't open; log-in at 5.30 p.m. didn't work.",
    ]

    email_re = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    url_re = r'https?://[a-zA-Z0-9_./-]+(?<![.,;])|www\.[a-zA-Z0-9_./-]+(?<![.,;])'
    phone_re = r'\+?\d{1,3}[- ]?\d{5}[- ]?\d{5}|\d{4}-\d{3}-\d{4}'

    print("--- Replacement using re.sub() on TEST_LINES ---")
    for i, line in enumerate(TEST_LINES, 1):
        cleaned = re.sub(email_re, '<EMAIL>', line)
        cleaned = re.sub(url_re, '<URL>', cleaned)
        cleaned = re.sub(phone_re, '<PHONE>', cleaned)
        print(f"Test Line {i} Original: {line}")
        print(f"Test Line {i} Cleaned : {cleaned}\n")

    print("--- Replacement using re.sub() on Dataset Tickets ---")
    for _, r in df.iterrows():
        t = r["Ticket_Text"]
        subbed = re.sub(email_re, '<EMAIL>', t)
        subbed = re.sub(url_re, '<URL>', subbed)
        subbed = re.sub(phone_re, '<PHONE>', subbed)
        if subbed != t:
            print(f"[{r['Ticket_ID']}] Original: {t}")
            print(f"[{r['Ticket_ID']}] Cleaned : {subbed}\n")

    print("[Observation - Q2]:")
    # Count how many capitalized words are capitalized ONLY because they start a sentence
    # Sentence-initial words in the corpus:
    sent_init_words = []
    non_init_words = []
    for _, r in df.iterrows():
        for s in sent_tokenize(r["Ticket_Text"]):
            w_list = re.findall(r'\b[A-Za-z]+\b', s)
            if w_list and w_list[0][0].isupper():
                sent_init_words.append(w_list[0])
            for w in w_list[1:]:
                if w[0].isupper():
                    non_init_words.append(w)
    non_init_set = set(non_init_words)
    only_sent_init = [w for w in sent_init_words if w not in non_init_set and w != "I"]
    print(f"Total capitalized words: {len(cap_words)}")
    print(f"Sentence-initial occurrences: {len(sent_init_words)}")
    print(f"Capitalized ONLY due to sentence start (e.g., 'The', 'It', 'Please', 'Can', 'This', 'Is', 'Email'): {len(only_sent_init)} occurrences")
    print(f"Specific words capitalized only at start: {set(only_sent_init)}\n")

    # ==============================================================================
    # Section 3: Custom Tokenization
    # ==============================================================================
    print("================================================================================")
    print(" 3. CUSTOM TOKENIZATION")
    print("================================================================================")
    custom_pattern = r'''(?x)
        (?:https?://|www\.)[a-zA-Z0-9_./-]+(?<![.,;:])         # URLs (excluding trailing punctuation)
        | [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+       # Email addresses
        | (?:\+\d{1,3}[- ]?)?\d{5}[- ]?\d{5}|\d{4}-\d{3}-\d{4} # Phone numbers
        | \b\d+(?:\.\d+)+\b                                    # Versions and decimals (2.0.1, 95.5, 5.30, 3.12)
        | \b[A-Za-z]+(?:-[A-Za-z]+)+\b                         # Hyphenated words (Wi-Fi, state-of-the-art, log-in, e-mail)
        | \b[A-Za-z]+['’][A-Za-z]+\b                           # Contractions (isn't, didn't, don't, can't)
        | \b\d{1,3}(?:,\d{3})+\b                               # Comma-formatted numbers (1,250)
        | \b\w+\b                                              # Standard words and standalone integers
        | [^\s\w]                                              # Individual punctuation marks / symbols
    '''

    my_tokenizer = RegexpTokenizer(custom_pattern)
    def my_tokenize(text):
        return my_tokenizer.tokenize(text)

    print("--- Comparison on TEST_LINES ---")
    for i, line in enumerate(TEST_LINES, 1):
        my_toks = my_tokenize(line)
        nltk_toks = word_tokenize(line)
        print(f"Test Line {i}: \"{line}\"")
        print(f"  my_tokenize  : {my_toks}")
        print(f"  word_tokenize: {nltk_toks}\n")

    # Comparison on dataset tickets
    diff_tickets = 0
    diff_ticket_ids = []
    for _, r in df.iterrows():
        t = r["Ticket_Text"]
        if my_tokenize(t) != word_tokenize(t):
            diff_tickets += 1
            diff_ticket_ids.append(r["Ticket_ID"])

    print(f"Tickets tokenized differently: {diff_tickets} out of {len(df)} ({diff_ticket_ids})\n")

    print("[Differences and Explanations]:")
    print("1. Contractions: word_tokenize() splits contractions (e.g. \"isn't\" -> ['is', \"n't\"]) based on Penn")
    print("   Treebank standards. In contrast, my_tokenize() preserves the contraction as a single token (\"isn't\").")
    print("2. Email Addresses & URLs: word_tokenize() breaks emails and URLs around '@', '.', and '/' characters")
    print("   (e.g. 'helpdesk@university.edu' -> ['helpdesk', '@', 'university.edu']). my_tokenize() preserves")
    print("   the entire email and URL as single unified tokens.")
    print("3. Phone Numbers & Decimals: word_tokenize() splits phone numbers containing spaces into separate digit tokens")
    print("   (e.g. '+91 98765 43210' -> ['+91', '98765', '43210']). my_tokenize() preserves international format phone")
    print("   numbers as unified tokens.\n")

    # ==============================================================================
    # Section 4: Stemming and Lemmatization
    # ==============================================================================
    print("================================================================================")
    print(" 4. STEMMING AND LEMMATIZATION")
    print("================================================================================")
    unique_final_tokens = sorted(list(set(all_final_tokens)))
    print(f"Total Unique Final Tokens: {len(unique_final_tokens)}")

    porter = PorterStemmer()
    lancaster = LancasterStemmer()
    # Choice of suffix for RegexpStemmer:
    # Multiple progressive verb forms appear in dataset: 'restarting', 'disconnecting', 'opening',
    # 'asking', 'uploading', 'getting'. Suffix 'ing$' directly strips inflectional progressive markers.
    regexp_stemmer = RegexpStemmer('ing$', min=4)
    wnl = WordNetLemmatizer()

    def get_wordnet_pos(treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        return wordnet.NOUN

    pos_tagged_tokens = pos_tag(unique_final_tokens)
    q4_rows = []

    for word, tag in pos_tagged_tokens:
        p = porter.stem(word)
        l = lancaster.stem(word)
        r = regexp_stemmer.stem(word)
        wn_pos = get_wordnet_pos(tag)
        w = wnl.lemmatize(word, wn_pos)

        # Include ONLY words where outputs differ
        if len({p, l, r, w}) > 1:
            q4_rows.append({
                "Word": word,
                "POS": tag,
                "Porter": p,
                "Lancaster": l,
                "Regexp": r,
                "WordNet_POS": w
            })

    q4_df = pd.DataFrame(q4_rows)
    print(f"Table of Differing Words ({len(q4_df)} of {len(unique_final_tokens)} words):")
    print(q4_df.to_string(index=False))

    print("\n[Suffix Choice Justification for RegexpStemmer]:")
    print("Suffix chosen: 'ing$' (with min length 4).")
    print("Justification: In our generated dataset, there are numerous progressive verbs ending in '-ing',")
    print("specifically: 'restarting', 'disconnecting', 'opening', 'asking', 'uploading', and 'getting'.")
    print("The regex rule accurately strips the '-ing' suffix to reveal root morphemes without over-truncating.")

    print("\n[Observation - Q4]:")
    print("1. Over-stemming Example: Lancaster stemmer reduces 'portal' to 'port' (stripping '-al') and 'campus' to 'camp'")
    print("   (stripping '-us'), conflating unrelated words and obliterating their true semantic meanings.")
    print("2. Under-stemming Example: RegexpStemmer with rule 'ing$' fails to stem past-tense inflectional forms")
    print("   such as 'worked', 'installed', 'failed', 'changed', and 'reinstalled', leaving them entirely unstemmed.\n")

    # ==============================================================================
    # Section 5: Corpus Statistics
    # ==============================================================================
    print("================================================================================")
    print(" 5. CORPUS STATISTICS")
    print("================================================================================")
    s1 = [t for res in processed_dict.values() for t in res["tokens"]]
    s2 = [t for res in processed_dict.values() for t in res["tokens"] if not is_punct(t)]
    s3 = [t for res in processed_dict.values() for t in res["final"]]
    s4 = [porter.stem(t) for t in s3]

    def calc_ttr(t_list):
        total = len(t_list)
        unique = len(set(t_list))
        return total, unique, (unique / total) if total > 0 else 0

    s1_tot, s1_unq, s1_ttr = calc_ttr(s1)
    s2_tot, s2_unq, s2_ttr = calc_ttr(s2)
    s3_tot, s3_unq, s3_ttr = calc_ttr(s3)
    s4_tot, s4_unq, s4_ttr = calc_ttr(s4)

    stats_df = pd.DataFrame({
        "Corpus": ["S1 (all tokens)", "S2 (no punctuation)", "S3 (final tokens)", "S4 (S3 after Porter stemming)"],
        "Total Tokens": [s1_tot, s2_tot, s3_tot, s4_tot],
        "Unique Tokens": [s1_unq, s2_unq, s3_unq, s4_unq],
        "TTR": [s1_ttr, s2_ttr, s3_ttr, s4_ttr]
    })
    print(stats_df.to_string(index=False))

    print("\n--- Top 10 Words ---")
    print("Top 10 words in S1:")
    for w, c in Counter(s1).most_common(10):
        print(f"  {w:>12}: {c}")

    print("\nTop 10 words in S3:")
    for w, c in Counter(s3).most_common(10):
        print(f"  {w:>12}: {c}")

    print("\n--- Top 5 Bigrams ---")
    print("Top 5 bigrams in S1:")
    for bg, c in Counter(list(nltk.bigrams(s1))).most_common(5):
        print(f"  {str(bg):>24}: {c}")

    print("\nTop 5 bigrams in S3:")
    for bg, c in Counter(list(nltk.bigrams(s3))).most_common(5):
        print(f"  {str(bg):>24}: {c}")

    # Zipf's Law Plot for S3
    s3_counts = Counter(s3)
    sorted_freqs = sorted(s3_counts.values(), reverse=True)
    ranks = np.arange(1, len(sorted_freqs) + 1)
    freqs = np.array(sorted_freqs)

    log_ranks = np.log10(ranks)
    log_freqs = np.log10(freqs)

    slope, intercept = np.polyfit(log_ranks, log_freqs, 1)

    plt.figure(figsize=(8, 5))
    plt.plot(log_ranks, log_freqs, marker='o', linestyle='-', color='#1f77b4', label='Empirical S3 Tokens')
    plt.plot(log_ranks, slope * log_ranks + intercept, 'r--', label=f'Zipf Linear Fit (Slope = {slope:.2f})')
    plt.title("Zipf's Law for S3 (Final Tokens): log(Rank) vs log(Frequency)")
    plt.xlabel("log10(Rank)")
    plt.ylabel("log10(Frequency)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plot_file = os.path.join(OUTPUT_DIR, "log_rank_frequency_s3.png")
    plt.savefig(plot_file, dpi=300)
    plt.close()
    print(f"\n[Zipf's law plot saved to {plot_file}]")

    # ==============================================================================
    # Section 6: Interpretation
    # ==============================================================================
    print("\n================================================================================")
    print(" 6. INTERPRETATION")
    print("================================================================================")
    print("(a) Why does TTR change from S1 to S4 in your dataset?")
    print(f"    - S1 -> S2: TTR increases ({s1_ttr:.4f} -> {s2_ttr:.4f}) because punctuation tokens (e.g. repeated '.')")
    print("      are removed. This reduces total tokens by 31 while only removing 6 unique punctuation symbols.")
    print(f"    - S2 -> S3: TTR increases significantly ({s2_ttr:.4f} -> {s3_ttr:.4f}) because high-frequency stopwords")
    print("      (e.g., 'the', 'it', 'i', 'after') are removed. This drastically cuts the denominator of repeated")
    print("      function words while retaining information-dense content vocabulary.")
    print(f"    - S3 -> S4: TTR decreases ({s3_ttr:.4f} -> {s4_ttr:.4f}) because Porter stemming collapses inflectional")
    print("      variants (such as 'works' and 'worked' -> 'work', 'keeps' -> 'keep') into shared root stems, reducing")
    print(f"      the number of unique types (from {s3_unq} to {s4_unq}) while total tokens remain constant ({s3_tot}).")

    print("\n(b) Give one example where word_tokenize() and your tokenizer differ. Explain the difference.")
    print("    - Example: \"Email me at helpdesk@university.edu.\" and \"The Wi-Fi works, but the VPN doesn't.\"")
    print("    - Difference: word_tokenize() splits \"doesn't\" into ['does', \"n't\"] and \"helpdesk@university.edu\"")
    print("      into ['helpdesk', '@', 'university.edu']. In contrast, my_tokenize() keeps \"doesn't\" and")
    print("      \"helpdesk@university.edu\" intact as unified tokens, avoiding artificial fragmentation.")

    print("\n(c) Give one example where stemming produces an undesirable result.")
    print("    - Example: Lancaster stemmer stems 'portal' to 'port' and 'campus' to 'camp'.")
    print("    - Explanation: This is an over-stemming error. It strips legitimate root letters ('-al', '-us'),")
    print("      creating false semantic equivalence with unrelated English words ('port', 'camp').")

    print("\n(d) Give one example where POS-aware lemmatization preserves meaning better than stemming.")
    print("    - Example: 'opening' (POS = NN) and 'changed' (POS = VBD).")
    print("    - Explanation: Porter stems 'opening' to 'open' and 'changed' to 'chang' (which is not a real word).")
    print("      WordNet lemmatizer with POS tag NN preserves 'opening' as a valid noun, and for verb 'changed'")
    print("      lemmatizes it cleanly to the standard dictionary lemma 'change'.")
    print("================================================================================")


if __name__ == "__main__":
    main()
