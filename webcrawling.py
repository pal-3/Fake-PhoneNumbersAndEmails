from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

email_sites = []

# These are the only sites with activity/US numbers/no Cloudflare challenges
number_sites = ["https://www.anonymsms.com",
                "https://www.receivesms.co/us-phone-numbers/us/",
                "https://smstome.com/country/usa",
                "https://www.freephonenum.com/us",
                "https://www.smsreceivefree.com/country/usa",
                "https://www.online-sms.org"]

# Canadian numbers also start with +1, so we can exclude them by searching for their area codes.
canadian_area_codes = [204, 226, 236, 249, 250, 263, 289, 306, 343, 365,
                       367, 368, 403, 416, 418, 431, 437, 438, 450, 474,
                       506, 514, 519, 548, 579, 581, 584, 587, 600, 604,
                       613, 639, 647, 672, 683, 700, 705, 709, 753, 778,
                       780, 782, 807, 819, 825, 867, 873, 879, 902, 905]

def main():
    # Set browser options and create the driver
    settings = webdriver.ChromeOptions()
    settings.headless = True
    settings.page_load_strategy = "none"
    settings.add_argument("--log-level=3")
    chrome_path = ChromeDriverManager().install() 
    chrome_service = Service(chrome_path) 
    driver = Chrome(options=settings, service=chrome_service) 
    driver.implicitly_wait(5)

    # Iterate through each of the websites
    for url in number_sites:
        driver.get(url) # load site
        time.sleep(10)  # give time for JS to render
        numbers = get_numbers(driver, url)

def get_numbers(driver, url):
    """
    Get the links to each US phone number on the website.

    Because phone numbers on the sites are constantly being
    created / deleted, this function will dynamically retrieve
    every currently active number.

    Args:
        driver: the web driver
        url:    the url of the current site being crawled

    Retvals:
        links: a set containing all active US phone numbers
               on the site
    """
    links = set()
    content = driver.find_elements(By.TAG_NAME, "a")

    # for every "<a>" element on the page
    for element in content:
        href = element.get_attribute("href")
        if href != None:
            href_split = href.strip("/").split("/") # split the href to get the number at the end

            # online-sms has a different scheme from the other 5,
            # so we will accomodate here.
            if url == "https://www.online-sms.org":
                potential_number = href_split[-1].split("-")[-1]
            else:
                potential_number = href_split[-1]

            if validate_number(url, potential_number):
                links.add(href)

    return links

def validate_number(url, number):
    """
    Validate whether the last element of the href is a valid
    US phone number or not.

    The value at the end of the href (commonly the resource of the URL)
    may or not be the US phone number we want. This function will take
    that "number" as an argument and validate if it should be returned or
    not.

    Args:
        url:    the url of the current site being crawled
        number: the end of the href (may or may not be a US phone number)

    Retvals:
        True if the arg is a US phone number, false if not.
    """

    if number.isnumeric():

        # These 2 sites are unique in that they do not have a page specifically for
        # US numbers, but all US numbers will be len 11.
        if url == "https://www.anonymsms.com" or url == "https://www.online-sms.org":
            if len(number) != 11:
                return False
        
        # number[0] == "1" is used because US phone numbers start with 1.
        # If the len is <= 10, we add it since some sites will append
        # 4 digit numbers to the end of the href of US numbers.
        if len(number) > 10 and number[0] == "1" or len(number) <= 10:
            if int(number[1:4]) not in canadian_area_codes:
                return True
            
    return False

if __name__ == "__main__":
    main()
