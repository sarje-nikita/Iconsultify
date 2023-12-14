from django.shortcuts import render, redirect
from scrape.models import CountryTable, CityTable, StateTable, Author
from django.http import HttpResponse
from django.db.models import Max, Q
import os

import random


from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


# Create your views here.
def langingpage(request):
    my_values = CountryTable.objects.filter().values(
        'Rank', 'Name', 'country_icon_url', 'Total_with_rent_1p')
    dict_list = list(my_values.values(
        'Rank', 'Name', 'country_icon_url', 'Total_with_rent_1p'))
    max_vals = {'Total_with_rent_1p': CountryTable.objects.aggregate(
        Max('Total_with_rent_1p'))['Total_with_rent_1p__max']}
    m_p = CityTable.objects.aggregate(Max('_Population'))['_Population__max']
    max_Population = float(m_p.replace('M', '').replace(
        'K', '').replace('k', '').replace('B', '').strip())
    if 'K' in m_p:
        max_Population *= 1000
    elif 'M' in m_p:
        max_Population *= 1000000
    elif 'B' in m_p:
        max_Population *= 10000000
    max_vals['max_Population'] = max_Population

    my_values1 = CityTable.objects.filter().values('Name')
    dict_list1 = list(my_values1.values('Name', '_Population',
                      'country_flag_url', 'country_name', 'Total_with_rent_1p','state_name'))
    for i in dict_list1:
        # print(i['_Population'])
        if 'K' in i['_Population']:
            pass
        elif 'M' in i['_Population']:
            pass
        elif 'B' in i['_Population']:
            pass
        else:
            i['_Population'] = i['_Population']+'K'

        temp = i['_Population']
        i['Population'] = temp
        # print(dict_list1)
    dict_list1 = random.sample(dict_list1, min(50, len(dict_list1)))
    dict_list.sort(key=lambda x: x['Rank'])

    return render(request, 'index.html', {'list': dict_list, 'max_vals': max_vals, 'dict_list1': dict_list1})

from num2words import num2words
# import cairosvg

