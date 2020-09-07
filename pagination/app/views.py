import csv

from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as file:
        reader = csv.DictReader(file)
        pt_stop_list = list(reader)
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
        else:
            page = 1
        p = Paginator(pt_stop_list, 5)
        try:
            pt_stops = p.page(page)
        except EmptyPage:
            pt_stops = p.page(p.num_pages)

        current_page = pt_stops.number

        if current_page == 1:
            prev_page_url = None
        else:
            prev_page_url = f'?page={pt_stops.previous_page_number()}'

        next_page_url = f'?page={pt_stops.next_page_number()}'

        return render_to_response('index.html', context={
            'bus_stations': pt_stops,
            'current_page': current_page,
            'prev_page_url': prev_page_url,
            'next_page_url': next_page_url,
        })


