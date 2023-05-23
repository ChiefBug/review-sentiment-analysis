import nltk
from textblob import TextBlob
from nltk.tokenize import WhitespaceTokenizer
import pandas as pd
from tqdm.auto import tqdm

df = pd.read_csv('C:/Users/shing/Documents/Semester_3/Research Sentiment Analysis/Reviews/v2_B000GAYQKY.csv', usecols=['User', 'Date', 'Stars', 'Title', 'Text'])

review_lst = []
review_lst = df['Text'].astype(str)

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


# Check polarity
def analyze_verbs(review_lst):
    verbs = set()  # using a set so that same verbs from multiple reviews are not repeated
    filename = 'verb_analysis.csv'
    data = {}
    for review in tqdm(review_lst):
        tokens = create_tokens(review)
        for i in range(len(tokens)):
            text, tag = tokens[i]
            if tag in ("VBZ", "VBD", "VBG", "VBP", "VBN"):
                verbs.add(text)

        for word in verbs:
            ans = sentiment_analysis(word)
            out = ans.get(word)
            data[word] = {'Subjectivity': out.get('Subjectivity'), 'Polarity': out.get('Polarity'),
                          'Score': out.get('Score')}
    create_file(data, filename)


def analyze_sentences(review_lst):
    filename = 'sentence_analysis.csv'
    data = {}
    for review in tqdm(review_lst):
        sentences = review.split('.')
        for sentence in sentences:
            data.update(sentiment_analysis(sentence))
    create_file(data, filename)


def analyze_review(review_lst):
    filename = 'review_analysis.csv'
    data = {}
    for review in tqdm(review_lst):
        data.update(sentiment_analysis(review))
    create_file(data, filename)


def create_file(data, filename):
    formatted_data = pd.DataFrame.from_dict(data)
    analysis_res = pd.concat([output_file, formatted_data])
    analysis_res = analysis_res.T
    analysis_res.to_csv(filename)


# analyze_review(review_lst)
analyze_sentences(review_lst)
# analyze_verbs(review_lst)
