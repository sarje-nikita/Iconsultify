import json
dictionary={}
cnt = 0

import requests
from bs4 import BeautifulSoup

url = "https://datagemba.com/b/c/us/arvada"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    main_titles = soup.find_all("div", attrs={"class": "sec-head-row text-center"})
    main_business = soup.find_all("div", attrs={"class": "description"})

    for i in range(len(main_business)):
        key = main_titles[i].find("h1").text
        # print(key)
        b_ls = main_business[i].find_all('a')
        val = []
        for i in b_ls:
            # print(i)
            cnt += 1

            val.append(i.text)

        dictionary[key]=val

else:
    print("Failed to retrieve the webpage")


json_data = json.dumps(dictionary)

with open('main_business_list.json', 'w') as json_file:
    json_file.write(json_data)

# print(json_data)



dictionary2={}
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    ul = soup.find_all("ul")[2]
    strongs = ul.find_all("strong")
    ols = ul.find_all("ol")
    # print(ols[2])
    # print(strongs[3])
    for i in range(len(strongs)):
        j=i
        key2 = strongs[i].text
        # print(key)
        if i >=3 :
            j=j-1
        o_ls = ols[j].find_all('li')
        val2 = []
        if len(o_ls)==0:
            cnt += 1
        for i in o_ls:
            cnt+=1
            val2.append(i.text.split('.')[1])

        dictionary2[key2] = val2





json_data = json.dumps(dictionary2)
# print(dictionary2)

with open('other_business_list.json', 'w') as json_file:
    json_file.write(json_data)
print(cnt)
