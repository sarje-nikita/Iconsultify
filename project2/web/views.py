from django.shortcuts import render, redirect
from model.models import Business, store
from django.db.models import Count
from collections import defaultdict
import hashlib
import math
from django.utils.safestring import mark_safe





main_business = {'Health-': ['Acupuncture', 'Veterinarians', 'Audiology-Clinics', 'Bike-shops', 'Chiropractors', 'Counselling-services', 'Dance-schools', 'Gyms', 'Hypnotherapy', 'Martial-arts-classes', 'Massage-therapy', 'Naturopathy', 'Occupational-therapists', 'Opticians', 'Orthodontists', 'Pharmacies', 'Physiotherapy', 'Psychologists', 'Sleep-clinics', 'Weight-loss-centres', 'Yoga-studios'], 'Doctors-': ['Cardiologists', 'Cosmetic-dentists', 'Dentists', 'Dermatologists', 'Endocrinologists', 'ENT-specialist', 'Gastroenterologists', 'General-practitioners', 'Gynaecologists', 'Homeopaths', 'Neurologists', 'Neurosurgeons', 'Optometrists', 'Orthopedics', 'Paediatric-dentists', 'Pain-management-doctors', 'Paediatricians', 'Plastic-surgeon', 'Podiatrists', 'Psychiatrists', 'Rheumatologists', 'Urologists'], 'Entertainment-': ['Bars', 'Beauty-salons', 'DJs', 'Event-management-company', 'Face-painting', 'Golf-courses', 'Hairdressers', 'Hiking-trails', 'Landmarks', 'Leisure-centres', 'Limo-hire', 'Nail-salons', 'Parks', 'Places-to-visit', 'Public-swimming-pools', 'Shopping-centre', 'Spas', 'Tattoo-shops', 'Theme-parks', 'Wedding-planners'], 'Local-Businesses-': ['Apartments-for-rent', 'Auto-body-shops', 'Car-dealerships', 'Child-care-centres', 'Custom-cabinets', 'Department-stores', 'Dog-grooming', 'Florists', 'Furniture-stores', 'Gift-shops', 'Home-builders', 'Hotels', 'Jewellery', 'Kitchen-supply-stores', 'Locksmiths', 'Mattress-stores', 'Mechanic-shops', 'Nursing-homes', 'Pawn-shops', 'Preschools', 'Septic-tank-services', 'Towing-services', 'Tutors', 'Window-companies'], 'Restaurants-': ['Bakeries', 'BBQ-restaurants', 'Cafe', 'Chinese-restaurants', 'Fish-and-chips', 'Indian-restaurants', 'Italian-restaurants', 'Mexican-restaurants', 'Pizzeria', 'Sandwich-shops', 'Steakhouses', 'Thai-restaurants'], 'Speciality-Food-': ['Australian-restaurants', 'Bagel-shops', 'Cakes', 'Caterers', 'Chocolate-shops', 'Food-trucks', 'French-Restaurants', 'Japanese-restaurants', 'Juice-bars', 'Seafood-restaurants', 'Sushi', 'Vegetarian-restaurants', 'Vietnamese-restaurants'], 'Lawyers-': ['Bankruptcy-lawyers', 'Compensation-lawyers', 'Consumer-protection-lawyers', 'Criminal-lawyers', 'Employment-lawyers', 'Estate-planning-lawyers', 'Family-lawyers', 'Immigration-lawyers', 'Medical-malpractice-lawyers', 'Patent-attorney', 'Traffic-lawyers'], 'Local-Services-': ['Appliance-repair-services', 'Carpet-cleaning-service', 'Cell-phone-repair', 'Churches', 'Computer-repair', 'Courier-services', 'Dry-cleaners', 'Electricians', 'Fencing-contractors', 'Garage-door-repair', 'House-cleaning-services', 'HVAC-services', 'Landscaping-companies', 'Lawn-care-services', 'Marriage-celebrants', 'Removalists', 'Pest-control-companies', 'Pet-sitting', 'Plumbers', 'Roofing-contractors', 'Rubbish-removal', 'Security-systems', 'Self-storage', 'Tree-services', 'Window-cleaners'], 'Professional-Services-': ['Advertising-agencies', 'Animal-removal', 'Architects', 'CPA', 'Driving-schools', 'Financial-services', 'Insurance-brokers', 'Interior-designer', 'Marriage-counselling', 'Migration-agents', 'Mortgage-brokers', 'Painters', 'Photographers', 'Conveyancer', 'Real-estate-agents', 'Tax-services', 'names-of-travel-agencies', 'Videographers', 'Web-designers']}

