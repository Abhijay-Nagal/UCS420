# UCS420: Cognitive Computing — Assignment 7: NLP-I

## Student Details
- **Student Name:** Abhijay Nagal
- **Roll Number:** 1024170013
- **Dataset Fingerprint:** `242147B7`
- **Total Tickets Generated:** 15
- **Focus Ticket IDs:** `['T01', 'T11']`

---

## Files in this Directory
- `UCS420_Assignment_7_NLP_I.ipynb`: Fully executed Jupyter Notebook with all outputs, code, observations, and Zipf's law plot.
- `assignment_7.py`: Standalone Python script running all steps end-to-end.
- `1024170013_generated_dataset.csv`: Exported generated ticket dataset.
- `log_rank_frequency_s3.png`: Log(rank) vs. log(frequency) plot for S3 tokens.

---

## Summary of Results

### 1. Preprocessing Pipeline (`process_ticket()`)
| Metric | Total across 15 Tickets |
|---|---|
| Sentences | 27 |
| Tokens | 191 |
| Punctuation | 31 |
| Stopwords | 69 |
| Final Tokens | 91 |

**Selected Ticket Display (T01):**
- **Text:** `E-mail keeps disconnecting after restarting the system. I don't know what changed.`
- **Actual Tokens (15):** `['e-mail', 'keeps', 'disconnecting', 'after', 'restarting', 'the', 'system', '.', 'i', 'do', "n't", 'know', 'what', 'changed', '.']`
- **Punctuation (2):** `['.', '.']`
- **Stopwords (5):** `['after', 'the', 'i', 'do', 'what']`
- **Final Tokens (8):** `['e-mail', 'keeps', 'disconnecting', 'restarting', 'system', "n't", 'know', 'changed']`

**Observation:**
- Non-standard word tokens in final tokens include `"n't"`, `"ca"`, `"3.12"`, `"e-mail"`, `"wi-fi"`, and `"university.edu"`. Contractions like `"don't"`, `"can't"`, `"doesn't"` are split into verb stems and `"n't"`/`"ca"` by Treebank tokenization rules. Since `"n't"` and `"ca"` are not present in the standard NLTK stopwords list, they survive into final tokens.

---

### 2. Regex Extraction and Replacement
- **Words > 5 letters:** Extracted 65 matches (38 unique words).
- **Numbers (keeping decimals and version numbers):** Matched `['3.12']`.
- **Capitalized words:** 35 matches.
- **Words beginning with a vowel:** 45 matches.
- **Replacement Patterns:**
  - Email addresses replaced with `<EMAIL>`
  - URLs replaced with `<URL>`
  - Phone numbers replaced with `<PHONE>`
  - Successfully verified on provided `TEST_LINES` and dataset tickets.

**Observation:**
- Out of 35 capitalized words, **16 words** (`The`, `It`, `Please`, `Email`, `Can`, `This`, `Is`, `Pls`) are capitalized solely because they appear at the start of a sentence.

---

### 3. Custom Tokenization (`my_tokenize()`)
- Implemented with a single `RegexpTokenizer` pattern that preserves:
  - Contractions: `isn't`, `didn't`, `don't`, `can't`
  - Hyphenated words: `Wi-Fi`, `state-of-the-art`, `log-in`, `e-mail`
  - Decimals: `95.5`, `5.30`
  - Versions: `2.0.1`, `3.12`
  - Email addresses: `helpdesk@university.edu`, `it.helpdesk@thapar.edu`
  - URLs: `https://lms.thapar.edu/help`, `www.thapar.edu/it`
  - Phone numbers: `+91 98765 43210`, `+91-98765-43210`, `0175-239-3201`
- **Differing Tickets:** 5 out of 15 tickets (`T01`, `T02`, `T04`, `T10`, `T14`) differ from `word_tokenize()`.

**Key Differences:**
1. **Contractions:** `word_tokenize()` splits contractions into two tokens (`"isn't"` -> `['is', "n't"]`), whereas `my_tokenize()` keeps them whole (`"isn't"`).
2. **Emails & URLs:** `word_tokenize()` splits around `@`, `:`, and `/`, whereas `my_tokenize()` keeps emails and URLs unified.
3. **Phone Numbers:** `word_tokenize()` breaks telephone numbers with spaces into multiple tokens, whereas `my_tokenize()` keeps them unified.

