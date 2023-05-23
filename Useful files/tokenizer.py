import nltk
from nltk.tokenize import WhitespaceTokenizer
import pandas as pd

df = pd.read_csv('C:/Users/shing/Documents/Semester_3/Research Sentiment Analysis/Reviews/v1_reviews.csv', usecols=['Name', 'Stars', 'Title', 'Review'])


review_lst = []
review_lst = df['Review'].astype(str)

output_file = pd.DataFrame()

tokens_positions = list(WhitespaceTokenizer().span_tokenize(review_lst[0]))  # Tokenize to spans to get start/end positions: [(0, 3), (4, 9), ... ]
tokens = WhitespaceTokenizer().tokenize(review_lst[0])  # Tokenize on a string lists: ["man", "walks", "into", ... ]

tokens = nltk.pos_tag(tokens) # Run Part-of-Speech tagger

verbs = set()
for i in range(len(tokens)):
    text, tag = tokens[i]
    start, end = tokens_positions[i]
    if tag in ("CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT",
               "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ",
               "WDT", "WP", "WP$", "WRB"):
        verbs.add(text)

print(review_lst[0])
print(verbs)

