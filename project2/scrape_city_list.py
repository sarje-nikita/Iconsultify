import json
dictionary={}
cnt = 0

import requests
from bs4 import BeautifulSoup
print('hi')

url = "https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068"

response = requests.get(url)
print('hi')


if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)
    sections = soup.find_all("section")[1:]
    # print(section[-1])
    for section in sections:
        key = section.find("h2").text
        val = []
        lis = section.find_all("li")
        for li in lis:
            cnt+=1
            val.append(li.text)
            print(cnt)

        dictionary[key]=val

else:
    print("Failed to retrieve the webpage")


json_data = json.dumps(dictionary)

with open('city_list.json', 'w') as json_file:
    json_file.write(json_data)

print(cnt)
