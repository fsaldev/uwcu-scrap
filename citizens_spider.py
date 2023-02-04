import time
import csv
from selenium.webdriver.common.by import By
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CitizensBankScraper:
    def __init__(self, url, zip_code):
        self.file_name = None
        self.url = url
        self.zip_code = zip_code
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        # chrome_options.add_argument('--headless')
        seleniumwire_options = {
            'verify_ssl': False, 'connection_timeout': None}
        self.driver = uc.Chrome(options=chrome_options,
                                seleniumwire_options=seleniumwire_options,
                                use_subprocess=True)

    def open_website(self):
        self.driver.get(self.url)

    def enter_zip_code(self):
        try:
            zip_code = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="zip_input_region"]')))
            zip_code.send_keys(self.zip_code)
        except Exception as e:
            print(f"enter_zip_code function failed with error: {e}")

    def submit(self):
        try:
            submit = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="zip_submit_region"]')))
            submit.click()
        except Exception as e:
            print(f"submit function failed with error: {e}")

    def view_rates(self):
        try:
            view_rates = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modal1"]')))
            view_rates.click()
        except Exception as e:
            print(f"view_rates function failed with error: {e}")

    def extract_data(self):
        try:
            rates_data = []
            headers = []

            file_name = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '(//*[@class="hls_modal"]/div[@class="hls_modal_header"]/h2)[1]')))
            file_name = file_name.text.split(' ')
            self.file_name = "_".join(file_name)
            table_data = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '(//*[@class="hls_modal"]/div[@class="hls_modal_content"]/table)[1]')))

            header_elements = table_data.find_elements(By.XPATH, 'thead/tr/th')
            for header_element in header_elements:
                headers.append(header_element.text)

            row_elements = table_data.find_elements(By.XPATH, 'tbody/tr')
            for row_element in row_elements:
                row = []
                cell_elements = row_element.find_elements(By.XPATH, 'td')
                for cell_element in cell_elements:
                    row.append(cell_element.text)
                rates_data.append(row)
            return headers, rates_data
        except Exception as e:
            print(f"extract_data function failed with error: {e}")

    def save_to_csv(self, headers, rates_data):
        with open(f"{self.file_name}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rates_data)

    def close_driver(self):
        self.driver.quit()

    def scrape(self):
        self.open_website()
        self.enter_zip_code()
        self.submit()
        time.sleep(20)
        self.view_rates()
        time.sleep(2)
        headers, rates_data = self.extract_data()
        self.save_to_csv(headers, rates_data)
        self.close_driver()


if __name__ == "__main__":
    scraper = CitizensBankScraper(
        url="https://www.citizensbank.com/custom/regionalizationgateway.aspx?targetpage=/savings/money-market-accounts/overview.aspx",
        zip_code="02421"
    )
    scraper.scrape()
