import os
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd
import spacy
from spacy.language import Language

from spacy_language_detection import LanguageDetector

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)  # We use the seed 42


nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)


def annotate_and_save(sub_dir, filename_in, filenam_out):
    df = pd.read_json("data/{}/{}.json".format(sub_dir, filename_in))
    df["lang"] = df.apply(lambda row: nlp(row["text"])._.language["language"], axis=1)
    df = df[df.lang == "en"]
    df["sentiment"] = df.apply(lambda row: sia.polarity_scores(row["text"])["compound"], axis=1)
    df[["created_at", "text", "sentiment"]].to_csv("data/{}/{}.csv".format(sub_dir, filenam_out), index=False)


for subdir in os.listdir("data"):
    if "scoredpregnancytweets.csv" not in os.listdir("data/{}".format(subdir)):
        annotate_and_save(subdir, "pregnancytweets", "scoredpregnancytweets")
        annotate_and_save(subdir, "alltweets", "scoredalltweets")
