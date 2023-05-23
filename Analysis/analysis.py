import pandas as pd
import seaborn as sns
import nltk
nltk.download('wordnet')
from textblob import TextBlob
color = sns.color_palette()
import plotly.offline as py

py.init_notebook_mode(connected=True)
import plotly.express as px

df = pd.read_csv('C:/Users/shing/Documents/Semester_3/Research Sentiment Analysis/Reviews/reviews.csv', usecols=['Name', 'Stars', 'Title', 'Review'])
df.head()

df['Review'] = df['Review'].astype(str)
pol = lambda x: TextBlob(x).sentiment.polarity
df = df[df['Stars'] != 3]
df['Polarity'] = df['Review'].apply(pol)
df['Sentiment'] = df['Stars'].apply(lambda rating: +1 if rating > 3 else -1)


df['Sentiment1'] = df['Sentiment'].replace({-1: 'negative'})
df['Sentiment1'] = df['Sentiment1'].replace({1: 'positive'})
fig = px.histogram(df, x="Sentiment1")
fig.update_traces(marker_color="indianred", marker_line_color="rgb(8, 48, 107)", marker_line_width=1.5)
fig.update_layout(title_text='Product Sentiment')
fig.show()

# num_bins = 50
# plt.figure(figsize=(10, 6))
# n, bins, patches = plt.hist(df.polarity, num_bins, facecolor='blue', alpha=0.5)
# plt.xlabel('Polarity')
# plt.ylabel('Number of reviews')
# plt.title('Histogram of polarity score')
# plt.show()
# df.to_csv('C:/Users/shing/Documents/Semester_3/Research Sentiment Analysis/Reviews/analyzed_reviews.csv')


