from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import time

FORMS_LINK = "https://forms.gle/Fxz2FBzUKc6Ye1AP8"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=headers)
website_zillow = response.text

soup = BeautifulSoup(website_zillow, "html.parser")

# Here this will fetch the links of the properties
all_links_elements = soup.select(".StyledPropertyCardPhotoBody a")
all_links = [link["href"] for link in all_links_elements]

length_of_links = len(all_links)
print(length_of_links)

# Here it fetches address of the properties
address_elements = soup.select(".StyledPropertyCardDataWrapper address")
addresses = [address.getText().replace(" | ", " ").strip() for address in address_elements]

# Here it fetches the price of the properties
price_list = soup.select(".PropertyCardWrapper span")
prices = [price.get_text().replace("/mo", "").split("+")[0] for price in price_list if "$" in price.text]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(FORMS_LINK)

for n in range(length_of_links):
    driver.get(FORMS_LINK)
    time.sleep(2)

    address_input = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    address_input.send_keys(addresses[n])
    price_input.send_keys(prices[n])
    link_input.send_keys(all_links[n])

    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit_button.click()
