import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

class MulchPriceMonitor:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.target_price = 3.70
        
        # Add your headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Store URLs for different retailers
        self.retailers = {
            'Home Depot': 'https://www.homedepot.com/b/Outdoors-Garden-Center-Mulch/N-5yc1vZbx5e',
            'Lowes': 'https://www.lowes.com/pl/Mulch-Mulch-soil-Lawn-garden/4294612776'
        }

    def check_home_depot(self):
        try:
            response = requests.get(self.retailers['Home Depot'], headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find product prices (you'll need to update these selectors based on the actual website structure)
            products = soup.find_all('div', class_='product-price')
            deals = []
            
            for product in products:
                try:
                    price = float(product.text.strip().replace('$', ''))
                    if price <= self.target_price:
                        title = product.find_previous('h2', class_='product-title').text.strip()
                        deals.append((title, price))
                except ValueError:
                    continue
                    
            return deals
        except Exception as e:
            print(f"Error checking Home Depot: {str(e)}")
            return []

    def check_lowes(self):
        try:
            response = requests.get(self.retailers['Lowes'], headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find product prices (you'll need to update these selectors based on the actual website structure)
            products = soup.find_all('div', class_='price')
            deals = []
            
            for product in products:
                try:
                    price = float(product.text.strip().replace('$', ''))
                    if price <= self.target_price:
                        title = product.find_previous('h2', class_='product-title').text.strip()
                        deals.append((title, price))
                except ValueError:
                    continue
                    
            return deals
        except Exception as e:
            print(f"Error checking Lowes: {str(e)}")
            return []

    def send_email_notification(self, deals):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.email
        msg['Subject'] = 'Mulch Price Alert!'

        body = "The following mulch products are at or below $2:\n\n"
        for title, price in deals:
            body += f"{title}: ${price:.2f}\n"

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            print("Email notification sent successfully!")
        except Exception as e:
            print(f"Error sending email: {str(e)}")

    def monitor_prices(self, check_interval=3600):
        while True:
            all_deals = []
            
            # Check Home Depot
            hd_deals = self.check_home_depot()
            all_deals.extend([('Home Depot', *deal) for deal in hd_deals])
            
            # Check Lowes
            lowes_deals = self.check_lowes()
            all_deals.extend([('Lowes', *deal) for deal in lowes_deals])
            
            # If any deals are found, send notification
            if all_deals:
                self.send_email_notification(all_deals)
            
            # Wait for the specified interval before checking again
            time.sleep(check_interval)

# Usage example
if __name__ == "__main__":
    # Replace with your email and app password
    # Load environment variables from .env file
    load_dotenv("env/.env")

    # Usage example
    if __name__ == "__main__":
        monitor = MulchPriceMonitor(
            email=os.getenv("EMAIL"),
            password=os.getenv("PASSWORD")
        )
        
        # Start monitoring (checks every hour by default)
        monitor.monitor_prices()
    
    # Start monitoring (checks every hour by default)
    monitor.monitor_prices()