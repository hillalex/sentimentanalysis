from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd

import spacy
from spacy.language import Language

from spacy_language_detection import LanguageDetector

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


def get_lang_detector():
    return LanguageDetector(seed=42)  # We use the seed 42


nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)


def main():
    preg_df = pd.read_json("../data/pregnancytweets.json")
    preg_df["sentiment"] = preg_df.apply(lambda row: sia.polarity_scores(row["text"])["compound"], axis=1)
    preg_df["lang"] = preg_df.apply(lambda row: nlp(row["text"])._.language["language"], axis=1)
    preg_df[["created_at", "text", "sentiment", "lang"]].to_csv("data/scoredpregnancytweets.csv", index=False)

    df = pd.read_json("../data/alltweets.json")
    df["sentiment"] = df.apply(lambda row: sia.polarity_scores(row["text"])["compound"], axis=1)
    df["lang"] = df.apply(lambda row: nlp(row["text"])._.language["language"], axis=1)
    df[["created_at", "text", "sentiment", "lang"]].to_csv("data/scoredalltweets.csv", index=False)


if __name__ == "__main__":
    main()
