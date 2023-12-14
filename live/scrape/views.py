from django.shortcuts import render
from django.http import HttpResponse
import random
from scrape.models import CountryTable,CityTable

# Scraping
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import time
import regex



# def create(request):
#     my_obj = MyTable(field1 = "Nikita",field2='21')
#     my_obj.save()

def store_flag_in_svg(country_flag_url):
    country_flag_url=f'https://livingcost.org{country_flag_url}'
    # print(country_flag_url)
    file_extension = '.svg'

    parent_dir = os.getcwd()
    path = os.path.join(parent_dir,'static/media/flagIcon')
    # print(path)
    # print()

    # if(os.path.exists(path)):
    #     os.rmdir(path)

    # os.mkdir(path)

    r = requests.get(country_flag_url)
    name = country_flag_url.split("/")[-1]

    filename = os.path.join(path, name)

    with open(filename, 'wb') as f:
            f.write(r.content)

    return f"static\media\\flagIcon\{name}"    


def store_city_image(city_img_url):
    # newcity_img_url=f'https://livingcost.org{city_img_url}'
    # print(country_flag_url)
    file_extension = '.jpg'

    parent_dir = os.getcwd()
    path = os.path.join(parent_dir,'static/media/city')
    # print(path)
    # print()

    # if(os.path.exists(path)):
    #     os.rmdir(path)

    # os.mkdir(path)

    r = requests.get(city_img_url)
    name = city_img_url.split("/")[-1]

    filename = os.path.join(path, name)

    with open(filename, 'wb') as f:
            f.write(r.content)

    return f"static\media\\city\{name}"    


def remove_emojis(text):
    text = regex.sub('[\p{Emoji}]', '', text)
    text = text.replace('\u2009','_')
    text = text.replace('.','')
    text = text.replace("'",'')
    text = text.replace('+','')
    text = text.replace('-','_')
    text = text.replace('(','_')
    text = text.replace(')','_')
    text = text.replace('/','')
    text = text.replace('\u200d','_')
    text = text.replace('%','')
    text = text.strip()
    text = text.replace(' ','_')
    text = text.replace('__','_')
    text = text.replace('&','and')
    if text[0]=='_':
      text = text[1:]
    if text[len(text)-1]=="_":
      text = text[0:len(text)-2]
    regex_pattern = r"[^a-zA-Z0-9_]"
    text = regex.sub(regex_pattern, "", text)  
    return text
def remove_symbols(text):
    text = text.replace('%','')
    text = text.replace(' ','')
    text = text.replace('$','')
    text = text.replace('K','')
    text = text.strip()
    return text



# Create your views here.
def home(request):
    n= random.randint(1,100)
    colour_list = ['pink','white','green','purple','sky','yello','red']

    c = random.choice(colour_list)
    create(request)
    return render(request,'index.html',{'number' : n , 'color':c})



country_url_list = []
country_icon_url_list = []
country_ranks_list=[]
country_names_list=[]
def ascrape():
    z=0
    url = 'https://livingcost.org/'
    HEADERS =({'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' , 'Accept-Languge':'en-US, en;q=0.5'}) 
    response = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    web1 = soup.find('table', {'class': 'table table-sm table-striped text-center'})
    tr_tags = web1.find('tbody').find_all('tr')
    
    for tr in tr_tags:
        if z==2:
            break
        z+=1
        rank = tr.find('td',{'class':"best-rank align-middle"}).text
        country_name = tr.find('th',{'class':"cost-country text-left"}).find('span').text
        country_ranks_list.append(rank)
        country_names_list.append(country_name)
        country_link = tr.find('th',{'class':"cost-country text-left"}).find('a').get('href')
        country_url_list.append(country_link)
        country_icon_url = tr.find('th',{'class':"cost-country text-left"}).find('img').get('src')
        country_icon_url = store_flag_in_svg(country_icon_url)
        country_icon_url_list.append(country_icon_url)
        country_d = {'rank':rank, 'country_name':country_name,'country_flag_url':country_icon_url}
        print(country_d)





















         
