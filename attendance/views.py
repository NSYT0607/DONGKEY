from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.template.loader import render_to_string
from club.models import Club
from .models import Event
from .forms import EventForm, DateInputForm


def event_list(request, pk):
    club = get_object_or_404(Club, pk=pk)
    form = DateInputForm()
    event_list = club.event_set.all()
    ctx = {
            'club': club,
            'dateinput_form': form,
            'event_list': event_list[:15],
    }
    return render(request, 'attendance/event_list.html', ctx)


def non_admin_event_list(request, pk):
    club = get_object_or_404(Club, pk=pk)
    form = DateInputForm()
    event_list = club.event_set.all()
    ctx = {
            'club': club,
            'dateinput_form': form,
            'event_list': event_list[:15],
    }
    return render(request, 'attendance/non_admin_event_list.html', ctx)


def create_event(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == "POST":
        event_form = EventForm(club, request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.club = club
            event.save()
            event_form.save_m2m()
            return redirect(reverse('attendance:read_event', kwargs={'event_pk': event.pk, }))
    else:
        event_form = EventForm(club)
    ctx = {
            'club': club,
            'event_form': event_form,
    }
    return render(request, 'attendance/create_event.html', ctx)


def read_event(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    club = event.club
    ctx = {
            'club': club,
            'event': event,
     }
    return render(request, 'attendance/read_event.html', ctx)


def search_by_date(request, pk):
    club = Club.objects.get(pk=pk)
    form = DateInputForm(request.GET)
    if form.is_valid():
        year = int(form.cleaned_data['year'])
        month = int(form.cleaned_data['month'])
        search_attendance = club.event_set.filter(
            event_at__year="{0}".format(year),
            event_at__month="{0}".format(month))
        ctx = {
            'year': year,
            'month': month,
            'club': club,
            'event_list': search_attendance.order_by('event_at')
        }
        html = render_to_string('attendance/search_by_date.html', ctx)
        return JsonResponse({'success': True, 'html': html})
    else:
        return JsonResponse({'success': False, 'status': 'form_invaild'})