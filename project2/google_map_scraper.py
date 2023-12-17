import os
import django
import asyncio
from django.db.models import Q
import hashlib


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')
django.setup()

from asgiref.sync import sync_to_async


from model.models import Business, store

from playwright.async_api import async_playwright, Error


import os
import time

import json
from playwright.sync_api import sync_playwright

import argparse
import re

async def save_store(store):
    # pass
    await sync_to_async(store.save)()
    

async def save_businesses(business_list):
    # pass
    await sync_to_async(Business.objects.bulk_create)(business_list)    

async def main(city_list, b_list):
    async with async_playwright() as p:
        browser =await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.google.com/maps", timeout=60000)
        await page.wait_for_selector('//input[@id="searchboxinput"]')
     
        await page.wait_for_timeout(5000)
        cnt = 0
        
        for l_i in city_list.keys():
            # cnt1 = 0
            for l_j in city_list[l_i]:
                # if cnt1 >= 2:
                    # continue
                # cnt1+=1
                # cnt2 = 0
                for l_k in b_list.keys():
       
                    try:
                        if b_list[l_k] == []:
                            # print(l_k)
                            b_list[l_k].append(l_k)
                    except:
                        pass
                    # cnt3 = 0
                    for l_l in b_list[l_k]:
                        cnx=1
                        l_i=l_i.replace(" ","-")
                        l_j=l_j.replace(" ","-")
                        l_k=l_k.replace(" ","-")
                        l_l=l_l.replace(" ","-")

                        hash_object = hashlib.sha256(str(l_i+l_j+l_l).encode())
                        hashed_value = hash_object.hexdigest()
                        business_listtt = []
                        entry_exists = await sync_to_async(Business.objects.filter(
                            Q(hash_value=hashed_value) 
                        ).exists)()

                        if entry_exists:
                            print(f"Entry already exists for {l_l} in {l_j}, {l_i}")
                            cnt+=1
                            continue
                            
                        search_key = f'{l_l} in {l_j}, {l_i}'
                        # search_key = 'Law Firm in  AL 36201'
                        cnt += 1
                        # if(cnt==5):
                        #     return
                        print('//////////////////////////////////------', cnt,
                              '------//////////////////////////////////')
                        

                        if await page.locator(' // button[contains( @class, "yAuNSb")]').count() > 0:
                           try:
                            await page.locator(' // button[contains( @class, "yAuNSb")]').click()
                           except:
                               continue 
                        await page.wait_for_timeout(1000)
                        await page.locator('//input[@id="searchboxinput"]').fill(search_key)
                        # page.wait_for_timeout(1000)
                        await page.keyboard.press("Enter")

                        print(f"scrapping for {l_l} in {l_j}, {l_i} ......")

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
                        # print(final_s)
                        if final_s == ' // a[contains( @ href, "https://www.google.com/maps/place")]':
                            await page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

                            previously_counted = 0

                            while True:
                                await page.mouse.wheel(0, 10000)

                                if (
                                        await page.locator(
                                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                                        ).count()
                                        == previously_counted
                                ):
                                    listings = await page.locator(
                                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                                    ).all()
                                    # print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                                    break
                                else:
                                    previously_counted = await page.locator(
                                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                                    ).count()
                                   
                            prv_name = "na"
                         
                            for listing in listings:
                                # print(await page.locator('// div[contains( @class, "GZz5vb")]').count())
                                
                                print("************")
                                # print(listing)
                                print("************")

                            
                                try:
                                    await listing.click()
                                except:
                                    print("Timeout error occurred while clicking the element. Skipping this entry.")
                                    continue  # Continue with the next iteration of the loop

                                if await page.locator('// div[contains( @class, "GZz5vb")]').count() != 0:
                                    print('Sponsored...')
                                    continue
                                
                
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
                                business.hash_value=hashed_value
                                ts = time.time()
                                bs=0
                                while True:
                                    if await page.locator(name_xpath).count() <= 0 or await page.locator(name_xpath).inner_text()==prv_name:
                                        try:
                                            await listing.click()
                                        except:
                                            print("Timeout error occurred while clicking the element. Skipping this entry.")
                                            continue  # Continue with the next iteration of the loop

                                    else:
                                        break
                                    tm = time.time() - ts
                                    if tm > 10:
                                        bs=1
                                        break
                                if bs==1:
                                    continue
                                try:
                                    await page.wait_for_selector(name_xpath)
                                except:
                                    continue    
                                txt = await page.locator(name_xpath).inner_text()
                                prv_name=txt
                                try:
                                    business.name = await page.locator(name_xpath).inner_text(timeout=20)
                                    print(business.name)
                                except:
                                    business.name = ""
                                try:
                                    business.address = await page.locator(address_xpath).inner_text(timeout=20)
                                except:
                                    business.address = ""
                                try:
                                    business.website = await page.locator(website_xpath).inner_text(timeout=20)
                                except:
                                    business.website = ""
                                try:
                                    business.phone_number = await page.locator(phone_number_xpath).inner_text(timeout=20)
                                except:
                                    business.phone_number = ""


                                try:
                                    html = await page.locator(reviews_span_xpath).inner_html(timeout=20)

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

                                # print(business.reviews_count)
                                # print('hiiiii')
                                isitstuck = 0
                                try:
                                    await page.wait_for_selector(' // button[contains( @data-value, "Share")]',timeout=1000)  
                                    print('share.....')                                  
                                    await page.locator(' // button[contains( @data-value, "Share")]').click()
                                    isitstuck=1
                                    print('share')
                                    await page.wait_for_selector(' // button[contains( @data-tooltip, "Embed a map")]',timeout=2000)                                    
                                    await page.locator(' // button[contains( @data-tooltip, "Embed a map")]').click()
                                    print('Embed a map')

                                    await page.wait_for_selector(' //div[@id="modal-dialog"]// input[contains( @class, "yA7sBe")]',timeout=2000)                                    
                                    copied_text = await page.locator(' //div[@id="modal-dialog"]// input[contains( @class, "yA7sBe")]').get_attribute('value')
                                    # print('copied')
                                    # copied_text = await page.evaluate('() => navigator.clipboard.readText()')
                                    # print('peste')
                                    business.map=copied_text
                                    await page.wait_for_selector(' // button[contains( @class, "AmPKde")]',timeout=2000)                                    
                                    # await page.locator(' // button[contains( @class, "AmPKde")][1]').click()
                                    await page.locator('//div[@id="modal-dialog"]//button[contains(@class, "AmPKde")]').click()

                                    print('closed...1')

                                except:
                                    if isitstuck == 1:
                                        try:
                                            print("worst")
                                            await page.wait_for_selector(' // button[contains( @class, "AmPKde")]',timeout=3000)  
                                            await page.locator('//div[@id="modal-dialog"]//button[contains(@class, "AmPKde")]').click()
                                        except:
                                            pass   
                                   
                                    business.map=""

                                if business.map == '':
                                    querry=search_key.replace(' ','%20').replace(',','%C')
                                    business.map = maps=f'<iframe width="600" height="450" src="https://maps.google.com/maps?width=600&amp;height=450&amp;hl=en&amp;q={querry}&amp;ie=UTF8&amp;t=&amp;z=10&amp;iwloc=B&amp;output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>'
                                if business.name != "" and len(business.name)<255 and len(business.address)<255 and len(business.website)<255 and len(business.phone_number)<20:
                                    business_listtt.append(business)
                                print(f"add entry {cnx}")
                                cnx+=1


                            
                            print(f"scrapping for {l_l} in {l_j}, {l_i} completed")




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
                            business.hash_value = hashed_value

                            try:
                                business.name = await page.locator(name_xpath).inner_text(timeout=20)
                            except:
                                business.name = ""
                            try:
                                business.address = await page.locator(address_xpath).inner_text(timeout=20)
                            except:
                                business.address = ""
                            try:
                                business.website =await page.locator(website_xpath).inner_text(timeout=20)
                            except:
                                business.website = ""
                            try:
                                business.phone_number = await page.locator(phone_number_xpath).inner_text(timeout=20)
                            except:
                                business.phone_number = ""
                            try:
                                html = await page.locator(reviews_span_xpath).inner_html(timeout=20)

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

                            
                            isitstuck = 0
                            try:
                                await page.wait_for_selector(' // button[contains( @data-value, "Share")]',timeout=1000)  
                                print('share.....')                                  
                                await page.locator(' // button[contains( @data-value, "Share")]').click()
                                isitstuck=1
                                print('share')
                                await page.wait_for_selector(' // button[contains( @data-tooltip, "Embed a map")]',timeout=2000)                                    
                                await page.locator(' // button[contains( @data-tooltip, "Embed a map")]').click()
                                print('Embed a map')

                                await page.wait_for_selector(' //div[@id="modal-dialog"]// input[contains( @class, "yA7sBe")]',timeout=2000)                                    
                                copied_text = await page.locator(' //div[@id="modal-dialog"]// input[contains( @class, "yA7sBe")]').get_attribute('value')
                                # print('copied')
                                # copied_text = await page.evaluate('() => navigator.clipboard.readText()')
                                # print('peste')
                                business.map=copied_text
                                await page.wait_for_selector(' // button[contains( @class, "AmPKde")]',timeout=2000)                                    
                                # await page.locator(' // button[contains( @class, "AmPKde")][1]').click()
                                await page.locator('//div[@id="modal-dialog"]//button[contains(@class, "AmPKde")]').click()

                                print('closed...1')

                            except:
                                if isitstuck == 1:
                                    try:
                                        print("worst")
                                        await page.wait_for_selector(' // button[contains( @class, "AmPKde")]',timeout=3000)  
                                        await page.locator('//div[@id="modal-dialog"]//button[contains(@class, "AmPKde")]').click()
                                    except:
                                        pass   
                                
                                business.map=""
                            if business.map == '':
                                querry=search_key.replace(' ','%20').replace(',','%C')
                                business.map = maps=f'<iframe width="600" height="450" src="https://maps.google.com/maps?width=600&amp;height=450&amp;hl=en&amp;q={querry}&amp;ie=UTF8&amp;t=&amp;z=10&amp;iwloc=B&amp;output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>'

                            if business.name != "" and len(business.name)<255 and len(business.address)<255 and len(business.website)<255 and len(business.phone_number)<20:
                                business_listtt.append(business)
                                
                            print(f"add entry {cnx}")
                            cnx+=1
                            print(f"scrapping for {l_l} in {l_j}, {l_i} completed")

                        
                        else:
                            print("page not found")
                            continue
                        if len(business_listtt)>0:
                            await save_businesses(business_listtt)
                hash_object1 = hashlib.sha256(str(l_i+l_j).encode())
                hashed_value1 = hash_object1.hexdigest()
                stores = store()
                stores.state = l_i
                stores.city = l_j
                stores.hash_value=hashed_value1
                entry_exists1 = await sync_to_async(store.objects.filter(
                                    Q(hash_value=hashed_value1) 
                                ).exists)()
                if not entry_exists1:
                    await save_store(stores)

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
        # search_for = "Colleges in pune"

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
    business_list = main_business_list
    asyncio.run(main(city_list, business_list))

