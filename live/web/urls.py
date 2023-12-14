from django.urls import path
from . import views
from django.conf.urls import handler404


urlpatterns = [
    path('', views.langingpage , name='langingpage'),
    path('cost/<name>', views.cost , name='cost'),
    path('best/', views.best , name='best'),
    path('best/<country>/', views.best_country , name='best_country'),
    path('best/<country>/<state>/', views.best_state , name='best_state'),
    path('cost/<country_name>/<city_name>', views.city_cost , name='city_cost'),
    path('cost/<country>/<state>/<city>', views.city_with_state_cost , name='city_with_state_cost'),
    path('compare/<arg1>/<arg2>', views.compare , name='compare'),
    path('submit-form/', views.submit_form, name='submit_form'),
    path('vs-img/<img1>/<img2>/', views.vs, name='vs'),
    path('author/<author_name>', views.author, name='author'),

]
handler404 = 'web.views.page_not_found'

