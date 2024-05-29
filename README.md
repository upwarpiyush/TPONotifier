# TPONotifier

TPONotifier is a Python - Selenium - AWS Lambda based project that logs into TPO website, scrapes data about newly listed companies, and sends this information via email. The function runs daily at 09:30 PM 🕥 using a CloudWatch trigger.

## Table of Contents
- [What It Does❓](#what-it-does)
- [Tools I Used🛠](#tools-i-used)
- [How It Works🤔](#how-it-works)
- [Known Problems❌](#known-problems)
- [Work In Progress🚧](#work-in-progress)

## What It Does❓
- Automatically logs into the VIIT TPO website.
- Scrapes data about newly listed companies from the website.
- Sends an email with the list of newly listed companies every day at 6 PM.

## Tools I Used🛠
- Python: Used for scripting and backend processing.
- Selenium: Used for web scraping to automate browser interaction.
- BeautifulSoup: Used for parsing HTML to extract data.
- boto3: Used to interact with AWS services.
- smtplib: Used for sending emails via SMTP.
- AWS Lambda: Used to run the script serverlessly.
- AWS CloudWatch: Used to trigger the Lambda function on a schedule.
- Docker: Used for containerizing the application.

## How It Works🤔
- **Login:** The script uses Selenium to open the TPO website and logs in using the provided credentials.
- **Scrape Data:** After logging in, it navigates to the company listing page and scrapes the data using BeautifulSoup.
- **Send Email:** The scraped data is formatted and sent via email using smtplib.
- **Automation:** AWS Lambda runs this script daily at 09:30 PM, triggered by a CloudWatch Events rule.

## Known Problems❌
- The Lambda function might fail if the website structure changes.

## Work In Progress🚧
- Improving error handling and retry logic.
- Enhancing email formatting.
