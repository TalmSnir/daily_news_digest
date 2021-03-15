from bs4 import BeautifulSoup
import requests
import time
from smtplib import SMTP
from email.message import EmailMessage
import schedule
from pathlib import Path
from string import Template


def get_news():
    url1 = 'https://www.mako.co.il/nexter?partner=NavBar'
    res1 = requests.get(url1)
    res1_top_story = BeautifulSoup(
        res1.text, "html.parser").find_all(class_='triple')
    res1_top_story_title = res1_top_story[0].p.text
    res1_top_story_url = (res1_top_story[0].pre).a['href']
    res1_top_story_a = f'<a href="{res1_top_story_url}">continue to the article </a>'
    return res1_top_story_title, res1_top_story_a


def send_email(to_address, from_address, password):
    article_title, article_a = get_news()
    html = Template(Path('daily_news_digest\index.html').read_text())
    email = EmailMessage()
    email['from'] = from_address
    email['to'] = to_address
    email['subject'] = 'your daily news digest'
    email.set_content(html.substitute(
        article_title=article_title, article_a=article_a), 'html')

    with SMTP(host='smtp.gmail.com', port=587) as smtp:

        smtp.starttls()
        smtp.login(from_address, password)
        smtp.send_message(email)
        smtp.quit()


# ! enter the relevant informarion below
# from_address =
# to_address =
# password =

schedule.every().day.at('07:45').do(
    send_email, to_address, from_address, password)
while True:
    schedule.run_pending()
    time.sleep(1)
