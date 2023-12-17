from playwright.sync_api import sync_playwright
import time
import random


# Contact details
contact_name = "Nikita"
message = random.choice(['hi','hiii','gi','ki','hi','hi','hey'])

# Initialize Playwright and open WhatsApp Web
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://web.whatsapp.com/')
    page.wait_for_load_state('domcontentloaded')

    # Wait for the QR code to be scanned
    page.wait_for_selector('canvas[aria-label="Scan me!"]', state='attached')

    # Find and click on the contact's chat
    contact_selector = f'text="{contact_name}"'
    contact_element = page.wait_for_selector(contact_selector, state='attached')
    contact_element.click()

    page.wait_for_timeout(5000)

    # Send a message
    for i in range(100):
        message_input_selector = 'div[class="_3Uu1_"]'
        message_input_element = page.wait_for_selector(message_input_selector)
        message_input_element.type(f'{message*5}')
        page.wait_for_timeout(1000)
        page.keyboard.press("Enter")

    # Close the browser
    context.close()
