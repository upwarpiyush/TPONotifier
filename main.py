import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from playwright._impl._errors import TimeoutError

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
        with sync_playwright() as p:
            # browser = p.chromium.launch(headless=False, slow_mo=50)
            browser = p.chromium.launch(headless=True, slow_mo=50)
            page = browser.new_page()

            try:
                page.goto('https://tpo.vierp.in/')

                page.wait_for_load_state('networkidle')
                
                page.fill('input#input-15', LOGIN_EMAIL)
                page.fill('input#input-18', LOGIN_PASSWORD)
                
                page.click('button.logi')
                
                page.wait_for_load_state('networkidle')

                #login failure notification
                # if page.url != 'https://tpo.vierp.in/home':
                #     send_email(subject='TPONotifier - Login Failure', body='Failed to login to the website')
                #     return None
                
                desired_url = 'https://tpo.vierp.in/apply_company'
                page.goto(desired_url)
                
                page.wait_for_load_state('networkidle')
                
                full_html = page.content()

                browser.close()
                
                return full_html
            
            except TimeoutError:
                if attempt == retries:
                    send_email(subject='TPONotifier - Failed to list companies', body=f'Failed to navigate to the page after {retries} retries')
                    return None
                else:
                    browser.close()
                    print(f"Attempt {attempt}: Timeout occurred. Retrying...")
            finally:
                browser.close()

def main():
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

if __name__ == "__main__":
    main()
