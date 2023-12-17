from .models import Business
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.core.paginator import Paginator


class BusnessFeed(Feed):
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
        return Business.objects.all()[x:y]
    
    def item_title(self, item):
        return f'{item.name}'
    
    def item_description(self, item):
        return f'{item.name} is a {item.sub_business} in {item.city}'
        # return self.page
    
    def item_link(self, item):
        return f"/cost/{item.name}"
    
