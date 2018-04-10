from django.shortcuts import render
from django.http import JsonResponse
from .functions import place_search


def map(request):
    if request.GET.get('place'):
        return place_search(request.GET.get('place'))
    return render(request, 'map/map.html')


def return_coord(request, mapx, mapy):
    return JsonResponse({'success': True, 'mapx': mapx, 'mapy': mapy})

