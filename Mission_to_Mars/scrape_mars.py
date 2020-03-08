# Section II Data Collection Script
# Convert the 'mission_to_mars.ipynb' into this Python script
# Add function called scrape that will execute all of your scraping code

# Inport Data Collection Dependencies
from bs4 import BeautifulSoup as bs
import requests
# Import Splinter and setup environment variables
from splinter import Browser


# def init_browser():
#     # @NOTE: Replace the path with your actual path to the chromedriver
#     executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#     return Browser("chrome", **executable_path, headless=False)


def scrape():
    # Create variables to hold news information
    news_title = ""
    news_text = ""
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())
    # Save news title of first article
    news_text = soup.find('div', class_="rollover_description_inner").text.strip()
    # Save news text teaser of first article
    news_title = soup.find('div', class_="content_title").text.strip()
    mars_news = [{"title":news_title,"text":news_text}]

    # ---- Find the image url for the current Featured Mars Image ----
    # Start automated browsing session
    browser = Browser('chrome', **executable_path, headless=False)
    # Create a variable to hold complete url string for the 'full size' .jpg image
    featured_image_url = ""
    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Click 'FULL IMAGE' link on landing page
    browser.click_link_by_partial_text('FULL IMAGE')
    # Click 'more info' link on Featured Image page
    browser.click_link_by_partial_text('more info')
    # Capture page as html
    html = browser.html
    # Store html as soup object
    soup = bs(html, 'html.parser')
    # Capture image download links
    image_dowload_links = soup.find_all('div', class_='download_tiff')
    # Store the second download link on the page; Full-Res JPG
    featured_image_url = image_dowload_links[1].a['href']
    # Exit browser
    browser.quit()
    # Show featured image url
    #featured_image_url


    # ---- Scrape the latest Mars weather tweet from Twitter ----
    # Create a variable to save the latest Mars weather report tweet from Twitter
    mars_weather = ""
    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())
    # Capture weather tweets
    weather_tweets = soup.find_all('div', class_="js-tweet-text-container")
    # Isolate a-tag data for removal from weather tweet
    a_text = weather_tweets[0].a.text.strip()
    #a_text
    # Store most recent Mars weather tweet
    mars_weather = weather_tweets[0].p.text.strip(a_text)
    # Display most recent Mars weather tweet
    #mars_weather

    # ---- Scrape the the Mars Facts webpage for facts about the planet including Diameter, Mass, etc ----
    # Create a variable to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Convert the data to an HTML table string
    mars_facts_html = ""
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())
    # Capture mars facts html tables
    mars_facts_tables = soup.find_all('table', class_="tablepress tablepress-id-p-mars")
    #mars_facts_tables
    mars_facts_html = mars_facts_tables[1]
    # Show raw html formatted Mars facts table
    #mars_facts_html

    # ---- Visit the SGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres ----
    # Create a Python dictionary to store the data using the keys 'img_url' and 'title'.
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "..."},
        {"title": "Cerberus Hemisphere", "img_url": "..."},
        {"title": "Schiaparelli Hemisphere", "img_url": "..."},
        {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    ]
    # Find urls for all images in the dictionary
    for image in range(len(hemisphere_image_urls)):
        # Start automated browsing session
        browser = Browser('chrome', **executable_path, headless=False)
        # URL of page to be scraped
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        # Navigate to given url
        browser.visit(url)
        # Store current image title for readability
        current_image = hemisphere_image_urls[image]["title"]
        # Click 'FULL IMAGE' link on landing page
        browser.click_link_by_partial_text(current_image)
        # Capture page as html
        html = browser.html
        # Store html as soup object
        soup = bs(html, 'html.parser')
        #soup
        # Capture image download links
        image_dowloads = soup.find_all('div', class_='downloads')
        # Store the first download link in the container
        hemisphere_image_urls[image]["img_url"] = image_dowloads[0].a['href']
        #hemisphere_image_urls[0]["img_url"]
        # Print image capture confirmation log
        print(f"Captured image URL for {current_image}")
        print('-----------')
        # Close the browser
        browser.quit()

    # Mars Data Dictionary
    complete_mars_data_set = [
        {"Mars News":mars_news},
        {"Featured Image URL":featured_image_url},
        {"Latest Mars Weather":mars_weather},
        {"Mars Facts HTML":mars_facts_html},
        {"Hemisphere Image URLs":hemisphere_image_urls}
    ]