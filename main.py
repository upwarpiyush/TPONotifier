from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50) #make headless=true at the time of deployment as it opens gui when its false
    page = browser.new_page()
    page.goto('https://tpo.vierp.in/')
    page.fill('input#input-15', '22010485@viit.ac.in')
    page.fill('input#input-18', 'anushka26')
    page.click('button.logi')
    # html = page.inner_html('.v-toolbar__content')
    # print(html)
    page.wait_for_load_state('networkidle')
    desired_url = 'https://tpo.vierp.in/company-dashboard'
    page.goto(desired_url)
    page.wait_for_load_state('networkidle')

    html = page.inner_html('.container')
    print(html)
