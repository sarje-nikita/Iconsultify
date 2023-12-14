import requests
from bs4 import BeautifulSoup 
import os


def store_city_image(city_img_url,name):

    r = requests.get(city_img_url)

    print(os.getcwd())
    with open(f'/static/media/flag_gif/{name}.gif', 'wb') as f:
            f.write(r.content)



url = 'https://www.allwavingflags.com/'
HEADERS =({'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' , 'Accept-Languge':'en-US, en;q=0.5'}) 
response = requests.get(url,headers=HEADERS)
soup = BeautifulSoup(response.content, 'html.parser')
src = soup.findAll('ul', {'class': 'flag-list'})
lis=[]
# print(src)
for i in src:
  for j in i:
    lis.append(j)
names=[]
urls=[]
for i in lis:
  # p="https://flagpedia.net"+i.find('img').get('src')
  # p=p.replace('h80','w580')
  if type(i.find('a'))!= type(10):
    names.append(i.find('a').text.strip().replace(' ','-'))
    urls.append(i.find('a').get('href'))
  # name= i.find('span').text
  # name=name.replace(' ','-')
  # store_city_image(p,name)


for i in range(len(names)):
  response = requests.get(urls[i],headers=HEADERS)
  imglink = BeautifulSoup(response.content, 'html.parser').find('div',{'class':'separator vertical-pole'}).find('img').get('src')
  store_city_image(imglink,names[i])
# print(names)  
# print(urls)  

