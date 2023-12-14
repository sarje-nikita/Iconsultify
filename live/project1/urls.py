from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse,Http404,HttpRequest
from django.template import loader
from project1.view import SitemapIndexView ,rssSiteView
from web.sitemaps import CountrySitemap, CitySitemap, StateSitemap, BestCountrySitemap, BestCitySitemap, BestStateSitemap
from django.views.generic.base import TemplateView
from django.shortcuts import render


sitemaps = {
    'countries': CountrySitemap,
    'cities': CitySitemap,
    'states': StateSitemap,
    'bestcountries': BestCountrySitemap,
    'bestcities': BestCitySitemap,
    'beststates': BestStateSitemap,
}


def get_context_data(request, **kwargs):
    section = kwargs['section']
    page = kwargs.get('page', 1)
    sitemap_class = sitemaps.get(section)
    if sitemap_class is None:
        raise Http404("No sitemap available for the section '%s'." % section)
    
    sitemap = sitemap_class()
    urls = sitemap.get_urls()
    items_per_page = 200  # Number of URLs per page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_urls = urls[start_index:end_index]
    lst = []
    for i in paginated_urls:
        lst.append(i['location'])
    # print(lst)
    if len(lst)==0 :
        raise Http404("No sitemap available for the section '%s' at this page." % section)
    

    return render(request,'sitemap.xml',{'urls':lst},content_type='application/xml')

from scrape.feeds import CountryFeed, CityFeed, StateFeed, BestCountryFeed, BestCityFeed, BestStateFeed
rss = {
    'countries': CountryFeed,
    'cities': CityFeed,
    'states': StateFeed,
    'bestcountries': BestCountryFeed,
    'bestcities': BestCityFeed,
    'beststates': BestStateFeed,
}

def ass(request, section, page):
    feed = rss[section](page)

    
    return HttpResponse(feed(request), content_type='application/rss+xml')



urlpatterns = [
    path('', include('web.urls')),
    path('sitemaps/', SitemapIndexView.as_view(), name='sitemap_index'),
    path('sitemaps/<str:section>/<int:page>.xml', get_context_data, name='sitemap_page'),
    path('scrape/', include('scrape.urls')),
    path('cost/', include('web.urls')),
    path('best/', include('web.urls')),
    path('vs-img/', include('web.urls')),
    path('compare/', include('web.urls')),
    path('admin/', admin.site.urls),
    path('submit-form/', include('web.urls')),
    path('author/', include('web.urls')),
    # path('feeds/', rssSiteView.as_view(), name='rss_feeds'),
    # path('feeds/<str:section>/<int:page>',ass,name='country_feed'),

]
