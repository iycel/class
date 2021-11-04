from os import name
from django.shortcuts import redirect, render, get_object_or_404
import requests
from decouple import config
from pprint import pprint
from .models import City
from django.contrib import messages

def index(request):
    cities = City.objects.all()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    # url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format('a', 'b')  bu şekilde de tanımlanabilir
    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config('API_KEY')}"
    # response = requests.get(url) bu şekilde de olabilir
    # city = 'istanbul'
    # response = requests.get(url.format(city, config('API_KEY')))
    # content = response.json()
    # pprint(content)
    # pprint(type(content))

    g_city = request.GET.get('name')
    print('g_city : ', g_city)
    if g_city : 
        response = requests.get(url.format(g_city, config('API_KEY')))
        print(response.status_code)
        if response.status_code == 200:
            content = response.json()
            a_city = content['name']
            print(a_city)
            if City.objects.filter(name=a_city):
                messages.warning(request, 'City already exists.')
            else:
                City.objects.create(name=a_city)
                messages.success(request, 'City succesful add')
        else:
            messages.warning(request, 'City does not exists.')
        return redirect('home')
    city_data = []
    for city in cities :
        print(city)
        response = requests.get(url.format(city, config('API_KEY')))
        content = response.json()
        # pprint(content)
        data = {
            'city': city,
            'temp' : content['main']['temp'],
            'desc' : content['weather'][0]['description'],
            'icon' : content['weather'][0]['icon'],
        }
        # pprint(type(content))
        city_data.append(data)
    # print(city_data)
    context = {
        'city_data' : city_data
    }
    return render(request, 'weather_app/index.html', context)

def delete_city(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.warning(request, 'City Deleted')
    return redirect('home')
