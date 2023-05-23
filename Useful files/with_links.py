import nltk
from textblob import TextBlob
from nltk.tokenize import WhitespaceTokenizer
import pandas as pd
from collections import defaultdict
from tqdm.auto import tqdm

# df = pd.read_csv('C:/Users/shing/Documents/Semester_3/Research Sentiment Analysis/Reviews/v2_B000GAYQKY.csv', usecols=['User', 'Date', 'Stars', 'Title', 'Text'])
df = pd.read_csv('C:/Users/shing/Documents/Semester_3/Research Sentiment Analysis/Reviews/B000GAYQKY_with_links.csv', usecols=['Link', 'User', 'Date', 'Stars', 'Title', 'Text'])
# review_lst = df['Text'].astype(str)
with_links = df.iloc[:, 0::5].values.tolist()
output_file = pd.DataFrame()


def create_tokens(review_text):
    tokens = WhitespaceTokenizer().tokenize(review_text)
    tokens = nltk.pos_tag(tokens)
    return tokens


def sentiment_analysis(review):
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
    res[review] = {'Subjectivity': sub, 'Polarity': pol, 'Score': score}
    return res


def analyze_verbs(with_links):
    filename = 'verb_analysis.csv'
    data = defaultdict(dict)
    for review in tqdm(with_links):
        try:
            tokens = create_tokens(review[1])
        except Exception:
            print("Null")
        for i in range(len(tokens)):
            text, tag = tokens[i]
            if tag in ("VBZ", "VBD", "VBG", "VBP", "VBN"):
                data.update(sentiment_analysis(text))
                data.get(text).update({"Link": review[0]})
    create_file(data, filename)


def analyze_sentences(with_links):
    filename = 'sentence_analysis.csv'
    data = defaultdict(dict)
    for review in tqdm(with_links):
        try:
            sentences = review[1].split('.')
        except Exception:
            print("Null")
        for sentence in sentences:
            data.update(sentiment_analysis(sentence))
            data.get(sentence).update({"Link": review[0]})
    create_file(data, filename)


def analyze_review(with_links):
    filename = 'review_analysis.csv'
    data = defaultdict(dict)
    for review in tqdm(with_links):
        try:
            data.update(sentiment_analysis(review[1]))
        except Exception:
            print("Null")
    create_file(data, filename)


def create_file(data, filename):
    formatted_data = pd.DataFrame.from_dict(data)
    analysis_res = pd.concat([output_file, formatted_data])
    analysis_res = analysis_res.T
    analysis_res.to_csv(filename)


analyze_verbs(with_links)
analyze_sentences(with_links)
analyze_review(with_links)
