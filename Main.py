from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv
#import lxml

load_dotenv()

url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

header = {
    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 18_5_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/375.1.776343893 Mobile/15E148 Safari/604.1",
    "Accept-Language": "en-GB,en;q=0.9"
}


response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "html.parser" #Or lxml)



price = soup.find(class_="a-offscreen").get_text()

# Remove currency
price_without_currency = price.split("€")[1]

#Floating point number
price_float = float(price_without_currency)
print(price_float)

# Get the product title
product_title = soup.find(id="productTitle").get_text().strip()



FINAL_PRICE = 'Your final buy price'

if price_as_float < FINAL_PRICE:
    message = f"{product_title} is on sale for {price}!"
    with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
        connection.starttls()
        result = connection.login(os.environ["ADDRESS"], os.environ["PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["EMAIL"],
            to_addrs=os.environ["EMAIL"],
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )
