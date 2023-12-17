import os
import django
import asyncio
# asyncio.get_event_loop().set_debug(True)

from django.db.models import Q


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')
django.setup()

from asgiref.sync import sync_to_async


from model.models import Business

from playwright.async_api import async_playwright, Error


import os
import time

import json
from playwright.sync_api import sync_playwright

import argparse
import re

async def save_business(business):
    await sync_to_async(business.save)()

async def save_businesses(business_list):
    await sync_to_async(Business.objects.bulk_create)(business_list)   

async def scrape_data(page, l_i, l_j, l_k, l_l):
    print("ss hi")

    business_listtt = []
    entry_exists = await sync_to_async(Business.objects.filter(
        Q(state=l_i) &
        Q(city=l_j) &
        Q(main_business=l_k) &
        Q(sub_business=l_l)
    ).exists)()

    if entry_exists:
        print(f"Entry already exists for {l_l} in {l_j}, {l_i}")
        return

    search_key = f'{l_l} in {l_j}, {l_i}'

    if await page.locator('// button[contains( @class, "yAuNSb")]').count() > 0:
        await page.locator('// button[contains( @class, "yAuNSb")]').click()
    await page.wait_for_timeout(1000)
    await page.locator('//input[@id="searchboxinput"]').fill(search_key)
    await page.keyboard.press("Enter")

    final_s = 'na'
    ts = time.time()
    while True:
        if await page.locator(
                ' // a[contains( @ href, "https://www.google.com/maps/place")]').count() > 0:
            final_s = ' // a[contains( @ href, "https://www.google.com/maps/place")]'
            break
        if await page.locator(' // h1[contains( @class, "DUwDvf")]').count() > 0:
            final_s = ' // h1[contains( @class, "DUwDvf")]'
            break
        tm = time.time() - ts
        # print(tm)
        if tm > 20:
            await page.locator('//input[@id="searchboxinput"]').fill(search_key)
            await page.keyboard.press("Enter")
            break
    print(final_s)
    if final_s == ' // a[contains( @ href, "https://www.google.com/maps/place")]':
        await page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

        previously_counted = 0

        while True:
            await page.mouse.wheel(0, 10000)

            if (
                    await page.locator('//a[contains(@href, "https://www.google.com/maps/place")]')
                            .count()
                    >= total
            ):
                listings = await page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).all()
                
                parent_elements = [listing.locator("xpath=..") for listing in listings]

                print(f"Total Scraped: {len(parent_elements)}")

                break
            else:
                if (
                        await page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        == previously_counted
                ):
                    listings = await page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()
                    print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                    break
                else:
                    previously_counted = await page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    print(
                        f"Currently Scraped: ",
                        await page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count(),
                    )
        
        for listing in listings:
            await listing.click()
            # page.wait_for_timeout(1000)

            # name_xpath = '//div[contains(@class, "fontHeadlineSmall")]'
            name_xpath = ' // h1[contains( @class, "DUwDvf")]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            # reviews_span_xpath = '//span[@role="img"]'
            reviews_span_xpath = '//div[@class="F7nice "]'

            business = Business()
            business.state = l_i
            business.city = l_j
            business.main_business = l_k
            business.sub_business = l_l
            while True:
                if await page.locator(name_xpath).count() <= 0:
                    await listing.click()
                else:
                    break

            await page.wait_for_selector(name_xpath)

            try:
                business.name = await page.locator(name_xpath).inner_text(timeout=100)
            except:
                business.name = ""
            try:
                business.address = await page.locator(address_xpath).inner_text(timeout=100)
            except:
                business.address = ""
            try:
                business.website = await page.locator(website_xpath).inner_text(timeout=100)
            except:
                business.website = ""
            try:
                business.phone_number = await page.locator(phone_number_xpath).inner_text(timeout=100)
            except:
                business.phone_number = ""


            try:
                html = await page.locator(reviews_span_xpath).inner_html(timeout=100)

                rating_match = re.search(r'<span aria-hidden="true">([\d.]+)</span>', html)
                if rating_match:
                    business.reviews_average = rating_match.group(1)
                else:
                    business.reviews_average = 0.0

                reviews_match = re.search(r'aria-label="([\d,]+) reviews"', html)
                if reviews_match:
                    business.reviews_count = reviews_match.group(1).replace(',',
                                                                            '')  # Remove commas
                else:
                    business.reviews_count = 0

            except:
                business.reviews_count = 0  # Default value
                business.reviews_average = 0.0  # Default value

            print(business.reviews_count)
            print('hiiiii')
            if business.name != "":
                business_listtt.append(business)
            print("Giiii")




    elif final_s == ' // h1[contains( @class, "DUwDvf")]':

        name_xpath = ' // h1[contains( @class, "DUwDvf")]'
        address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
        website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
        phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
        reviews_span_xpath = '//div[@class="F7nice "]'

        business = Business()
        business.state = l_i
        business.city = l_j
        business.main_business = l_k
        business.sub_business = l_l

        try:
            business.name = await page.locator(name_xpath).inner_text(timeout=100)
        except:
            business.name = ""
        try:
            business.address = await page.locator(address_xpath).inner_text(timeout=100)
        except:
            business.address = ""
        try:
            business.website =await page.locator(website_xpath).inner_text(timeout=100)
        except:
            business.website = ""
        try:
            business.phone_number = await page.locator(phone_number_xpath).inner_text(timeout=100)
        except:
            business.phone_number = ""
        try:
            html = await page.locator(reviews_span_xpath).inner_html(timeout=100)

            # print(html)
            # Extract rating
            rating_match = re.search(r'<span aria-hidden="true">([\d.]+)</span>', html)
            if rating_match:
                business.reviews_average = rating_match.group(1)
            else:
                business.reviews_average = 0.0

            reviews_match = re.search(r'aria-label="([\d,]+) reviews"', html)
            if reviews_match:
                business.reviews_count = reviews_match.group(1).replace(',',
                                                                        '')  # Remove commas
            else:
                business.reviews_count = 0

        except:
            business.reviews_count = 0  # Default value
            business.reviews_average = 0.0  # Default value


        if business.name != "":
            business_listtt.append(business)

    
    else:
        print("page not found")
        return
    if len(business_listtt)>0:
        await save_businesses(business_listtt)

