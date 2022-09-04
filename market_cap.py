import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window()  # maximize window

# move to the page

url = 'https://finance.naver.com/sise/sise_market_sum.nhn?&page='
browser.get(url)

# initialize the check mark
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected():
        checkbox.click()

# Select desired table
items_to_select = ['영업이익', '매출액', '자산총계']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..')  # finding parent element
    label = parent.find_element(By.TAG_NAME, 'label')

    if label.text in items_to_select:
        checkbox.click()  # select the desired data table

# Apply the selection
btn_apply = browser.find_element(
    By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1, 40):  # page from 1 to less than 40

    browser.get(url + str(idx))  # move page

    # Acquring Data
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0:
        break

    # Save the data
    f_name = 'kospi_market.csv'
    if os.path.exists(f_name):  # remove header if file exists
        df.to_csv(f_name, encoding='utf-8-sig',
                  index=False, mode='a', header=False)
    else:  # include header if the file does not exist
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} Page completed')

browser.quit()  # exit the browser
