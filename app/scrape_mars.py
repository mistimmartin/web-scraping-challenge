from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time 

def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    news_title = soup.find('div', class_='content_title').find('a',target='_self').text
    news_p = soup.find('div', class_='article_teaser_body').text

    return news_title, news_p


def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')
    featured_image = jpl_soup.find('div',class_='carousel_items').a['data-fancybox-href']
    return featured_image


def hemispheres(browser):

    # A way to break up long strings
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )

    browser.visit(url)
    
    html = browser.html
    hemisphere_soup = BeautifulSoup(html, 'html.parser')

    hemisphere_images_url = []
    hemispheres = hemisphere_soup.find_all('div',class_="item")
    for h in hemispheres:
        h_url = h.find('a')['href']
        title = h.find('h3').text
        hemisphere_images_url.append({"title": title, "img_url": url + h_url})
    return hemisphere_image_url


def twitter_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    weather_soup = BeautifulSoup(html, 'lxml')

    mars_weather = weather_soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text

    return mars_weather


def mars_facts():
    try:
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        return None

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)

    # Add some bootstrap styling to <table>
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
