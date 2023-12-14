from django.shortcuts import render
from django.views import View

class SitemapIndexView(View):
    def get(self, request):
        sitemap_urls = []
        
        for i in range(1,2):
            sitemap_urls.append(f'/sitemaps/countries/{i}.xml')

        for i in range(1,28):
            sitemap_urls.append(f'/sitemaps/cities/{i}.xml')

        for i in range(1,2):
            sitemap_urls.append(f'/sitemaps/states/{i}.xml')

        for i in range(1,2):
            sitemap_urls.append(f'/sitemaps/bestcountries/{i}.xml')

        for i in range(1,28):
            sitemap_urls.append(f'/sitemaps/bestcities/{i}.xml')

        for i in range(1,2):
            sitemap_urls.append(f'/sitemaps/beststates/{i}.xml')
                               
        context = {
            'sitemap_urls': sitemap_urls,
        }
        return render(request, 'sitemap_index.html', context)


class rssSiteView(View):
    def get(self, request):
        feed_urls = []
        
        for i in range(1,2):
            feed_urls.append(f'/feeds/countries/{i}')

        for i in range(1,28):
            feed_urls.append(f'/feeds/cities/{i}')

        for i in range(1,2):
            feed_urls.append(f'/feeds/states/{i}')

        for i in range(1,2):
            feed_urls.append(f'/feeds/bestcountries/{i}')

        for i in range(1,28):
            feed_urls.append(f'/feeds/bestcities/{i}')

        for i in range(1,2):
            feed_urls.append(f'/feeds/beststates/{i}')
                               
        context = {
            'feed_urls': feed_urls,
        }
        return render(request, 'rss_site.html', context)
