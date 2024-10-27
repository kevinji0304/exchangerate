from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime

driver = webdriver.Chrome()
base_url = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'
today_date = datetime.now().strftime("%Y-%m-%d")
timestamp = datetime.now().strftime("%Y%m%d_%H%M") 

driver.get(base_url)

start_time = driver.find_element(By.NAME, 'erectDate')
start_time.clear()
start_time.send_keys(today_date)  

end_time = driver.find_element(By.NAME, 'nothing') 
end_time.clear()
end_time.send_keys(today_date)


currency_dropdown = driver.find_element(By.NAME, 'pjname')
currency_dropdown.click()

# Wait for data to load after clicking the search button
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CLASS_NAME, "odd"))
)

rows = driver.find_elements(By.XPATH, "//div[@class='BOC_main publish']/table/tbody/tr[contains(@class, 'odd') or not(@class)]")
data = []
for row in rows:
    columns = row.find_elements(By.TAG_NAME, 'td')
    if columns:  # Ensure it's a data row
        row_data = [col.text.strip() for col in columns]
        data.append(row_data)

# Save data to CSV
filename = f'exchange_rates_{timestamp}.csv'
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['货币名称', '现汇买入价', '现钞买入价', '现汇卖出价', '现钞卖出价', '中行折算价', '发布时间'])  # Adjust headers as needed
    csvwriter.writerows(data)

# Close the driver
driver.quit()