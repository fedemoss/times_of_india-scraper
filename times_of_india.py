# -*- coding: utf-8 -*-
"""
@author: mossney


This is a web scraper for the famous indian newspaper 'Times of India'. The aim of this project is to get information about 
certain topics from different perspectives. So I started by analyzing which news are relevant in India.

Keep in mind that this scraper takes into considerations the english version of the newspaper 
(SO HANDLE THE INFORMATION WITH CARE).

------- ADVICE & IP STUFF

This script is intended to work from google colab by default, since you dont use your IP when using this service.

If you want to run the script locally, be aware that, thanks to the many requests, 
out IP can be blocked by the newspaper site. In this case, we would want some kind of IP protection. 

I tried to protect my IP by generating a random number in each request and using that number to sleep the script....
but this is a poor way of protecting my IP...


------- WHAT WE NEED TO INSTALL

In either case, we nedd to install SELENIUM. So,  we run in the console:
    
    !pip install selenium
    !apt-get update 
    !apt install chromium-chromedriver

If we are running the script locally, we need the PATH to the chromedriver.exe

more info: https://selenium-python.readthedocs.io/installation.html#drivers


-------- USING THE SCRIPT

The main function is:
    
    times_india_scraper(topic, PATH)

-Where the topic is the topic we want to search about. There are going to be news related with this topic. 

-The PATH is the path to the webdriver (chromedriver.exe if using chrome). By default (if we run the script in colab), 
 the PATH its a given parameter. 


The main function returns a PANDAS dataframe with every article found related with the topic inserted.


"""
#Iterate!
def iterator(url):
  driver.get(url)
  time.sleep(2)
  html = driver.page_source
  soup = BS(html, 'html.parser')
  #Total number of publications
  total_articles = int(soup.find(attrs={'id':'Articles'}).text.split('(')[1].replace(')',''))

  #iterations
  x = total_articles-20 #primera pasada
  iterations = int(x/15)

  #View more
  for i in range(iterations):
    driver.find_element_by_css_selector('._3BnB0 ').click()
    time.sleep(2)

  #Articles
  html = driver.page_source
  soup = BS(html, 'html.parser')

  news = soup.find_all(attrs={'class': 'Mc7GB'})
  return news

#Articles
def articles_finder(news):
  newspaper = []
  link = []
  title = []
  month = []
  day = []
  year = []
  time = []

  for new in news:
    newspaper.append('Times of India')
    link.append(new.find('a')['href'])
    title.append(new.find(attrs={'class':'EW1Mb _3v379'}).text)
    try:
      month.append(new.find(attrs={'class':'hVLK8'}).text.split(',')[0].split('/ ')[1].split(' ')[0])
    except:
      month.append(new.find(attrs={'class':'hVLK8'}).text.split(',')[0].split(' ')[0])
    try:
      day.append(int(new.find(attrs={'class':'hVLK8'}).text.split(',')[0].split('/ ')[1].split(' ')[1]))
    except:
      day.append(int(new.find(attrs={'class':'hVLK8'}).text.split(',')[0].split(' ')[2])) #Sometimes its like this, when theres no publisher info

    year.append(int(new.find(attrs={'class':'hVLK8'}).text.split(',')[1].replace(' ','')))
    time.append(new.find(attrs={'class':'hVLK8'}).text.split(',')[2].replace(' ','').split('(')[0])


  general_dict = {'Newspaper': newspaper, 'Title': title, 'Month': month, 'Day':day, 'Year':year, 'Time': time, 'Link': link}
  df = pd.DataFrame(general_dict)
  return df

#Content
def get_content(df):
  import numpy as np
  links = df['Link']
  content = []
  for link in links:
    try:
      driver.get(link)
      time.sleep(2)
      html = driver.page_source
      soup = BS(html, 'html.parser')
      try:
        content.append(soup.find(attrs={'class':'ga-headlines'}).text)
      except:
        content.append(soup.find(attrs={'class':'_3YYSt clearfix '}).text) 
      time.sleep(np.random.uniform(0.5,1)) #Acting as a normal user
    except:
      content.append(np.nan)

  return content

#Everything together
def times_india_scraper(topic,PATH='chromedriver'):
  import numpy as np
  import pandas as pd
  import time
  from bs4 import BeautifulSoup as BS
  from selenium import webdriver
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

  #Url
  topic.replace(' ','-')
  url = 'https://timesofindia.indiatimes.com/topic/{}/news'.format(topic)

  #Iterator (All news)
  news = iterator(url)

  #Articles general info
  df = articles_finder(news)

  #Get Content of each article
  content = get_content(df)
  df['Content'] = content

  return df