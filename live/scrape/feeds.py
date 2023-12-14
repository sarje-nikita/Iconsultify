from .models import CountryTable, StateTable, CityTable
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.core.paginator import Paginator


class CountryFeed(Feed):
    # pass
    def __init__(self,page) -> None:
        super().__init__()
        self.page = page

    title = "Latest blog"
    link = "/feeds/"
    description = "Latest blog posts"
    protocol='https'

    def items(self):
        x=(self.page-1)*200
        y= x+201
        return CountryTable.objects.all()[x:y]
    
    def item_title(self, item):
        return f'cost of living in {item.Name}'
    
    def item_description(self, item):
        return f'Total cost of living with rent for one person in {item.Name} is {item.Total_with_rent_1p}'
        # return self.page
    
    def item_link(self, item):
        return f"/cost/{item.Name}"
    

# CountryFeed, CityFeed, StateFeed, BestCountryFeed, BestCityFeed, BestStateFeed


class CityFeed(Feed):
    def __init__(self,page) -> None:
        super().__init__()
        self.page = page

    title = "Latest blog"
    link = "/feeds/"
    description = "Latest blog posts"
    protocol='https'

    def items(self):
        x=(self.page-1)*200
        y= x+201
        return CityTable.objects.all()[x:y]
    
    def item_title(self, item):
        return f'cost of living in {item.Name}'
    
    def item_description(self, item):
        return f'Total cost of living with rent for one person in {item.Name} is {item.Total_with_rent_1p}'
    
    def item_link(self, obj):
        if obj.state_name == '-':
            return f"/cost/{obj.country_name}/{obj.Name}"
        else:
            return f"/cost/{obj.country_name}/{obj.state_name}/{obj.Name}"




class StateFeed(Feed):
    def __init__(self,page) -> None:
        super().__init__()
        self.page = page

    title = "Latest blog"
    link = "/feeds/"
    description = "Latest blog posts"
    protocol='https'

    def items(self):
        x=(self.page-1)*200
        y= x+201
        return StateTable.objects.all()[x:y]
    
    def item_title(self, item):
        return f'cost of living in {item.Name}'
    
    def item_description(self, item):
        return f'Total cost of living with rent for one person in {item.Name} is {item.Total_with_rent_1p}'
    
    
    def location(self, obj):
        return f"/cost/{obj.country_name}/{obj.Name}"


class BestCountryFeed(Feed):
    def __init__(self,page) -> None:
        super().__init__()
        self.page = page

    title = "Latest blog"
    link = "/feeds/"
    description = "Latest blog posts"
    protocol='https'

    def items(self):
        x=(self.page-1)*200
        y= x+201
        return CountryTable.objects.all()[x:y]
    def item_title(self, item):
        return f'cost of living in {item.Name}'
    
    def item_description(self, item):
        return f'Total cost of living with rent for one person in {item.Name} is {item.Total_with_rent_1p}'
    

    def item_link(self, obj):
        return f"/best/{obj.Name}"





class BestCityFeed(Feed):
    def __init__(self,page) -> None:
        super().__init__()
        self.page = page

    title = "Latest blog"
    link = "/feeds/"
    description = "Latest blog posts"
    protocol='https'

    def items(self):
        x=(self.page-1)*200
        y= x+201
        return CityTable.objects.all()[x:y]
    
    def item_title(self, item):
        return f'cost of living in {item.Name}'
    
    def item_description(self, item):
        return f'Total cost of living with rent for one person in {item.Name} is {item.Total_with_rent_1p}'
    
    
    def item_link(self, obj):
        if obj.state_name == '-':
            return f"/best/{obj.country_name}/{obj.Name}"
        else:
            return f"/best/{obj.country_name}/{obj.state_name}/{obj.Name}"




class BestStateFeed(Feed):
    def __init__(self,page) -> None:
        super().__init__()
        self.page = page

    title = "Latest blog"
    link = "/feeds/"
    description = "Latest blog posts"
    protocol='https'
    
    def items(self):
        x=(self.page-1)*200
        y= x+201
        return StateTable.objects.all()[x:y]
    
    def item_title(self, item):
        return f'cost of living in {item.Name}'
    
    def item_description(self, item):
        return f'Total cost of living with rent for one person in {item.Name} is {item.Total_with_rent_1p}'
    
    
    def item_link(self, obj):
        return f"/best/{obj.country_name}/{obj.Name}"
  