def scrape(request):
    ascrape()
    all_countries=[]
    HEADERS =({'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' , 'Accept-Languge':'en-US, en;q=0.5'})
    counter=0
    for country_url in country_url_list: 
        tm = time.time() 
        response1 = requests.get(country_url,headers=HEADERS)
        soup1 = BeautifulSoup(response1.content,'html.parser')
        all_table_in_country = soup1.find('table', {'class': 'table table-sm'})
        r = all_table_in_country.find('tbody').find_all('tr')
        k = 0
        country_d={}
        country_d['Rank']=country_ranks_list[counter]
        country_d['Name']=country_names_list[counter]
        country_d['country_icon_url']=country_icon_url_list[counter]
        counter+=1
        for row in r:
            if k<5: 
                key1 = row.find('th').text
                key1 = key1.strip()
                key1 = remove_emojis(key1)
                # print(key1)
                key1 = key1+'_1p'
                k+=1
                key2 = key1[:len(key1)-3]+'_3p'   
                country_d[key1] = remove_symbols(row.find_all('td')[0].find('span').text)
                country_d[key2] = remove_symbols(row.find_all('td')[1].find('span').text )
                continue
            key = row.find('th').text
            key = key.strip()
            key = remove_emojis(key)
            country_d[key] = remove_symbols(row.find_all('td')[0].find('div').text)
            k+=1

            all_table_in_country1=soup1.find_all('table', {'class': 'table table-sm table-striped table-hover'})

            for tab in all_table_in_country1:
                r = tab.find('tbody').find_all('tr')

                for row in r:
                    key = row.find('th').text
                    key = key.split(',')
                    if len(key)>1:
                        key[0] = key[0].strip()
                        key[0] = remove_emojis(key[0])
                        key=key[0]

                        country_d[key] = remove_symbols(row.find_all('td')[0].find('span').text )
                    else:
                        key = row.find('th').text
                        key = key.strip()
                        key = remove_emojis(key).strip()

                        country_d[key] =remove_symbols(row.find_all('td')[0].find('div').text ) 

        # my_obj = Country(field1 = "Nikita",field2='21')
        # my_obj.save()
        # print("nnnnnkjhsidfbsiudhfbdsbcihsbhcsnv =====  =   ",end=' ')
        # print(country_d['Total_with_rent_1p'])
        country_obj = CountryTable(Rank =  country_d['Rank'],
                                   Name =  country_d['Name'],
                                   Total_with_rent_1p =  country_d['Total_with_rent_1p'],
                                   Total_with_rent_3p =  country_d['Total_with_rent_3p'],
                                   _Without_rent_1p =  country_d['_Without_rent_1p'],
                                   _Without_rent_3p =  country_d['_Without_rent_3p'],
                                   Rent_and_Utilities_1p =  country_d['Rent_and_Utilities_1p'],
                                   Rent_and_Utilities_3p =  country_d['Rent_and_Utilities_3p'],
                                   _Food_1p =  country_d['_Food_1p'],
                                   _Food_3p =  country_d['_Food_3p'],
                                   Transport_1p =  country_d['Transport_1p'],
                                   Transport_3p =  country_d['Transport_3p'],
                                   Monthly_salary_after_tax =  country_d['Monthly_salary_after_tax'],Lunch_Menu =  country_d['Lunch_Menu'],Dinner_in_a_Restaurant =  country_d['Dinner_in_a_Restaurant'],Fast_food_meal =  country_d['Fast_food_meal'],Beer_in_a_Pub =  country_d['Beer_in_a_Pub'],Cappuccino =  country_d['Cappuccino'],Pepsi_Coke =  country_d['Pepsi_Coke'],
                                   _bedroom_apartment_in_city_Center =  country_d['_bedroom_apartment_in_city_Center'],Cheap_bedroom_apartment =  country_d['Cheap_bedroom_apartment'],Utility_Bill_one_person =  country_d['Utility_Bill_one_person'],Utility_Bill_for_a_Family =  country_d['Utility_Bill_for_a_Family'],Internet_plan =  country_d['Internet_plan'],Mortgage_Interest_Rate_for_Years =  country_d['Mortgage_Interest_Rate_for_Years'],_Apartment_price_to_Buy_in_city_Center =  country_d['_Apartment_price_to_Buy_in_city_Center'],House_price_to_Buy_in_Suburbs =  country_d['House_price_to_Buy_in_Suburbs'],Local_transport_ticket =  country_d['Local_transport_ticket'],_Monthly_ticket_local_transport =  country_d['_Monthly_ticket_local_transport'],Taxi_Ride =  country_d['Taxi_Ride'],
                                   Gas_Petrol =  country_d['Gas_Petrol'],Milk =  country_d['Milk'],Bread =  country_d['Bread'],Rice =  country_d['Rice'],Eggs =  country_d['Eggs'],Cheese =  country_d['Cheese'],Chicken_Breast =  country_d['Chicken_Breast'],Round_Steak =  country_d['Round_Steak'],Apples =  country_d['Apples'],Banana =  country_d['Banana'],Oranges =  country_d['Oranges'],Tomato =  country_d['Tomato'],Potato =  country_d['Potato'],Onion =  country_d['Onion'],Water =  country_d['Water'],Coca_Cola_Pepsi =  country_d['Coca_Cola_Pepsi'],Wine_mid_price =  country_d['Wine_mid_price'],Beer =  country_d['Beer'],Cigarette_pack =  country_d['Cigarette_pack'],Cold_medicince =  country_d['Cold_medicince'],Hair_Shampoo =  country_d['Hair_Shampoo'],Toilet_paper =  country_d['Toilet_paper'],Toothpaste =  country_d['Toothpaste'],_Gym_Membership =  country_d['_Gym_Membership'],Cinema_Ticket =  country_d['Cinema_Ticket'],Doctors_visit =  11,Haircut =  country_d['Haircut'],Brand_Jeans =  country_d['Brand_Jeans'],Brand_Sneakers =  country_d['Brand_Sneakers'],
                                   Daycare_or_Preschool =  country_d['Daycare_or_Preschool'],International_Primary_School =  country_d['International_Primary_School'],GDP_per_capita =  country_d['GDP_per_capita'],Human_freedom_index =  country_d['Human_freedom_index'],English_speaking =  country_d['English_speaking'],
                                   _Population =  country_d['_Population'],
                                   _Life_expectancy =  country_d['_Life_expectancy'],
                                   country_icon_url =  country_d['country_icon_url']
                                   )

        country_obj.save()
        # print(country_d)
        # all_countries.append(country_d)     
        print(time.time()-tm)

        state_soup = soup1.findAll('table',{'class':'table table-sm table-striped text-center'})
        city_soup = soup1.find('ol',{'class':'row geo-gutters mb-4 list-unstyled'})

        states_names=[]
        states_links=[]
        city_names=[]
        city_links=[]
        city_img_links=[]
        
        if(len(state_soup)>0):
            states_tr = state_soup[0].find('tbody').findAll('tr')
            for state_tr in states_tr:
                states_names.append(state_tr.find('a').text)    
                states_links.append(state_tr.find('a').get('href'))
            for st_l in states_links:
                state_page_response = requests.get(st_l,headers=HEADERS)
                statedata_soup = BeautifulSoup(state_page_response.content, 'html.parser')
                statedata_soup = statedata_soup.find('ol',{'class':'row geo-gutters mb-4 list-unstyled'})
                city_data_lis = statedata_soup.findAll('li')
                for city_data_li in city_data_lis:
                    city_img_links.append(city_data_li.find('img').get('src'))
                    city_links.append(city_data_li.find('a').get('href'))
                    city_names.append(city_data_li.find('h3').text)


          
        else:
            city_lis = city_soup.findAll('li')
            for city_li in city_lis:
                city_img_links.append(city_li.find('img').get('src'))
                city_links.append(city_li.find('a').get('href'))
                city_names.append(city_li.find('h3').text)



        print(city_img_links)

        counter_city = 0
        if len(city_links)>0:
            for state_l in city_links:
                city_page_response = requests.get(state_l,headers=HEADERS)
                city_soup = BeautifulSoup(city_page_response.content, 'html.parser')
                
                ########################################################################
                all_table_in_country_city = city_soup.find('table', {'class': 'table table-sm'})
                r_city = all_table_in_country_city.find('tbody').find_all('tr')
                k_city = 0
                country_d_city={}
                country_d_city['Name']=city_names[counter_city]
                counter_city+=1
                for row_city in r_city:
                    if k_city<5: 
                        key1_city = row_city.find('th').text
                        key1_city = key1_city.strip()
                        key1_city = remove_emojis(key1_city)
                        # print(key1)
                        key1_city = key1_city+'_1p'
                        k_city+=1
                        key2_city = key1_city[:len(key1_city)-3]+'_3p'   
                        country_d_city[key1_city] = remove_symbols(row_city.find_all('td')[0].find('span').text)
                        country_d_city[key2_city] = remove_symbols(row_city.find_all('td')[1].find('span').text )
                        continue
                    key_city = row_city.find('th').text
                    key_city = key_city.strip()
                    key_city = remove_emojis(key_city)
                    country_d_city[key_city] = remove_symbols(row_city.find_all('td')[0].find('div').text)
                    k_city+=1

                    all_table_in_country1_city=city_soup.find_all('table', {'class': 'table table-sm table-striped table-hover'})

                    for tab_city in all_table_in_country1_city:
                        rs = tab_city.find('tbody').find_all('tr')

                        for row_citys in rs:
                            key_city = row_citys.find('th').text
                            key_city = key_city.split(',')
                            if len(key_city)>1:
                                key_city[0] = key_city[0].strip()
                                key_city[0] = remove_emojis(key_city[0])
                                key_city=key_city[0]

                                country_d_city[key_city] = remove_symbols(row_citys.find_all('td')[0].find('span').text )
                            else:
                                key_city = row_citys.find('th').text
                                key_city = key_city.strip()
                                key_city = remove_emojis(key_city).strip()

                                country_d_city[key_city] =remove_symbols(row_citys.find_all('td')[0].find('div').text ) 

                # my_obj = Country(field1 = "Nikita",field2='21')
                # my_obj.save()
                # print("nnnnnkjhsidfbsiudhfbdsbcihsbhcsnv =====  =   ",end=' ')
                # print(country_d['Total_with_rent_1p'])
                advance_data_city = city_soup.findAll('table', {'class': 'table table-sm'})[1].findAll('tr')
                Closest_airport = advance_data_city[0].findAll('td')[0].text
                Closest_airport_val = advance_data_city[0].findAll('td')[1].text
                Air_quality = advance_data_city[1].findAll('td')[0].text
                Air_quality_val = advance_data_city[1].findAll('td')[1].text
                try:
                    Best_university_rank = advance_data_city[2].findAll('td')[0].text
                    Best_university_rank_val = advance_data_city[2].findAll('td')[1].text
                except:
                    Best_university_rank = '-'
                    Best_university_rank_val = '-'

                
                country_flag_url_city = store_city_image(city_img_links[counter_city-1])
                # print(store_city_image(city_img_links[counter_city-1]))

                city_obj = CityTable(
                                        country_flag_url = country_flag_url_city,
                                        country_name = country_names_list[counter-1],
                                        Closest_airport = Closest_airport,
                                        Closest_airport_val=Closest_airport_val,
                                        Air_quality=Air_quality,
                                        Air_quality_val=Air_quality_val,
                                        Best_university_rank=Best_university_rank,
                                        Best_university_rank_val=Best_university_rank_val,
                                        Name =  country_d_city['Name'],
                                        Total_with_rent_1p =  country_d_city['Total_with_rent_1p'],
                                        Total_with_rent_3p =  country_d_city['Total_with_rent_3p'],
                                        _Without_rent_1p =  country_d_city['_Without_rent_1p'],
                                        _Without_rent_3p =  country_d_city['_Without_rent_3p'],
                                        Rent_and_Utilities_1p =  country_d_city['Rent_and_Utilities_1p'],
                                        Rent_and_Utilities_3p =  country_d_city['Rent_and_Utilities_3p'],
                                        _Food_1p =  country_d_city['_Food_1p'],
                                        _Food_3p =  country_d_city['_Food_3p'],
                                        Transport_1p =  country_d_city['Transport_1p'],
                                        Transport_3p =  country_d_city['Transport_3p'],
                                        Monthly_salary_after_tax =  country_d_city['Monthly_salary_after_tax'],Lunch_Menu =  country_d_city['Lunch_Menu'],Dinner_in_a_Restaurant =  country_d_city['Dinner_in_a_Restaurant'],Fast_food_meal =  country_d_city['Fast_food_meal'],Beer_in_a_Pub =  country_d_city['Beer_in_a_Pub'],Cappuccino =  country_d_city['Cappuccino'],Pepsi_Coke =  country_d_city['Pepsi_Coke'],
                                        _bedroom_apartment_in_city_Center =  country_d_city['_bedroom_apartment_in_city_Center'],Cheap_bedroom_apartment =  country_d_city['Cheap_bedroom_apartment'],Utility_Bill_one_person =  country_d_city['Utility_Bill_one_person'],Utility_Bill_for_a_Family =  country_d_city['Utility_Bill_for_a_Family'],Internet_plan =  country_d_city['Internet_plan'],Mortgage_Interest_Rate_for_Years =  country_d_city['Mortgage_Interest_Rate_for_Years'],_Apartment_price_to_Buy_in_city_Center =  country_d_city['_Apartment_price_to_Buy_in_city_Center'],House_price_to_Buy_in_Suburbs =  country_d_city['House_price_to_Buy_in_Suburbs'],Local_transport_ticket =  country_d_city['Local_transport_ticket'],_Monthly_ticket_local_transport =  country_d_city['_Monthly_ticket_local_transport'],Taxi_Ride =  country_d_city['Taxi_Ride'],
                                        Gas_Petrol =  country_d_city['Gas_Petrol'],Milk =  country_d_city['Milk'],Bread =  country_d_city['Bread'],Rice =  country_d_city['Rice'],Eggs =  country_d_city['Eggs'],Cheese =  country_d_city['Cheese'],Chicken_Breast =  country_d_city['Chicken_Breast'],Round_Steak =  country_d_city['Round_Steak'],Apples =  country_d_city['Apples'],Banana =  country_d_city['Banana'],Oranges =  country_d_city['Oranges'],Tomato =  country_d_city['Tomato'],Potato =  country_d_city['Potato'],Onion =  country_d_city['Onion'],Water =  country_d_city['Water'],Coca_Cola_Pepsi =  country_d_city['Coca_Cola_Pepsi'],Wine_mid_price =  country_d_city['Wine_mid_price'],Beer =  country_d_city['Beer'],Cigarette_pack =  country_d_city['Cigarette_pack'],Cold_medicince =  country_d_city['Cold_medicince'],Hair_Shampoo =  country_d_city['Hair_Shampoo'],Toilet_paper =  country_d_city['Toilet_paper'],Toothpaste =  country_d_city['Toothpaste'],_Gym_Membership =  country_d_city['_Gym_Membership'],Cinema_Ticket =  country_d_city['Cinema_Ticket'],Doctors_visit =  11,Haircut =  country_d_city['Haircut'],Brand_Jeans =  country_d_city['Brand_Jeans'],Brand_Sneakers =  country_d_city['Brand_Sneakers'],
                                        Daycare_or_Preschool =  country_d_city['Daycare_or_Preschool'],International_Primary_School =  country_d_city['International_Primary_School'],
                                        _Population =  country_d_city['_Population'],
                                        )
                ########################################################################

                print(country_d_city)
                city_obj.save()
    # data_ex = pd.DataFrame(all_countries)
    # data_ex.to_excel('data.xlsx')
    return HttpResponse("Scraping ...")