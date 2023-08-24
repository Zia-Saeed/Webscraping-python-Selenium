from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd


if __name__ == '__main__':
    product_price = input("Enter the name of the product you want to get the data of: ")

    service = Service(executable_path="F:/chrome-driver/chromedriver")
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    wb = webdriver.Chrome(service=service, options=option)
    wb.get(url="https://www.alibaba.com/")
    time.sleep(1)

    search_bar = wb.find_element(By.CLASS_NAME, "search-bar-input")
    search_bar.send_keys(product_price)
    search_button = wb.find_element(By.CLASS_NAME, "fy23-icbu-search-bar-inner-button")
    search_button.click()
    time.sleep(1)

    headings = ["name", "price", "quantity", "links"]
    data_frame = pd.DataFrame(columns=headings)

    file_name = f"{product_price}.csv"

    data_frame.to_csv(file_name, index=False)

    for i in range(10):
        all_elements_links = wb.find_elements(By.CSS_SELECTOR, ".elements-title-normal__outter a")
        all_elements_name = wb.find_elements(By.CSS_SELECTOR, ".elements-title-normal__outter a p")
        price = wb.find_elements(By.CLASS_NAME, "elements-offer-price-normal__price")
        quantity = wb.find_elements(By.CLASS_NAME, "element-offer-minorder-normal__value")
        p_des = {
            "name": [],
            "price": [],
            "quantity": [],
            "links": []
        }
        for element in range(0, len(all_elements_name) - 1):
            p_des["name"].append(all_elements_name[element].text)
            p_des["price"].append(price[element].text)
            p_des["quantity"].append(quantity[element].text)
            p_des["links"].append(all_elements_links[element].get_attribute("href"))

        next_page = wb.find_element(By.CLASS_NAME, "pages-next")
        next_page.click()
        time.sleep(3)

        csv_file_path = f"{product_price}.csv"
        new_row = pd.DataFrame(p_des)
        new_row.to_csv(csv_file_path, mode="a", header=False, index=False)

    print("Data is collected successfully!")

    wb.close()

