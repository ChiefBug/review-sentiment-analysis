from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.amazon.com/COSORI-Airfryer-Dishwasher-Safe-freidora-Exclusive/product-reviews/B0936FGLQS/ref" \
      "=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1 "
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

review_data = pd.DataFrame(columns=['Name', 'Stars', 'Title', 'Review'])


def WaitForPageToLoad():
    WebDriverWait(driver, 30).until(lambda d: d.execute_script(
        'return (document.readyState == "complete" || document.readyState == "interactive")'))


for n in range(0, 500):

    name = []
    title = []
    stars = []
    review = []

    driver.get(url)
    WaitForPageToLoad()
    soup = BeautifulSoup(driver.page_source, 'lxml')

    for y in soup.find_all('div', attrs={'data-hook': 'review'}):
        [name.append(i.text) for i in y.find_all_next('span', class_='a-profile-name')]
        [stars.append(i.text[0]) for i in y.find_all_next('i', attrs={'data-hook': 'review-star-rating'})]
        [title.append(i.text) for i in y.find_all_next('a', attrs={'data-hook': 'review-title'})]
        [review.append(i.text) for i in y.find_all_next('span', attrs={'data-hook': 'review-body'})]

        data = {'Name': name, 'Stars': stars, 'Title': title, 'Review': review}
        formatted_data = pd.DataFrame.from_dict(data)
        review_data = pd.concat([review_data, formatted_data])
        break

    link = driver.current_url
    link_split = driver.current_url.split('pageNumber=')
    page_num = int(link_split[1])
    page_num += 1
    url = link_split[0] + f'pageNumber={page_num}'

driver.quit()

review_data.to_csv('reviews.csv')