def cost(request, name):
    # print('------')
    # print(name)
    # print(name.title())
    # print('------')
    my_values_c = CityTable.objects.filter(country_name=name)
    city_dict_list = list(my_values_c.values())
    city_dict_list = random.sample(
        city_dict_list, min(50, len(city_dict_list)))
    
    myst = StateTable.objects.filter(country_name=name.title())
    state_list = []
    # print(city_dict_list)
    if not city_dict_list:
        return redirect('/')
    # print('hi')
    if myst:
        state_list = list(myst.values(
            'Total_with_rent_1p', 'Name', 'country_name'))
        state_list.sort(key=lambda x: x['Total_with_rent_1p'], reverse=True)
        # print(state_list)
        j = 1
        for i in state_list:
            i['Rank'] = j
            j += 1
    
    for dic_c in city_dict_list:
        tm = dic_c.pop('_Population')
        dic_c['Population'] = tm

    # print(dic_c)

    max_vals = {}
    # print(name,'-----------------------------------------',name.title())
    my_values = CountryTable.objects.filter(Name=name)
    dict_list = list(my_values.values()) 
    # print(dict_list)
    my_dict = dict_list[0]
    for entry in my_dict.keys():
        max_vals[entry] = CountryTable.objects.aggregate(Max(entry))[
            f'{entry}__max']
    mv2 = max_vals.pop('_Without_rent_3p')
    mv1 = max_vals.pop('_Without_rent_1p')
    mv3 = max_vals.pop('_Food_1p')
    mv4 = max_vals.pop('_Food_3p')
    mv5 = max_vals.pop('_Life_expectancy')
    mv6 = max_vals.pop('_Population')
    mv7 = max_vals.pop('_bedroom_apartment_in_city_Center')
    mv8 = max_vals.pop('_Apartment_price_to_Buy_in_city_Center')
    mv9 = max_vals.pop('_Monthly_ticket_local_transport')
    mv10 = max_vals.pop('_Gym_Membership')
    temp = float(mv6.replace('M', '').replace(
        'K', '').replace('B', '').strip())
    if 'K' in mv6:
        temp *= 1000
    elif 'M' in mv6:
        temp *= 1000000
    elif 'B' in mv6:
        temp *= 10000000

    # print(dict_list[0]['_Without_rent_1p'])
    max_vals['Without_rent_1p'] = mv1
    max_vals['Without_rent_3p'] = mv2
    max_vals['Food_1p'] = mv3
    max_vals['Food_3p'] = mv4
    max_vals['Life_expectancy'] = mv5
    max_vals['Population'] = temp
    max_vals['bedroom_apartment_in_city_Center'] = mv7
    max_vals['Apartment_price_to_Buy_in_city_Center'] = mv8
    max_vals['Monthly_ticket_local_transport'] = mv9
    max_vals['Gym_Membership'] = mv10

    v1 = my_dict.pop('_Without_rent_1p')
    v2 = my_dict.pop('_Without_rent_3p')
    v3 = my_dict.pop('_Food_1p')
    v4 = my_dict.pop('_Food_3p')
    v5 = my_dict.pop('_Life_expectancy')
    v6 = my_dict.pop('_Population')
    v7 = my_dict.pop('_bedroom_apartment_in_city_Center')
    v8 = my_dict.pop('_Apartment_price_to_Buy_in_city_Center')
    v9 = my_dict.pop('_Monthly_ticket_local_transport')
    v10 = my_dict.pop('_Gym_Membership')

    # print(dict_list[0]['_Without_rent_1p'])_Gym_Membership
    my_dict['Without_rent_1p'] = v1
    my_dict['Without_rent_3p'] = v2
    my_dict['Food_1p'] = v3
    my_dict['Food_3p'] = v4
    my_dict['Life_expectancy'] = v5

    temp2 = float(v6.replace('M', '').replace(
        'K', '').replace('B', '').strip())
    if 'K' in v6:
        temp2 *= 1000
    elif 'M' in v6:
        temp2 *= 1000000
    elif 'B' in v6:
        temp2 *= 10000000
    # print(temp)
    my_dict['Population'] = temp2
    # print(temp2)
    my_dict['population_txt'] = v6
    my_dict['bedroom_apartment_in_city_Center'] = v7
    my_dict['Apartment_price_to_Buy_in_city_Center'] = v8
    my_dict['Monthly_ticket_local_transport'] = v9
    my_dict['Gym_Membership'] = v10
    pram1=1
    pram2=True
    # my_dict['Total_with_rent_1p']=1000
    if my_dict['Total_with_rent_1p']>978:
        pram1 = my_dict['Total_with_rent_1p']/978
        pram2 = True
    else:
        pram1 = 978/my_dict['Total_with_rent_1p']
        pram2 = False   

    my_dict['pram1']=round(pram1, 2)
    my_dict['pram2']=pram2

    pram3 = CountryTable.objects.filter(Total_with_rent_1p__gt=my_dict['Total_with_rent_1p'])
    # print(len(pram3))
    my_dict['pram3']=len(pram3)+1

    temp = list(CountryTable.objects.filter().values())
    temp.sort(key=lambda x: x['Quality_of_life'], reverse=True)
    pram4=0
    # print(name.title(),"gggg")
    for x in temp:
        # print(x['Name'])
        if x['Name']==name.title():
            pram4+=1
            break
        pram4+=1

    my_dict['pram4']=pram4
    # print(pram4)

    pram5 = round(my_dict['Total_with_rent_1p']/my_dict['Monthly_salary_after_tax'],1)
    pram5 = num2words(pram5)
    my_dict['pram5']=pram5








    temp_images_dir = os.path.join(settings.BASE_DIR, 'static/media/compare_country')
    for filename in os.listdir(temp_images_dir):
        file_path = os.path.join(temp_images_dir, filename)
        os.remove(file_path)
    temp1=[]
    names1=[]
    pr=[]
    countryDict =list(CountryTable.objects.filter().values())
    for i in countryDict:
        nm=i['Name']
        u=f'static/media/flag/{nm}.png' 

        resized_image = Image.open(u)
        # resized_image = resized_image.resize((300, 200))
        # resized_image = resized_image.convert('RGB')
        # resized_image.save(f'static/media/flag/{nm}.png')
        temp1.append(np.array(resized_image))

        names1.append(i['Name'])
        # print(i['Name']) 
        pr.append(i['Total_with_rent_1p'])
    if len(names1)%2!=0:
        temp1.pop()
        names1.pop()    
        pr.pop()    
    image_array1s=temp1[:len(temp1)//2]  
    # for i in image_array1s:
    #     print(Image.fromarray(i).save('c.png'))  
    image_array2s=temp1[len(temp1)//2:]
    name1s=names1[:len(temp1)//2]
    name2s=names1[len(temp1)//2:]
    p1s=pr[len(temp1)//2:]
    p2s=pr[:len(temp1)//2]
    com_urls = []
    # print(names)
    # print(len(name1),len(name2),len(p1),len(p2),len(names),len(temp))
    for i in range(len(name1s)):
        com_urls.append([name1s[i],name2s[i],p2s[i],p1s[i]])
    # print(com_urls) 

    # with open('mask.pickle', 'rb') as f: 
    #     mask = pickle.load(f)
    #     print(mask)

    # t = time.time()

    # num_processes = 3  # Adjust the number of processes as needed
    # pool = Pool(num_processes)

    # num_iterations = len(name1)

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = []
    #     for i in range(num_iterations):
            
    #         futures.append(executor.submit(process_image,i, image_array1[i], image_array2[i], mask,temp_images_dir,name1[i],name2[i]))
            
    #     # Wait for all the threads to complete
    #     concurrent.futures.wait(futures)
    #     print("weighting")
    










    temp_images_dir = os.path.join(settings.BASE_DIR, 'static/media/compare')
    for filename in os.listdir(temp_images_dir):
        file_path = os.path.join(temp_images_dir, filename)
        os.remove(file_path)
    temp=[]
    names=[]
    p=[]
    
    # image_pathx = 'Afghanistan.png'
    # imagex = Image.open(image_pathx)
    # imagex = imagex.convert('RGB')

    # image_arrayx = np.array(imagex)  # Specify data type as unsigned 8-bit integers
    # new_imagex = Image.fromarray(image_arrayx)
    # new_imagex.save('c.png')
    citydic =list(CityTable.objects.filter(country_name=name).values()) 
    for i in citydic :
        try:
       	    cnu = i['Name'].lower().replace("'","-")
            ctur = f"static/media/city/{cnu}.jpg"
            print(ctur)
            temp.append(np.array(Image.open(ctur)))
        except:
            continue
        # print(Image.fromarray(np.array(Image.open('Afghanistan.png'))).save('c.png'))
        # print(Image.open(i['country_flag_url']).size,'-------------------------')
        names.append(i['Name'])
        p.append(i['Total_with_rent_1p'])
    if len(temp)%2!=0:
        temp.pop()
        names.pop()    
        p.pop() 

    if len(p)>100:
        p=p[:100]       
        temp=temp[:100]       
        names=names[:100]       
    nimage_array1=temp[:len(temp)//2]    
    nimage_array2=temp[len(temp)//2:]
    nname1=names[:len(temp)//2]
    nname2=names[len(temp)//2:]
    np1=p[len(temp)//2:]
    np2=p[:len(temp)//2]
    com_url2 = []
    for i in range(len(nname1)):
        com_url2.append([nname1[i],nname2[i],np1[i],np2[i]])
    # print(com_url2,len(nname1))
    # print(len(nname1))
    nname1=nname1 + name1s 
    nname2=nname2 + name2s
    np1=np1 + p1s
    np2=np2 + p2s
    nimage_array1=nimage_array1 + image_array1s
    nimage_array2=nimage_array2 + image_array2s
    
    with open('mask.pickle', 'rb') as f:
        mask = pickle.load(f)
        # print(mask)

    t = time.time()

    num_processes = 3  # Adjust the number of processes as needed
    pool = Pool(num_processes)

    num_iterations = len(nname1)
    print(len(nname1))
    # indices = range(num_iterations)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(num_iterations):
            
            futures.append(executor.submit(process_image,i, nimage_array1[i], nimage_array2[i], mask,temp_images_dir,nname1[i],nname2[i]))
            
        # Wait for all the threads to complete
        concurrent.futures.wait(futures)
        
    # print(len(citydic)) 
    author={}
    day = random.randint(1, 31)
    month = random.randint(1, 12)
    year = 2022
    date = f"{day:02d}-{month:02d}-{year}"
    author['date']=date

    return render(request, 'country.html', {'list': my_dict, 'max_vals': max_vals, 'city_dict_list': city_dict_list, 'state_list': state_list, 'com_url':com_urls,'com_url2':com_url2,'author':author
                                            })
 
# city_cost


def city_cost(request, country_name, city_name):
    
    my_values1 = CityTable.objects.filter(Name=city_name)
    my_values2 = StateTable.objects.filter(Name=city_name.title())
    dict_list1 = list(my_values1.values())
    dict_list2 = list(my_values2.values())

    if not my_values1 and not my_values2:
        return redirect('/')

    if len(dict_list1) > 0:
        my_dict = dict_list1[0]

    else:
        my_dict = dict_list2[0]

    if country_name != my_dict['country_name']:
        return redirect('/')

    if 'state_name' in my_dict.keys() and not my_dict['state_name'] == '-':
        return redirect('/cost/' + country_name + '/' + my_dict['state_name'] + '/' + city_name)

    max_vals = {}

    for entry in my_dict.keys():
        if entry == 'State_rank':
            continue

        max_vals[entry] = CityTable.objects.aggregate(Max(entry))[
            f'{entry}__max']
    mv2 = max_vals.pop('_Without_rent_3p')
    mv1 = max_vals.pop('_Without_rent_1p')
    mv3 = max_vals.pop('_Food_1p')
    mv4 = max_vals.pop('_Food_3p')
    mv6 = max_vals.pop('_Population')
    mv7 = max_vals.pop('_bedroom_apartment_in_city_Center')
    mv8 = max_vals.pop('_Apartment_price_to_Buy_in_city_Center')
    mv9 = max_vals.pop('_Monthly_ticket_local_transport')
    mv10 = max_vals.pop('_Gym_Membership')
    temp = float(mv6.replace('M', '').replace(
        'K', '').replace('B', '').replace('k', '').strip())
    if 'K' in mv6:
        temp *= 1000
    elif 'M' in mv6:
        temp *= 1000000
    elif 'B' in mv6:
        temp *= 10000000

    # print(dict_list[0]['_Without_rent_1p'])
    max_vals['Without_rent_1p'] = mv1
    max_vals['Without_rent_3p'] = mv2
    max_vals['Food_1p'] = mv3
    max_vals['Food_3p'] = mv4
    # max_vals['Life_expectancy'] = mv5
    max_vals['Population'] = temp
    max_vals['bedroom_apartment_in_city_Center'] = mv7
    max_vals['Apartment_price_to_Buy_in_city_Center'] = mv8
    max_vals['Monthly_ticket_local_transport'] = mv9
    max_vals['Gym_Membership'] = mv10

    v1 = my_dict.pop('_Without_rent_1p')
    v2 = my_dict.pop('_Without_rent_3p')
    v3 = my_dict.pop('_Food_1p')
    v4 = my_dict.pop('_Food_3p')
    # v5 = my_dict.pop('_Life_expectancy')
    v6 = my_dict.pop('_Population')
    v7 = my_dict.pop('_bedroom_apartment_in_city_Center')
    v8 = my_dict.pop('_Apartment_price_to_Buy_in_city_Center')
    v9 = my_dict.pop('_Monthly_ticket_local_transport')
    v10 = my_dict.pop('_Gym_Membership')

    # print(dict_list[0]['_Without_rent_1p'])_Gym_Membership
    my_dict['Without_rent_1p'] = v1
    my_dict['Without_rent_3p'] = v2
    my_dict['Food_1p'] = v3
    my_dict['Food_3p'] = v4
    # my_dict['Life_expectancy'] = v5

    temp2 = float(v6.replace('M', '').replace(
        'K', '').replace('B', '').strip())
    if 'K' in v6:
        temp2 *= 1000
    elif 'M' in v6:
        temp2 *= 1000000
    elif 'B' in v6:
        temp2 *= 10000000
    # print(v9)
    my_dict['Population'] = temp2
    my_dict['population_txt'] = v6
    my_dict['bedroom_apartment_in_city_Center'] = v7
    my_dict['Apartment_price_to_Buy_in_city_Center'] = v8
    my_dict['Monthly_ticket_local_transport'] = v9
    my_dict['Gym_Membership'] = v10

    print('aaaaaaaaaaaaaaaaaaaaaa')
    author={}
    day = random.randint(1, 31)
    month = random.randint(1, 12)
    year = 2022
    date = f"{day:02d}-{month:02d}-{year}"
    author['date']=date
    if my_values2:
        print('State')
        my_values_c = CityTable.objects.filter(state_name=city_name.title())
        city_dict_list = list(my_values_c.values())
        city_dict_list = random.sample(
            city_dict_list, min(50, len(city_dict_list)))
        for i in city_dict_list:
            i['Population'] = i.pop('_Population')



        pram1=1
        pram2=True
        tem = list(StateTable.objects.filter().values())
        tem.sort(key=lambda x: x['Total_with_rent_1p'],reverse=True) 
        state_avrage=0
        pram3=1
        cn1=0
        for en in tem:
            state_avrage+=en['Total_with_rent_1p']
            print(en['Total_with_rent_1p'])
            if en['Name']!=city_name.title() and cn1==0:
                pram3+=1
                print(pram3)
            else:
                cn1=1    
        state_avrage=state_avrage/len(tem)
        if my_dict['Total_with_rent_1p']>state_avrage:
            pram1 = my_dict['Total_with_rent_1p']/state_avrage
            pram2 = True
        else:
            pram1 = state_avrage/my_dict['Total_with_rent_1p']
            pram2 = False   

        my_dict['pram1']=round(pram1, 2)
        my_dict['pram2']=pram2

       
        my_dict['pram3']=pram3

        tem.sort(key=lambda x: x['Quality_of_life'],reverse=True) 
        pram4=0
        for en in tem:
            if en['Name']==city_name.title():
                break
                
            pram4+=1 
       
        my_dict['pram4']=pram4+1
        # print(pram4)

        pram5 = round(my_dict['Total_with_rent_1p']/my_dict['Monthly_salary_after_tax'],1)
        pram5 = num2words(pram5)
        my_dict['pram5']=pram5    
        my_dict['pram6']=len(tem)    


        return render(request, 'state.html', {'list': my_dict, 'max_vals': max_vals, 'city_dict_list': city_dict_list,'author':author})
    else:
        print('city')
        my_values_c = CityTable.objects.filter(
            country_name=country_name.title())
        city_dict_list = list(my_values_c.values())
        city_dict_list = random.sample(
            city_dict_list, min(50, len(city_dict_list)))
        for i in city_dict_list:
            i['Population'] = i.pop('_Population')

    
        return render(request, 'city.html', {'list': my_dict, 'max_vals': max_vals, 'city_dict_list': city_dict_list,'author':author})


def city_with_state_cost(request, country, state, city):
    my_values = CityTable.objects.filter(Name=city.title())
    my_values2 = StateTable.objects.filter(Name=state.title())
    my_values3 = CountryTable.objects.filter(Name=country.title())
    dict_list = list(my_values.values())
    if not my_values or not my_values2 or not my_values3:
        return redirect('/')

    my_dict = dict_list[0]

    max_vals = {}

    for entry in my_dict.keys():
        if entry == 'State_rank':
            continue
        max_vals[entry] = CityTable.objects.aggregate(Max(entry))[
            f'{entry}__max']
    mv2 = max_vals.pop('_Without_rent_3p')
    mv1 = max_vals.pop('_Without_rent_1p')
    mv3 = max_vals.pop('_Food_1p')
    mv4 = max_vals.pop('_Food_3p')
    mv6 = max_vals.pop('_Population')
    mv7 = max_vals.pop('_bedroom_apartment_in_city_Center')
    mv8 = max_vals.pop('_Apartment_price_to_Buy_in_city_Center')
    mv9 = max_vals.pop('_Monthly_ticket_local_transport')
    mv10 = max_vals.pop('_Gym_Membership')
    temp = float(mv6.replace('M', '').replace(
        'K', '').replace('k', '').replace('B', '').strip())
    if 'K' in mv6:
        temp *= 1000
    elif 'M' in mv6:
        temp *= 1000000
    elif 'B' in mv6:
        temp *= 10000000

    # print(dict_list[0]['_Without_rent_1p'])
    max_vals['Without_rent_1p'] = mv1
    max_vals['Without_rent_3p'] = mv2
    max_vals['Food_1p'] = mv3
    max_vals['Food_3p'] = mv4
    # max_vals['Life_expectancy'] = mv5
    max_vals['Population'] = temp
    max_vals['bedroom_apartment_in_city_Center'] = mv7
    max_vals['Apartment_price_to_Buy_in_city_Center'] = mv8
    max_vals['Monthly_ticket_local_transport'] = mv9
    max_vals['Gym_Membership'] = mv10

    v1 = my_dict.pop('_Without_rent_1p')
    v2 = my_dict.pop('_Without_rent_3p')
    v3 = my_dict.pop('_Food_1p')
    v4 = my_dict.pop('_Food_3p')
    # v5 = my_dict.pop('_Life_expectancy')
    v6 = my_dict.pop('_Population')
    v7 = my_dict.pop('_bedroom_apartment_in_city_Center')
    v8 = my_dict.pop('_Apartment_price_to_Buy_in_city_Center')
    v9 = my_dict.pop('_Monthly_ticket_local_transport')
    v10 = my_dict.pop('_Gym_Membership')

    # print(dict_list[0]['_Without_rent_1p'])_Gym_Membership
    my_dict['Without_rent_1p'] = v1
    my_dict['Without_rent_3p'] = v2
    my_dict['Food_1p'] = v3
    my_dict['Food_3p'] = v4
    # my_dict['Life_expectancy'] = v5

    temp2 = float(v6.replace('M', '').replace(
        'K', '').replace('k', '').replace('B', '').strip())
    if 'K' in v6:
        temp2 *= 1000
    elif 'M' in v6:
        temp2 *= 1000000
    elif 'B' in v6:
        temp2 *= 10000000
    # print(v9)
    my_dict['Population'] = temp2
    my_dict['population_txt'] = v6
    my_dict['bedroom_apartment_in_city_Center'] = v7
    my_dict['Apartment_price_to_Buy_in_city_Center'] = v8
    my_dict['Monthly_ticket_local_transport'] = v9
    my_dict['Gym_Membership'] = v10

    print("3 url")

    my_values_c = CityTable.objects.filter(state_name=state.title())
    city_dict_list = list(my_values_c.values())
    print(city_dict_list[0])
    city_dict_list = random.sample(
        city_dict_list, min(50, len(city_dict_list)))
    for i in city_dict_list:
        i['Population'] = i.pop('_Population')

    pram1=1
    pram2=True
    tem = list(CityTable.objects.filter(country_name=country.title()).values())
    tem.sort(key=lambda x: x['Total_with_rent_1p'],reverse=True) 
    state_avrage=0
    pram3=1
    cn1=0
    for en in tem:
        state_avrage+=en['Total_with_rent_1p']
        print(en['Total_with_rent_1p'])
        if en['Name']!=city.title() and cn1==0:
            pram3+=1
            print(pram3)
        else:
            cn1=1    
    state_avrage=state_avrage/len(tem)
    if my_dict['Total_with_rent_1p']>state_avrage:
        pram1 = my_dict['Total_with_rent_1p']/state_avrage
        pram2 = True
    else:
        pram1 = state_avrage/my_dict['Total_with_rent_1p']
        pram2 = False   

    my_dict['pram1']=round(pram1, 2)
    my_dict['pram2']=pram2

    
    my_dict['pram3']=pram3

    tem.sort(key=lambda x: x['Quality_of_life'],reverse=True) 
    pram4=0
    for en in tem:
        if en['Name']==city.title():
            break
            
        pram4+=1 
    
    my_dict['pram4']=pram4+1
    # print(pram4)

    pram5 = round(my_dict['Total_with_rent_1p']/my_dict['Monthly_salary_after_tax'],1)
    pram5 = num2words(pram5)
    my_dict['pram5']=pram5    
    my_dict['pram6']=len(tem)    
    author={}
    day = random.randint(1, 31)
    month = random.randint(1, 12)
    year = 2022
    date = f"{day:02d}-{month:02d}-{year}"
    author['date']=date
    return render(request, 'city.html', {'list': my_dict, 'max_vals': max_vals, 'city_dict_list': city_dict_list,'author':author})


# city_cost
def compare(request, arg1, arg2):
    print(arg1, arg2)
    # is_arg_1_city = False
    # is_arg_2_city = False
    my_values1 = CityTable.objects.filter(Name=arg1.title())
    my_values2 = CityTable.objects.filter(Name=arg2.title())

    if not my_values1:
        my_values1 = CountryTable.objects.filter(Name=arg1.title())
    if not my_values1:
        my_values1 = StateTable.objects.filter(Name=arg1.title())

    if not my_values2:
        my_values2 = CountryTable.objects.filter(Name=arg2.title())
    if not my_values2:
        my_values2 = StateTable.objects.filter(Name=arg2.title())

    if my_values1 and my_values2:
        dict_list1 = list(my_values1.values())[0]
        dict_list2 = list(my_values2.values())[0]
    else:
        return redirect('/')

    # dict_list1 = list(my_values1.values())
    max_vals = {}

    # if len(dict_list1)>0:
    #     print(11111)
    #     dict_list1 = dict_list1[0]
    #     is_arg_1_city=True
    # else:
    #     my_values1 = CountryTable.objects.filter(Name=arg1.title())
    #     dict_list1 = list(my_values1.values())
    #     try:
    #         dict_list1 = dict_list1[0]
    #     finally:
    #         return redirect('/')
    print(dict_list1)
    print(dict_list2)
    # itr=dict_list1
    for key in dict_list2.keys():
        if key in dict_list1.keys(): 
            if key == 'Rank':
                    dict_list1.pop('Rank')

            if key == 'GDP_per_capita':
                dict_list1.pop('GDP_per_capita')

            if key == 'Human_freedom_index':
                dict_list1.pop('Human_freedom_index')

            if key == '_Life_expectancy':
                dict_list1.pop('_Life_expectancy')

            if key == 'English_speaking':
                dict_list1.pop('English_speaking')
    for key in dict_list1.keys():
        if key in dict_list2.keys(): 
            if key == 'Rank':
                dict_list2.pop('Rank')

            if key == 'GDP_per_capita':
                dict_list2.pop('GDP_per_capita')

            if key == 'Human_freedom_index':
                dict_list2.pop('Human_freedom_index')

            if key == '_Life_expectancy':
                dict_list2.pop('_Life_expectancy')

            if key == 'English_speaking':
                dict_list2.pop('English_speaking')
    # my_values2 = CityTable.objects.filter(Name=arg2.title())
    # dict_list2 = list(my_values2.values())
    # if len(dict_list2)>0:
    #     try:
    #         dict_list2 = dict_list2[0]
    #     finally:
    #         return redirect('/')
    #     is_arg_2_city=True
    # else:
    #     my_values2 = CountryTable.objects.filter(Name=arg2.title())
    #     dict_list2 = list(my_values2.values())
    #     dict_list2 = dict_list2[0]

    for entry in dict_list1.keys():
        try:
            max_vals[entry] = CityTable.objects.aggregate(Max(entry))[
            f'{entry}__max']
        except:
            continue
        
        # my_dict,max_vals={}
    dict_list1, max_vals = helper3(my_dict=dict_list1, max_vals=max_vals)
    dict_list2 = helper3(my_dict=dict_list2)
    













    
    a=CityTable.objects.filter().values()
    dl = list(a.values(
        'country_flag_url', 'Liveability', 'Name', 'country_name', 'Total_with_rent_1p', '_Population'))
    dl=dl[:100]
    temp_images_dir = os.path.join(settings.BASE_DIR, 'static/media/compare')
    for filename in os.listdir(temp_images_dir):
        file_path = os.path.join(temp_images_dir, filename)
        os.remove(file_path)
    temp=[]
    names=[]
    p=[]
    for i in dl:
        try:
            curln=i['Name'].lower().replace("'","-")
            curl=f"static/media/city/{curln}.jpg"
            temp.append(np.array(Image.open(curl)))
        except:
            continue
        names.append(i['Name'])
        p.append(i['Total_with_rent_1p'])
    if len(temp)%2==0:
        temp.pop()
        names.pop()    
        p.pop()    
    image_array1=temp[:len(temp)//2]    
    image_array2=temp[len(temp)//2:]
    name1=names[:len(temp)//2]
    name2=names[len(temp)//2:]
    p1=p[len(temp)//2:]
    p2=p[:len(temp)//2]
    com_url = []
    for i in range(len(name1)):
        com_url.append([name1[i],name2[i],p1[i],p2[i]])
    print(com_url)

    # print(image_array1,image_array2)   

    # image1 = Image.open("zhengzhou.jpg")
    # image2 = Image.open("zhoukou.jpg")
    # image_array1 = np.array(image1)
    # image_array2 = np.array(image2)

    # mask = np.arange(300) + np.arange(200)[:, np.newaxis] <= (300 // 1.2) - 2
    # mask = mask.astype(bool)

    # # Save the mask matrix using pickle
    # with open('mask.pickle', 'wb') as f:
    #     pickle.dump(mask, f)

    # Load the mask
    with open('mask.pickle', 'rb') as f:
        mask = pickle.load(f)
        print(mask)

    t = time.time()

    num_processes = 3  # Adjust the number of processes as needed
    pool = Pool(num_processes)

    num_iterations = len(name1)
    # indices = range(num_iterations)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(num_iterations):
            
            futures.append(executor.submit(process_image,i, image_array1[i], image_array2[i], mask,temp_images_dir,name1[i],name2[i]))
            
        # Wait for all the threads to complete
        concurrent.futures.wait(futures)
        print("weighting")
    # print(max_vals)
    # print(com_url)
    return render(request, 'compare.html', {'l1': dict_list1, 'l2': dict_list2, 'ml': max_vals,'com_url':com_url })


def submit_form(request):
    if request.method == 'POST':
        if len(request.POST) > 2:
            arg1 = request.POST.get('sel1')
            arg2 = request.POST.get('sel2')
            return redirect(f'/compare/{arg1}/{arg2}')

        input_text = request.POST.get('sel1')
        # print(input_text)
        my_values = CityTable.objects.filter(Name=input_text.title())
        dict_list = list(my_values.values())
        my_statevalues = StateTable.objects.filter(Name=input_text.title())
        dict_list_state = list(my_statevalues.values())
        if len(dict_list) > 0:
            print("1ngdh")
            c_name = dict_list[0]['country_name']
            return redirect(f'/cost/{c_name}/{input_text}')
        elif len(dict_list_state) > 0:
            print("ngdh")
            c_name = dict_list_state[0]['country_name']
            print(c_name)
            return redirect(f'/cost/{c_name}/{input_text}')
        else:
            print("3ngdh")
            return redirect(f'/cost/{input_text}')

        # return render(request, 'compare.html', {'input_text': input_text})
    # else:
        # return render(request, 'index.html')


def helper3(my_dict, max_vals={}):

    if len(max_vals) > 0:
        mv2 = max_vals.pop('_Without_rent_3p')
        mv1 = max_vals.pop('_Without_rent_1p')
        mv3 = max_vals.pop('_Food_1p')
        mv4 = max_vals.pop('_Food_3p')
        # if not is_arg_city:
        #     mv5 = max_vals.pop('_Life_expectancy')
        mv6 = max_vals.pop('_Population')
        mv7 = max_vals.pop('_bedroom_apartment_in_city_Center')
        mv8 = max_vals.pop('_Apartment_price_to_Buy_in_city_Center')
        mv9 = max_vals.pop('_Monthly_ticket_local_transport')
        mv10 = max_vals.pop('_Gym_Membership')
        temp = float(mv6.replace('M', '').replace(
            'K', '').replace('k', '').replace('B', '').strip())
        if 'K' in mv6:
            temp *= 1000
        elif 'M' in mv6:
            temp *= 1000000
        elif 'B' in mv6:
            temp *= 10000000

        # print(dict_list[0]['_Without_rent_1p'])
        max_vals['Without_rent_1p'] = mv1
        max_vals['Without_rent_3p'] = mv2
        max_vals['Food_1p'] = mv3
        max_vals['Food_3p'] = mv4
        # if not is_arg_city:
        #     max_vals['Life_expectancy'] = mv5
        max_vals['Population'] = temp
        max_vals['bedroom_apartment_in_city_Center'] = mv7
        max_vals['Apartment_price_to_Buy_in_city_Center'] = mv8
        max_vals['Monthly_ticket_local_transport'] = mv9
        max_vals['Gym_Membership'] = mv10

    v1 =  my_dict.pop('_Without_rent_1p')
    v2 = my_dict.pop('_Without_rent_3p')
    v3 = my_dict.pop('_Food_1p')
    v4 = my_dict.pop('_Food_3p')
    # if not is_arg_city:
    #     v5 = my_dict.pop('_Life_expectancy')
    v6 = my_dict.pop('_Population')
    v7 = my_dict.pop('_bedroom_apartment_in_city_Center')
    v8 = my_dict.pop('_Apartment_price_to_Buy_in_city_Center')
    v9 = my_dict.pop('_Monthly_ticket_local_transport')
    v10 = my_dict.pop('_Gym_Membership')

    # print(dict_list[0]['_Without_rent_1p'])_Gym_Membership
    my_dict['Without_rent_1p'] = v1
    my_dict['Without_rent_3p'] = v2
    my_dict['Food_1p'] = v3
    my_dict['Food_3p'] = v4
    # if not is_arg_city:
    #     my_dict['Life_expectancy'] = v5

    temp2 = float(v6.replace('M', '').replace(
        'K', '').replace('k', '').replace('B', '').strip())
    if 'K' in v6:
        temp2 *= 1000
    elif 'M' in v6:
        temp2 *= 1000000
    elif 'B' in v6:
        temp2 *= 10000000
    print(temp2)
    my_dict['Population'] = temp2
    my_dict['population_txt'] = v6
    my_dict['bedroom_apartment_in_city_Center'] = v7
    my_dict['Apartment_price_to_Buy_in_city_Center'] = v8
    my_dict['Monthly_ticket_local_transport'] = v9
    my_dict['Gym_Membership'] = v10

    if len(max_vals) > 0:
        return [my_dict, max_vals]
    else:
        return my_dict


def best(request):

    my_values = CountryTable.objects.filter(Q(Quality_of_life__gt=-1)).values(
        'Rank', 'Name', 'country_icon_url', 'Total_with_rent_1p', 'Quality_of_life')
    dict_list = list(my_values.values(
        'Rank', 'Name', 'country_icon_url', 'Total_with_rent_1p', 'Quality_of_life'))
    
    max_vals = {
        'Total_with_rent_1p': CountryTable.objects.aggregate(Max('Total_with_rent_1p'))['Total_with_rent_1p__max'],
        'Quality_of_life': CountryTable.objects.aggregate(Max('Quality_of_life'))['Quality_of_life__max'],
        # Add more columns and their corresponding max calculations as needed
    }
    dict_list.sort(key=lambda x: x['Quality_of_life'], reverse=True)
    zx=1
    for i in dict_list:
        i['no']=zx
        zx+=1
    my_values2 = CityTable.objects.filter(Q(Liveability__gt=0)).values(
        'country_flag_url', 'Liveability', 'Name', 'country_name', 'Total_with_rent_1p', '_Population','state_name')
    dict_list1 = list(my_values2.values(
        'country_flag_url', 'Liveability', 'Name', 'country_name', 'Total_with_rent_1p', '_Population','state_name'))

    dict_list1.sort(key=lambda x: x['Liveability'], reverse=True)
    for i in range(len(dict_list1)):
        dict_list1[i]['num'] = i+1
 #   print(dict_list1)
    max_vals1 = {
        'Total_with_rent_1p': CityTable.objects.aggregate(Max('Total_with_rent_1p'))['Total_with_rent_1p__max'],
        'Liveability': CityTable.objects.aggregate(Max('Liveability'))['Liveability__max'],
        # Add more columns and their corresponding max calculations as needed
    }

    dict_list1 = dict_list1[:min(len(dict_list1), 100)]

    return render(request, 'best.html', {'list': dict_list, 'max_vals': max_vals, 'list1': dict_list1, 'max_vals1': max_vals1})


import numpy as np
import pickle
import time
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont

def process_image(index, image_array1, image_array2, mask,temp_images_dir,name1,name2):
    
    # print(index,image_array1.shape,image_array1.shape)
    # print('hi')
    
    image_array = np.copy(image_array1)
    image_array[mask] = image_array2[mask]

    modified_image = Image.fromarray(image_array)
    # draw = ImageDraw.Draw(modified_image)
    # text = "VS  "
    # font_size = 20
    # font = ImageFont.truetype("arial.ttf", font_size)  # Use Liberation Sans Bold font

    # # Get the bounding box of the text
    # text_bbox = draw.textbbox((0, 0), text, font=font)
    # text_width = text_bbox[2] - text_bbox[0]
    # text_height = text_bbox[3] - text_bbox[1]

    # # Calculate the position to center the text
    # text_x = (300 - text_width) // 2
    # text_y = (200 - text_height) // 2

    # draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)  # Set the text fill color to black

    # modified_image.save(f"modified_image_{index}.jpg")
    # print(modified_image)
    # print('----------------------------------------------------------------------------')
    modified_image.save(os.path.join(temp_images_dir,f"{name1}_{name2}.jpg"))

    # print("done")


from django.conf import settings
import concurrent.futures

def best_country(request, country):

    my_values2_t = CountryTable.objects.filter(Name=country).values(
        'Total_with_rent_1p', '_Population','Human_freedom_index','GDP_per_capita','_Life_expectancy','English_speaking','Monthly_salary_after_tax')
    dict_list1_t = list(my_values2_t.values(
        'Total_with_rent_1p', '_Population','Human_freedom_index','GDP_per_capita','_Life_expectancy','English_speaking','Monthly_salary_after_tax'))
    
    dict_list1_t=dict_list1_t[0]
    max_vals2={}
    for i in dict_list1_t:
        s=f'{i}__max'
        max_vals2[i]=CountryTable.objects.aggregate(Max(i))[s]

    dict_list1_t['Population']=dict_list1_t['_Population']
    dict_list1_t['Life_expectancy']=dict_list1_t['_Life_expectancy']
    del dict_list1_t['_Population']
    del dict_list1_t['_Life_expectancy']


    max_vals2['Population']=max_vals2['_Population']
    max_vals2['Life_expectancy']=max_vals2['_Life_expectancy']
    del max_vals2['_Population']
    del max_vals2['_Life_expectancy']
    


    my_values2 = CityTable.objects.filter(country_name=country, Liveability__gt=0).values(
        'country_flag_url', 'Liveability', 'Name', 'country_name', 'Total_with_rent_1p', '_Population','state_name')
    dict_list1 = list(my_values2.values(
        'country_flag_url', 'Liveability', 'Name', 'country_name', 'Total_with_rent_1p', '_Population','state_name'))

    dict_list1.sort(key=lambda x: x['Liveability'], reverse=True)
    for i in range(len(dict_list1)):
        dict_list1[i]['num'] = i+1
    # print(dict_list1)
    max_vals1 = {
        'Total_with_rent_1p': CityTable.objects.aggregate(Max('Total_with_rent_1p'))['Total_with_rent_1p__max'],
        'Liveability': CityTable.objects.aggregate(Max('Liveability'))['Liveability__max'],
        'Quality_of_life': max(StateTable.objects.aggregate(Max('Quality_of_life'))['Quality_of_life__max'] , CountryTable.objects.aggregate(Max('Quality_of_life'))['Quality_of_life__max']),
        # Add more columns and their corresponding max calculations as needed
    }

    dict_list1 = dict_list1[:min(len(dict_list1), 100)]

    my_values = StateTable.objects.filter(country_name=country).values(
        'Name', 'country_name', 'Total_with_rent_1p', 'Quality_of_life')
    my_values_more = CityTable.objects.filter().values(
        'Name', 'country_name', 'Total_with_rent_1p', 'Quality_of_life')
    dict_list_more = list(my_values_more.values(
        'Name', 'country_name', 'Total_with_rent_1p', 'Quality_of_life'))
    dict_list_more = random.sample(dict_list_more, min(26, len(dict_list_more)))
    dict_list = list(my_values.values(
        'Name', 'country_name', 'Total_with_rent_1p', 'Quality_of_life'))
    
    print(dict_list)
    dict_list.sort(key=lambda x: x['Quality_of_life'], reverse=True)
    dict_list_more.sort(key=lambda x: x['Quality_of_life'], reverse=True)

    for i in range(len(dict_list)):
        dict_list[i]['num'] = i+1
    for i in range(len(dict_list_more)):
        dict_list_more[i]['num'] = i+1    

    # print("--------------------------------------------------")
    # print(settings.STATIC_URL)
    # print("--------------------------------------------------")
    # C:\Users\nikit\projects\project1\static\media\compare
    temp_images_dir = os.path.join(settings.BASE_DIR, 'static/media/compare')
    for filename in os.listdir(temp_images_dir):
        file_path = os.path.join(temp_images_dir, filename)
        os.remove(file_path)
    temp=[]
    names=[]
    p=[]

    for i in dict_list_more:

        random_i = random.sample(dict_list1, min(1, len(dict_list_more)))
        if len(random_i)>0:
            random_i=random_i[0]

        ubc=random_i['Name'].replace("'","-").lower()
        try:
            # print(ubc,'-------------------------------------')
            temp.append(np.array(Image.open(f"static/media/city/{ubc}.jpg")))
        except:
            continue
        names.append(random_i['Name'])
        p.append(random_i['Total_with_rent_1p'])

        
        ubc=i['Name'].replace("'","-").lower()
        print(ubc)
        try:
            # print(ubc,'-------------------------------------')
            temp.append(np.array(Image.open(f"static/media/city/{ubc}.jpg")))
        except:
            continue
        names.append(i['Name'])
        p.append(i['Total_with_rent_1p'])

    if len(temp)%2!=0:
        temp.pop() 
        names.pop()    
        p.pop()    
    image_array1=temp[:len(temp)//2]    
    image_array2=temp[len(temp)//2:]
    name1=names[:len(temp)//2]
    name2=names[len(temp)//2:]
    p1=p[len(temp)//2:]
    p2=p[:len(temp)//2]
    com_url = []
    for i in range(len(name1)):
        com_url.append([name1[i],name2[i],p1[i],p2[i]])

    with open('mask.pickle', 'rb') as f:
        mask = pickle.load(f)
        # print(mask)

    t = time.time()

    num_processes = 3  # Adjust the number of processes as needed
    pool = Pool(num_processes)

    num_iterations = len(name1)
    # indices = range(num_iterations)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(num_iterations):
            
            futures.append(executor.submit(process_image,i, image_array1[i], image_array2[i], mask,temp_images_dir,name1[i],name2[i]))
            
        # Wait for all the threads to complete
        concurrent.futures.wait(futures)
    print("................")
    print(dict_list1_t)
     
    return render(request, 'best_country.html', {'list': dict_list1, 'max_vals1':max_vals1,'list1':dict_list, 'compare_name':com_url, 'dict_list1_t':dict_list1_t, 'max_vals2':max_vals2})



def best_state(request, country ,state):

    my_values2 = CityTable.objects.filter(state_name=state).values(
        'country_flag_url', 'Liveability', 'Name', 'country_name', 'Total_with_rent_1p', '_Population','state_name')
    dict_list1 = list(my_values2.values(
        'country_flag_url', 'Liveability', 'Name', 'country_name', 'Total_with_rent_1p', '_Population','state_name'))

    dict_list1.sort(key=lambda x: x['Liveability'], reverse=True)
    for i in range(len(dict_list1)):
        dict_list1[i]['num'] = i+1
    print(dict_list1)
    max_vals1 = {
        'Total_with_rent_1p': CityTable.objects.aggregate(Max('Total_with_rent_1p'))['Total_with_rent_1p__max'],
        'Liveability': CityTable.objects.aggregate(Max('Liveability'))['Liveability__max'],
        'Quality_of_life': max(StateTable.objects.aggregate(Max('Quality_of_life'))['Quality_of_life__max'] , CountryTable.objects.aggregate(Max('Quality_of_life'))['Quality_of_life__max']),
        # Add more columns and their corresponding max calculations as needed
    }

    dict_list1 = dict_list1[:min(len(dict_list1), 100)]

    my_values = StateTable.objects.filter(country_name=country.title()).values(
        'Name', 'country_name', 'Total_with_rent_1p', 'Quality_of_life')
    dict_list = list(my_values.values(
        'Name', 'country_name', 'Total_with_rent_1p', 'Quality_of_life'))
    
    dict_list.sort(key=lambda x: x['Quality_of_life'], reverse=True)

    for i in range(len(dict_list)):
        dict_list[i]['num'] = i+1 
     
    return render(request, 'best_state.html', {'list': dict_list1, 'max_vals1':max_vals1,'list1':dict_list , 'name':state})

def vs(request,img1,img2):
    
    return HttpResponse('vs img')

def author(request,author_name):
    temp = author_name.replace('-',' ')
    author_ob = Author.objects.filter(name=temp).values(
        'name', 'bio')
    author_dict = list(author_ob.values(
        'name', 'bio'))
    author_dict=author_dict[0]
    author_dict['Name']=author_name
    return render(request, 'author.html', {'author':author_dict})