async def main(city_list, b_list):
    print("hi")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.google.com/maps", timeout=60000)
        await page.wait_for_selector('//input[@id="searchboxinput"]')
        await page.wait_for_timeout(5000)

        tasks = []
        stp = 0
        for l_i in city_list.keys():
            if stp == 1:
                break
            stp+=1

            for l_j in city_list[l_i]:
                if stp == 1:
                    break
                for l_k in b_list.keys():
                    try:
                        if b_list[l_k] == []:
                            b_list[l_k].append(l_k)
                    except:
                        pass
                    for l_l in b_list[l_k]:
                        tasks.append(scrape_data(page, l_i, l_j, l_k, l_l))
        
        await asyncio.gather(*tasks)  # Execute all tasks concurrently

        await browser.close()   
# async def main(city_list, b_list):
    
    async with async_playwright() as p:
        browser =await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.google.com/maps", timeout=60000)
        # wait is added for dev phase. can remove it in production

        await page.wait_for_selector('//input[@id="searchboxinput"]')
        await page.wait_for_timeout(5000)
        sr = ['hospitals in Enterprise', 'hospitals in Alabama', 'hospitals in Alaska']
        cnt = 0
    
        for l_i in city_list.keys():
            for l_j in city_list[l_i]:
                for l_k in b_list.keys():
                    try:
                        if b_list[l_k] == []:
                            # print(l_k)
                            b_list[l_k].append(l_k)
                    except:
                        pass
                    for l_l in b_list[l_k]:
                        business_listtt = []
                        entry_exists = await sync_to_async(Business.objects.filter(
                            Q(state=l_i) &
                            Q(city=l_j) &
                            Q(main_business=l_k) &
                            Q(sub_business=l_l)
                        ).exists)()

                        if entry_exists:
                            print(f"Entry already exists for {l_l} in {l_j}, {l_i}")
                            cnt+=1
                            continue
                            
                        search_key = f'{l_l} in {l_j}, {l_i}'
                        cnt += 1
                        # if(cnt==5):
                        #     return
                        print('//////////////////////////////////------', cnt,
                              '------//////////////////////////////////')
                        # time.sleep(0.001)
                        # continue

                        # business_list = BusinessList()  # Initialize BusinessList here

                        if await page.locator(' // button[contains( @class, "yAuNSb")]').count() > 0:
                           await page.locator(' // button[contains( @class, "yAuNSb")]').click()
                        await page.wait_for_timeout(1000)
                        await page.locator('//input[@id="searchboxinput"]').fill(search_key)
                        # page.wait_for_timeout(1000)
                        await page.keyboard.press("Enter")

                        print('start')
                        final_s = 'na'
                        ts = time.time()
                        while True:
                            if await page.locator(
                                    ' // a[contains( @ href, "https://www.google.com/maps/place")]').count() > 0:
                                final_s = ' // a[contains( @ href, "https://www.google.com/maps/place")]'
                                break
                            if await page.locator(' // h1[contains( @class, "DUwDvf")]').count() > 0:
                                final_s = ' // h1[contains( @class, "DUwDvf")]'
                                break
                            tm = time.time() - ts
                            # print(tm)
                            if tm > 20:
                                await page.locator('//input[@id="searchboxinput"]').fill(search_key)
                                await page.keyboard.press("Enter")
                                break
                        print(final_s)
                        if final_s == ' // a[contains( @ href, "https://www.google.com/maps/place")]':
                            await page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

                            previously_counted = 0

                            while True:
                                await page.mouse.wheel(0, 10000)

                                if (
                                        await page.locator('//a[contains(@href, "https://www.google.com/maps/place")]')
                                                .count()
                                        >= total
                                ):
                                    listings = await page.locator(
                                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                                    ).all()
                                    
                                    parent_elements = [listing.locator("xpath=..") for listing in listings]

                                    print(f"Total Scraped: {len(parent_elements)}")

                                    break
                                else:
                                    if (
                                            await page.locator(
                                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                                            ).count()
                                            == previously_counted
                                    ):
                                        listings = await page.locator(
                                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                                        ).all()
                                        print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                                        break
                                    else:
                                        previously_counted = await page.locator(
                                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                                        ).count()
                                        print(
                                            f"Currently Scraped: ",
                                            await page.locator(
                                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                                            ).count(),
                                        )
                            
                            for listing in listings:
                                await listing.click()
                                # page.wait_for_timeout(1000)

                                # name_xpath = '//div[contains(@class, "fontHeadlineSmall")]'
                                name_xpath = ' // h1[contains( @class, "DUwDvf")]'
                                address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                                website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                                phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                                # reviews_span_xpath = '//span[@role="img"]'
                                reviews_span_xpath = '//div[@class="F7nice "]'

                                business = Business()
                                business.state = l_i
                                business.city = l_j
                                business.main_business = l_k
                                business.sub_business = l_l
                                while True:
                                    if await page.locator(name_xpath).count() <= 0:
                                        await listing.click()
                                    else:
                                        break

                                await page.wait_for_selector(name_xpath)

                                try:
                                    business.name = await page.locator(name_xpath).inner_text(timeout=100)
                                except:
                                    business.name = ""
                                try:
                                    business.address = await page.locator(address_xpath).inner_text(timeout=100)
                                except:
                                    business.address = ""
                                try:
                                    business.website = await page.locator(website_xpath).inner_text(timeout=100)
                                except:
                                    business.website = ""
                                try:
                                    business.phone_number = await page.locator(phone_number_xpath).inner_text(timeout=100)
                                except:
                                    business.phone_number = ""


                                try:
                                    html = await page.locator(reviews_span_xpath).inner_html(timeout=100)

                                    rating_match = re.search(r'<span aria-hidden="true">([\d.]+)</span>', html)
                                    if rating_match:
                                        business.reviews_average = rating_match.group(1)
                                    else:
                                        business.reviews_average = 0.0

                                    reviews_match = re.search(r'aria-label="([\d,]+) reviews"', html)
                                    if reviews_match:
                                        business.reviews_count = reviews_match.group(1).replace(',',
                                                                                                '')  # Remove commas
                                    else:
                                        business.reviews_count = 0

                                except:
                                    business.reviews_count = 0  # Default value
                                    business.reviews_average = 0.0  # Default value

                                print(business.reviews_count)
                                print('hiiiii')
                                if business.name != "":
                                    business_listtt.append(business)
                                print("Giiii")


                

                        elif final_s == ' // h1[contains( @class, "DUwDvf")]':

                            name_xpath = ' // h1[contains( @class, "DUwDvf")]'
                            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                            reviews_span_xpath = '//div[@class="F7nice "]'

                            business = Business()
                            business.state = l_i
                            business.city = l_j
                            business.main_business = l_k
                            business.sub_business = l_l

                            try:
                                business.name = await page.locator(name_xpath).inner_text(timeout=100)
                            except:
                                business.name = ""
                            try:
                                business.address = await page.locator(address_xpath).inner_text(timeout=100)
                            except:
                                business.address = ""
                            try:
                                business.website =await page.locator(website_xpath).inner_text(timeout=100)
                            except:
                                business.website = ""
                            try:
                                business.phone_number = await page.locator(phone_number_xpath).inner_text(timeout=100)
                            except:
                                business.phone_number = ""
                            try:
                                html = await page.locator(reviews_span_xpath).inner_html(timeout=100)

                                # print(html)
                                # Extract rating
                                rating_match = re.search(r'<span aria-hidden="true">([\d.]+)</span>', html)
                                if rating_match:
                                    business.reviews_average = rating_match.group(1)
                                else:
                                    business.reviews_average = 0.0

                                reviews_match = re.search(r'aria-label="([\d,]+) reviews"', html)
                                if reviews_match:
                                    business.reviews_count = reviews_match.group(1).replace(',',
                                                                                            '')  # Remove commas
                                else:
                                    business.reviews_count = 0

                            except:
                                business.reviews_count = 0  # Default value
                                business.reviews_average = 0.0  # Default value


                            if business.name != "":
                                business_listtt.append(business)

                        
                        else:
                            print("page not found")
                            continue
                        if len(business_listtt)>0:
                            await save_businesses(business_listtt)

        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()

    if args.search:
        search_for = args.search
    else:
        search_for = "hospitals in Enterprise"

    if args.total:
        total = args.total
    else:
        total = 20

    with open("city_list.json", "r") as json_file:
        city_list = json.load(json_file)
    with open("main_business_list.json", "r") as json_file:
        main_business_list = json.load(json_file)
    with open("other_business_list.json", "r") as json_file:
        other_business_list = json.load(json_file)
    business_list = main_business_list | other_business_list

    asyncio.run(main(city_list, business_list))



