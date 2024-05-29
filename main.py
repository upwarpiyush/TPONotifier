import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
 
load_dotenv()
 
LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
 
def send_email(subject, body):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    server.quit()
 
def login_and_extract_content():
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            # driver = webdriver.Chrome()
 
            # chrome_options = Options()
            # chrome_options.add_argument("--headless")
 
            # driver = webdriver.Chrome(options=chrome_options)
 
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--single-process")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.binary_location = "/opt/chrome/chrome"  # path to headless chrome in the custom layer
 
            driver_service = Service("/opt/chromedriver")  # path to chromedriver in the custom layer
            driver = webdriver.Chrome(service=driver_service, options=chrome_options)
 
            driver.get('https://tpo.vierp.in/')
 
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#input-15')))
            
            email_input = driver.find_element(By.CSS_SELECTOR, 'input#input-15')
            password_input = driver.find_element(By.CSS_SELECTOR, 'input#input-18')
            login_button = driver.find_element(By.CSS_SELECTOR, 'button.logi')
            
            email_input.send_keys(LOGIN_EMAIL)
            password_input.send_keys(LOGIN_PASSWORD)
            login_button.click()
 
            WebDriverWait(driver, 10).until(EC.url_to_be('https://tpo.vierp.in/home'))
 
            driver.get('https://tpo.vierp.in/apply_company')
 
            WebDriverWait(driver, 10).until(EC.url_to_be('https://tpo.vierp.in/apply_company'))
 
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'v-card__title')))
            except:
                print("Timeout occurred while waiting for v-card__title elements to be present")
                
            html_content = driver.page_source
 
            return html_content
            
        except Exception as e:
            if attempt == retries:
                send_email(subject='TPONotifier - Failed to list companies', body=f'Failed to navigate to the page after {retries} retries. Error: {str(e)}')
                return None
            else:
                print(f"Attempt {attempt}: Error occurred. Retrying...")
        finally:
                if 'driver' in locals():
                    driver.quit()
 
def lambda_handler(event=None, context=None):
# def main():
    html_content = login_and_extract_content()
    
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        company_elements = soup.find_all(class_='v-card__title')
        
        if not company_elements:
            send_email(subject='TPONotifier - No Companies Listed', body='No companies are listed today')
            return
        
        company_names = [element.get_text().strip() for element in company_elements]
        
        # Format the email body
        email_body = "Hi Piyush !!\n\nHere are the companies listed today 👇\n\n"
        email_body += "\n".join(f"[{name}]" for name in company_names)
        email_body += "\n\nTPONotifier😍"
        
        send_email(subject='TPONotifier - Newly Listed Companies Today', body=email_body)
 
        return {
            'statusCode': 200,
            'body': 'Function executed successfully!'
        }
    
    else:
        return {
            'statusCode': 500,
            'body': 'Failed to list companies'
        }
 
# if __name__ == "__main__":
#     lambda_handler({}, {})
#     main()