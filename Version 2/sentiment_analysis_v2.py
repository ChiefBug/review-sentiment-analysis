import nltk
from textblob import TextBlob
from nltk.tokenize import WhitespaceTokenizer
import pandas as pd
from collections import defaultdict
from tqdm.auto import tqdm


df = pd.read_csv(
    'C:/Users/shing/Documents/Semester_3/Research Sentiment Analysis/Main/Version 2/scraper_v2/B000GAYQKY.csv',
    usecols=['Link', 'User', 'Date', 'Stars', 'Title', 'Text'])
df.drop(columns=['User', 'Date', 'Stars', 'Title'], inplace=True)
output_file = pd.DataFrame()


def create_tokens(review_text):
    tokens = WhitespaceTokenizer().tokenize(review_text)
    tokens = nltk.pos_tag(tokens)
    return tokens


def sentiment_analysis(review, link):
    res = {}

    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    def get_polarity(text):
        return TextBlob(text).sentiment.polarity

    def analysis(pol):
        if pol < 0:
            return 'Negative'
        elif pol == 0:
            return 'Neutral'
        else:
            return 'Positive'

    sub = get_subjectivity(review)
    pol = get_polarity(review)
    score = analysis(pol)
    res[review] = {'Link': link, 'Subjectivity': sub, 'Polarity': pol, 'Score': score}
    return res


def analyze_verbs(df):
    filename = 'verb_analysis.csv'
    data = defaultdict(dict)
    for review in tqdm(df.itertuples(index=False)):
        if type(review.Text) is str:
            tokens = create_tokens(review.Text)
        else:
            tokens = create_tokens(str(review.Text))
        for i in range(len(tokens)):
            text, tag = tokens[i]
            if tag in ("VBZ", "VBD", "VBG", "VBP", "VBN"):
                data.update(sentiment_analysis(text, review.Link))
    create_file(data, filename)


def analyze_adverbs(df):
    filename = 'adverb_analysis.csv'
    data = defaultdict(dict)
    for review in tqdm(df.itertuples(index=False)):
        if type(review.Text) is str:
            tokens = create_tokens(review.Text)
        else:
            tokens = create_tokens(str(review.Text))
        for i in range(len(tokens)):
            text, tag = tokens[i]
            if tag in ("RB", "RBR", "RBS"):
                data.update(sentiment_analysis(text, review.Link))
    create_file(data, filename)


def analyze_adjectives(df):
    filename = 'adjective_analysis.csv'
    data = defaultdict(dict)
    for review in tqdm(df.itertuples(index=False)):
        if type(review.Text) is str:
            tokens = create_tokens(review.Text)
        else:
            tokens = create_tokens(str(review.Text))
        for i in range(len(tokens)):
            text, tag = tokens[i]
            if tag in ("JJ", "JJR", "JJS"):
                data.update(sentiment_analysis(text, review.Link))
    create_file(data, filename)


def analyze_sentences(df):
    filename = 'sentence_analysis.csv'
    data = defaultdict(dict)
    for review in tqdm(df.itertuples(index=False)):
        if type(review.Text) is str:
            sentences = review.Text.split('.')
        else:
            sentences = str(review.Text).split('.')
        for sentence in sentences:
            data.update(sentiment_analysis(sentence, review.Link))
    create_file(data, filename)


def analyze_review(df):
    filename = 'review_analysis.csv'
    data = defaultdict(dict)
    for review in tqdm(df.itertuples(index=False)):
        if type(review.Text) is str:
            data.update(sentiment_analysis(review.Text, review.Link))
        else:
            data.update(sentiment_analysis(str(review.Text), review.Link))
    create_file(data, filename)


def create_file(data, filename):
    formatted_data = pd.DataFrame.from_dict(data)
    analysis_res = pd.concat([output_file, formatted_data])
    analysis_res = analysis_res.T
    analysis_res.to_csv(filename)


analyze_verbs(df)
analyze_adverbs(df)
analyze_adjectives(df)
analyze_sentences(df)
analyze_review(df)
