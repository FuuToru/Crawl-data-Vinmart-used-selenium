import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import os

url='utf-8'
# Khởi tạo trình duyệt Chrome và webdriver
driver = webdriver.Chrome()
driver.get("https://vinmart.co/thuc-pham-tuoi-song-46908/")

# Lấy link sản phẩm của 10 page đầu tiên
links = []
for i in range(9):
    # Lấy link sản phẩm từ trang hiện tại
    product_items = driver.find_elements(By.XPATH,"/html/body/main/div/div/div[2]/div[2]/div")

    for item in product_items:
        link = item.find_element(By.XPATH,".//a").get_attribute("href")
        links.append(link)

    # Chuyển sang trang kế tiếp
    t=i+2
    s='https://vinmart.co/thuc-pham-tuoi-song-46908/?trang=@'
    s=s.replace('@', str(t))
    driver.get(s)
    sleep(1)  # Chờ 2 giây để trang tiếp theo tải xong


# Thu thập dữ liệu của từng sản phẩm
data = []
for link in links:
    driver.get(link)

    name = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div[2]/h1")
    name = name.text.strip()

    store = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div[2]/div[1]/a[1]/strong")
    store = store.text.strip()

    price = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div[2]/div[3]/span[1]")
    t= price.text.strip().split('&')
    price=t[0]


    status = ""
    if driver.find_elements(By.XPATH,"/html/body/main/div/div[1]/div/div[2]/div[2]"):
        status = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div[2]/div[2]")
        status = status.text.strip()

    stock = ""
    if driver.find_elements(By.XPATH,"/html/body/main/div/div[1]/div/div[2]/div[3]/span"):
        stock = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div[2]/div[3]/span")
        stock = stock.text.strip()

    description = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div[2]/span[2]")
    description = description.text.strip()

    # Lưu dữ liệu vào một dict
    item = {
        "name": name,
        "store": store,
        "price": price,
        "status": status,
        "stock": stock,
        "description": description
    }
    data.append(item)

# Lưu dữ liệu vào file CSV
import csv


filename= "winmart.csv"
with open(os.path.join("data",filename),'w',encoding='utf-8') as csvfile:
    fieldnames = ["name", "store", "price", "status", "stock", "description"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in data:
        writer.writerow(item)

# Đóng trình duyệt
driver.close()
