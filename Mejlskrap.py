import scrapy
import pandas as pd
import re
from colorama import init, Fore
from scrapy.crawler import CrawlerProcess
from pyfiglet import Figlet

class Skrapspindel(scrapy.Spider):
    name = 'skrapspindel'
    start_urls = []
    allowed_domains = []
    emails = set()
    visited_urls = []

    def parse(self, response):
        # Check if the current URL has been visited before
        if response.url in self.visited_urls:
            return
        self.visited_urls.append(response.url)

        # Extract email addresses from 'mailto:' links
        for email in response.xpath("//a[starts-with(@href, 'mailto:')]/@href").getall():
            email = email.replace("mailto:", "")
            if email.endswith(self.allowed_domains[0]) and email not in self.emails:
                self.emails.add(email)
                yield {'email': email, 'url': response.url}

        # Extract email addresses from plain text
        page_content = response.body.decode()
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", page_content)
        for email in emails:
            if email.endswith(self.allowed_domains[0]) and email not in self.emails:
                self.emails.add(email)
                yield {'email': email, 'url': response.url}

        # Follow all links on the page
        for href in response.xpath("//a/@href"):
            yield response.follow(href, self.parse)

init()

def ascii_art_title():
    f = Figlet(font='roman')
    print(Fore.GREEN + f.renderText("MEJL\nSKRAP"))
    print("AV HANNERVAL \n")

ascii_art_title()

def domai():
    output_choice = input("Vill du skriva ut eller spara resultatet? (skriv ut/spara)\n")
    url = input("Vilken domän vill du skrapa?\n")
    if not url.startswith("http"):
        url = "https://" + url
    start_urls = [url]
    allowed_domains = [url.split("//")[-1]]
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
    process.crawl(Skrapspindel, start_urls=start_urls, allowed_domains=allowed_domains)
    process.start()
    emails = pd.DataFrame(Skrapspindel.emails, columns=['email'])
    emails.drop_duplicates(subset='email', inplace=True)  # drop duplicates based on email column
    if output_choice == "spara":
        filename = input("Ange filnamn för att spara resultatet: ")
        file_ext = ".csv"
        if not filename.endswith(".csv"):
            filename = filename + file_ext
        emails.to_csv(filename, index=False)
    else:
        print(emails)

domai()