ls = []
for i in main_business.values():
    for j in i:
        ls.append(j)


def home(request):
 
    result = store.objects.values('state', 'city').annotate(
        city_count=Count('city')).order_by('state')


    state_city_dict = defaultdict(list)
    for item in result:
        state = item['state']
        city = item['city']
        city_count = item['city_count']
        state_city_dict[state].append(city)
    state_city_dict = dict(state_city_dict)


    return render(request, 'home.html', {"cities": state_city_dict})




def city(request, state, city):
    return render(request, 'city.html', {'state': state, "city": city, 'main_business': main_business})


def business(request, state, city, business):
    hash_object = hashlib.sha256(str(state+city+business).encode())
    hashed_value = hash_object.hexdigest()
    business_objects = Business.objects.filter(hash_value=hashed_value)

    business_data = []
    for business_obj in business_objects:
        data = {
            'name': business_obj.name,
            'address': business_obj.address,
            'website': business_obj.website,
            'phone_number': business_obj.phone_number,
            'reviews_count': business_obj.reviews_count,
            'reviews_average': business_obj.reviews_average,
            'state': business_obj.state,
            'city': business_obj.city,
            'main_business': business_obj.main_business,
            'sub_business': business_obj.sub_business,
            'map': mark_safe(business_obj.map.replace('width="600" height="450"', 'height="200px" width="100%"')) if business_obj.map else "",
            # 'map':mark_safe(business_obj.map.replace('width="600" height="450"','height="200px" width="100%"')),
            'hash_value': hashlib.sha256(str(business_obj.hash_value+str(business_obj.id)).encode()).hexdigest(),
            't1':[i for i in range(math.floor(business_obj.reviews_average))],
            't2':[i for i in range(5-math.floor(business_obj.reviews_average))],
        }
        business_data.append(data)
    return render(request, 'business.html', {'state': state, "city": city, "business": business, 'ls': ls,'business_data':business_data})

def detail(request, state, city, business,hash):
   
    hash_object = hashlib.sha256(str(state+city+business).encode())
    hashed_value = hash_object.hexdigest()
    business_objects = Business.objects.filter(hash_value=hashed_value)

    business_data={}
    other_business_data=[]
    for i in business_objects:
        nhash = hashlib.sha256(str(i.hash_value+str(i.id)).encode()).hexdigest()
        if nhash==hash:
            business_data = {
                    'name': i.name,
                    'address': i.address,
                    'website': i.website,
                    'phone_number': i.phone_number,
                    'reviews_count': i.reviews_count,
                    'reviews_average': i.reviews_average,
                    'state': i.state,
                    'city': i.city,
                    'map': mark_safe(i.map.replace('width="600" height="450"', 'height="300px" width="100%"')) if i.map else "",
                    'main_business': i.main_business,
                    'sub_business': i.sub_business,   
                    't1':[j for j in range(math.floor(i.reviews_average))],
                    't2':[j for j in range(5-math.floor(i.reviews_average))],             
                }
        else:
            other_business_data.append([i.name,i.address,nhash])
            
    return render(request, 'details.html', {'state': state, "city": city, "business": business, 'ls': ls,'business_data':business_data, "other_business_data":other_business_data,"hash":hash})

# def homepg(request):
#     data = cities

#     data_list = list(data.items())

#     paginator = Paginator(data_list, 5)

#     page_number = request.GET.get('page')
#     page_data = paginator.get_page(page_number)

#     return render(request, 'home2.html', {'page_data': page_data})



def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def tnc(request):
    return render(request, 'tnc.html')

def policy(request):
    return render(request, 'policy.html')

def disclaimer(request):
    return render(request, 'disclaimer.html')

def page_not_found(request, exception=None):
    return redirect('/')