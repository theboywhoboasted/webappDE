import pandas as pd
from pathlib import Path
import random

DATA_DIR = Path("./data/")


def get_verb_to_test():
    verbs_file = DATA_DIR / "verbs.csv"
    verbs_df = pd.read_csv(verbs_file)
    selected_row = verbs_df.sample(1).iloc[0]
    return selected_row["word"], selected_row["meaning"]


def check_verb(args):
    verbs_file = DATA_DIR / "verbs.csv"
    verbs_df = pd.read_csv(verbs_file)
    word = args["word"]
    row = verbs_df.loc[verbs_df["word"] == word].iloc[0]
    if row["hilfsverb"] == "sein":
        correct_hilfsverb = "bin"
    else:
        correct_hilfsverb = "habe"
    outputs = {
        "verb": word,
        "meaning": row["meaning"],
        "ich": args["ich"].strip().lower(),
        "correct_ich": row["ich"],
        "du": args["du"].strip().lower(),
        "correct_du": row["du"],
        "hilfsverb": args["hilfsverb"].strip().lower(),
        "correct_hilfsverb": correct_hilfsverb,
        "partizip": args["partizip"].strip().lower(),
        "correct_partizip": row["partizip"],
    }
    return outputs


def get_nouns_to_test(n):
    nouns_file = DATA_DIR / "nouns.csv"
    nouns_df = pd.read_csv(nouns_file)
    selected_rows = nouns_df.sample(n).reset_index(drop=True)
    return selected_rows["word"].tolist()


def check_noun(args, n):
    nouns_file = DATA_DIR / "nouns.csv"
    nouns_df = pd.read_csv(nouns_file)
    outputs = []
    for i in range(1, n + 1):
        word = args[f"word{i}"]
        article = args[f"article{i}"]
        row = nouns_df.loc[nouns_df["word"] == word].iloc[0]
        correct_article = row["article"]
        meaning = row["meaning"]
        plural = "-" if (row["plural"] == "-") else ("die " + row["plural"])
        outputs.append(
            (correct_article.lower(), article.lower(), word, meaning, plural)
        )
    return outputs


def get_words_to_test(style, n):
    words_file = DATA_DIR / f"{style}.csv"
    words_df = pd.read_csv(words_file)
    selected_rows = words_df.sample(n).reset_index(drop=True)
    meanings = selected_rows["meaning"].tolist()
    random.shuffle(meanings)
    if style == "nouns":
        return (
            selected_rows.apply(
                lambda x: x["article"].lower() + " " + x["word"].title(), axis=1
            ).tolist(),
            meanings,
        )
    else:
        return selected_rows["word"].str.lower().tolist(), meanings


def check_vocab(args, style, n):
    words_file = DATA_DIR / f"{style}.csv"
    words_df = pd.read_csv(words_file)
    outputs = []
    for i in range(1, n + 1):
        word = args[f"word{i}"]
        meaning = args[f"meaning{i}"]
        if style == "nouns":
            lookup_word = " ".join(word.split(" ")[1:]).lower()
        else:
            lookup_word = word.lower()
        row = words_df.loc[words_df["word"].str.lower() == lookup_word].iloc[0]
        correct_meaning = row["meaning"]
        outputs.append((word, meaning, correct_meaning))
    return outputs
