import csv
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page


def index(request):
    return redirect(reverse('bus_stations'))




def bus_stations(request):
    with open(settings.BUS_STATION_CSV, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        all_stations = [row for row in reader]

    paginator = Paginator(all_stations, 10)

    page_number = request.GET.get('page')
    if page_number == '0':
        bus_stations = paginator.page(1)
    else:
        try:
            bus_stations: Page = paginator.page(page_number)
        except PageNotAnInteger:
            bus_stations = paginator.page(1)
        except EmptyPage:
            bus_stations = paginator.page(paginator.num_pages)

    context = {
        'bus_stations': bus_stations,
        'page': page_number,
    }
    return render(request, 'stations/index.html', context)
