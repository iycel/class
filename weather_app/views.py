from django.http import response
from django.shortcuts import render
import requests
from decouple import config

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    # url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format('a', 'b')  bu şekilde de tanımlanabilir
    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config('API_KEY')}"
    # response = requests.get(url) bu şekilde de olabilir
    city = 'istanbul'
    response = requests.get(url.format(city, config('API_KEY')))
    return render(request, 'weather_app/index.html')
    