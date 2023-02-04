import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


class UWCreditUnionScraper:

    def __init__(self):
        # Create a new instance of the Chrome driver
        self.driver = webdriver.Chrome()

    def scrape(self):
        # Load the website
        self.driver.get("https://www.uwcu.org/rates/save-invest/")

        # Find the "Specials" and "IRA Certificates Specials" tables
        specials_tables = self.driver.find_elements(By.XPATH,
                                                    '(//tr[td/span[contains(text(), "Specials")]])[1] | (//tr[td/span[contains(text(), "Specials")]])[1]/following-sibling::tr[1]')
        ira_certificates_specials_tables = self.driver.find_elements(By.XPATH,
                                                                     '(//tr[td/span[contains(text(), "IRA Certificate Specials")]])[1] | (//tr[td/span[contains(text(), "Specials")]])[2]/following-sibling::tr[1]')

        # Scrape the data from the tables
        specials_data = self.scrape_table(specials_tables)
        ira_certificates_specials_data = self.scrape_table(ira_certificates_specials_tables)

        # Save the data to a CSV file
        self.save_to_csv(specials_data, "specials.csv")
        self.save_to_csv(ira_certificates_specials_data, "ira_certificates.csv")

    def scrape_table(self, rows):
        data = []
        for row in rows:
            cells = row.find_elements(By.XPATH, 'td')
            row_data = [cell.text for cell in cells]
            data.append(row_data)
        if data[1][0] == '':
            data[1][0] = data[0][0]

        return data

    def save_to_csv(self, data, filename):
        # Write the data to a CSV file
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            # Add the column names as the first row of the CSV file
            writer.writerow(
                ["type", "terms", "minimum_balance", "dividend_rate", "apy", "premium_dividend_rate", "premium_apy",
                 "diamond_dividend_rate", "diamond_apy"])
            # Write the data to the CSV file
            writer.writerows(data)

    def __del__(self):
        # Close the browser
        self.driver.quit()


if __name__ == "__main__":
    # Run the scraper
    scraper = UWCreditUnionScraper()
    scraper.scrape()
