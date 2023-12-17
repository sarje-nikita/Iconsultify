from django.contrib.sitemaps import Sitemap
from model.models import Business
import hashlib


class CitySitemap(Sitemap):
    protocol = 'https'

    def items(self):
        unique_locations = Business.objects.values('state', 'city').distinct()
        urls = []
        for location in unique_locations:
            state = location['state']
            city = location['city']
            url = f"/us/{state}/{city}"  
            urls.append(url)

        return urls

    def location(self, obj):
        return obj 
   
class BusinessSitemap(Sitemap):
    protocol = 'https'
 
    def items(self):
        unique_locations = Business.objects.values('state', 'city', 'sub_business').distinct()
        urls = []
        for location in unique_locations:
            state = location['state']
            city = location['city']
            sub_business = location['sub_business']
            url = f"/us/{state}/{city}/{sub_business}"  
            urls.append(url)

        return urls

    def location(self, obj):
        return obj 
  
class DetailSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        unique_locations = Business.objects.values('state', 'city', 'sub_business', 'id', 'hash_value').distinct()
        urls = []

        for location in unique_locations:
            state = location['state']
            city = location['city']
            sub_business = location['sub_business']
            hashd = hashlib.sha256(str(location['hash_value']+str(location['id'])).encode()).hexdigest()
            url = f"/us/{state}/{city}/{sub_business}/{hashd}" 
            urls.append(url)

        return urls

    def location(self, obj):
        return obj