---

### 4. Stemming and Lemmatization
- Compared **Porter Stemmer**, **Lancaster Stemmer**, **Regexp Stemmer** (`'ing$'`, min length 4), and **WordNet Lemmatizer** with POS tags.
- Suffix choice for Regexp Stemmer: `'ing$'` based on multiple progressive verb forms in the dataset (`restarting`, `disconnecting`, `opening`, `asking`, `uploading`, `getting`).
- **33 out of 57 unique final tokens** produced differing outputs across the four techniques.

**Observations:**
- **Over-stemming Example:** Lancaster stemmer reduces `portal` -> `port` and `campus` -> `camp`, conflating distinct lexical concepts.
- **Under-stemming Example:** RegexpStemmer fails to stem past-tense inflectional forms (`worked`, `installed`, `changed`, `failed`) because its rule is restricted to `'ing$'`.

---

### 5. Corpus Statistics
| Corpus | Description | Total Tokens | Unique Tokens | TTR (Type-Token Ratio) |
|---|---|---|---|---|
| **S1** | All tokens | 191 | 90 | 0.4712 |
| **S2** | Tokens without punctuation | 160 | 84 | 0.5250 |
| **S3** | Final tokens (no stopwords / punct) | 91 | 57 | 0.6264 |
| **S4** | S3 after Porter stemming | 91 | 54 | 0.5934 |

- **Top words in S1:** `.` (24), `the` (19), `it` (8), `i` (7), `restarting` (5), `after` (3), `system` (3), `n't` (3), `matlab` (3), `works` (3)
- **Top words in S3:** `restarting` (5), `system` (3), `n't` (3), `matlab` (3), `works` (3), `please` (3), `resolve` (3), `yesterday` (3), `keeps` (2), `tried` (2)
- **Top bigrams in S1:** `('.', 'i')`: 7, `('restarting', 'the')`: 5, `('.', 'it')`: 4, `('.', 'the')`: 4, `('after', 'restarting')`: 3
- **Top bigrams in S3:** `('restarting', 'system')`: 3, `('please', 'resolve')`: 3, `('tried', 'restarting')`: 2, `('assignment', 'deadline')`: 2, `('works', 'another')`: 2
- **Zipf Plot for S3:** Linear regression slope = -0.46, intercept = 0.78.

---

### 6. Interpretation
**(a) Why does TTR change from S1 to S4?**
- S1 to S2 increases (0.4712 -> 0.5250) because non-word punctuation tokens (like 24 periods) are dropped, shrinking total tokens faster than types.
- S2 to S3 jumps to 0.6264 because repetitive grammatical stopwords (`the`, `it`, `i`, `after`) are removed, leaving a higher concentration of unique content words.
- S3 to S4 decreases (0.6264 -> 0.5934) because Porter stemming maps inflected word forms (`works` and `worked` -> `work`, `keeps` -> `keep`) into the same root stem, decreasing the number of unique types (57 -> 54) for the same 91 total tokens.

**(b) Example where `word_tokenize()` and custom tokenizer differ:**
- `"The Wi-Fi works, but the VPN doesn't."`
- `word_tokenize()` produces `['The', 'Wi-Fi', 'works', ',', 'but', 'the', 'VPN', 'does', "n't", '.']`
- `my_tokenize()` produces `['The', 'Wi-Fi', 'works', ',', 'but', 'the', 'VPN', "doesn't", '.']`

**(c) Example where stemming produces an undesirable result:**
- Lancaster Stemmer reduces `"portal"` to `"port"` and `"campus"` to `"camp"`, stripping valid word endings and distorting meaning.

**(d) Example where POS-aware lemmatization preserves meaning better than stemming:**
- For `"opening"` (noun in `"crashes while opening"`), Porter stemmer blindly chops `-ing` to produce the verb `"open"`, whereas WordNet Lemmatizer with POS `NOUN` retains `"opening"`. For `"changed"`, WordNet yields the clean dictionary lemma `"change"`, whereas Porter yields the truncated non-word `"chang"`.
