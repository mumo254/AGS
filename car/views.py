from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .utils import Calendar
from django.views import generic
from django.utils.safestring import mark_safe
# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):
    posts = Post.objects.all().order_by('-posted_at')
    advice = Advice.objects.all().order_by('-posted_at')
    respos = Response.objects.all().filter().order_by('-posted_at')
    current_user = request.user
    form = ResponseForm()
    try:
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        current_user = request.user
        profile = Profile.objects.get(user=current_user)

    except ObjectDoesNotExist:
        return redirect('update_profile')
    profiles = Profile.objects.filter(user_id=current_user.id).all()
    if request.method == 'POST':
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            com = form.save(commit=False)
            com.user = request.user
            com.save()
            return redirect('index')
    else:
        form = ResponseForm()
    return render(request, 'index.html', {'profiles': profiles, 'posts': posts, 'advice': advice, 'form': form, 'respos': respos, 'current_user': current_user})


@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user
    form = ProfileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            prof = form.save(commit=False)
            prof.user = request.user
            prof.save()
            return redirect('index')
        else:
            form = ProfileForm()
    return render(request, 'update-profile.html', {'form': form})


@login_required(login_url='/accounts/login/')
def profile(request, pk):
    user = User.objects.get(pk=pk)
    profiles = Profile.objects.filter(user=user).all()
    current_user = request.user
    return render(request, 'profile.html', {"current_user": current_user, "user": user, "profiles": profiles})


def about(request):
    user = request.user
    profiles = Profile.objects.filter(user=user).all()
    return render(request, 'about.html', {'profiles': profiles})


def tips(request):
    user = request.user
    profiles = Profile.objects.filter(user=user).all()
    return render(request, 'tips.html', {'profiles': profiles})


@login_required(login_url='/accounts/login/')
def issue(request):
    user = request.user
    profiles = Profile.objects.filter(user=user).all()
    form = PostForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            issu = form.save(commit=False)
            issu.user = request.user
            issu.save()
            return redirect('index')
        else:
            form = PostForm()
    return render(request, 'issue.html', {'form': form, 'profiles': profiles})


@login_required(login_url='/accounts/login/')
def advice(request):
    user = request.user
    profiles = Profile.objects.filter(user=user).all()
    form = AdviceForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            adv = form.save(commit=False)
            adv.user = request.user
            adv.save()
            return redirect('index')
        else:
            form = AdviceForm()
    return render(request, 'advice.html', {'form': form, 'profiles': profiles})


@login_required(login_url='/accounts/login/')
def sale(request):
    user = request.user
    profiles = Profile.objects.filter(user=user).all()
    form = SaleForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            sal = form.save(commit=False)
            sal.user = request.user
            sal.save()
            return redirect('bazaar')
        else:
            form = SaleForm()
    return render(request, 'sale.html', {'form': form, 'profiles': profiles})


@login_required(login_url='/accounts/login/')
def bazaar(request):
    cars = Sale.objects.all().order_by('-posted_at')
    user = request.user
    profiles = Profile.objects.filter(user=user).all()
    return render(request, 'bazaar.html', {'cars': cars, 'profiles': profiles})


@login_required(login_url='/accounts/login/')
def experience(request):
    advices = Advice.objects.all().order_by('-posted_at')
    user = request.user
    profiles = Profile.objects.filter(user=user).all()
    return render(request, 'experiences.html', {'advices': advices, 'profiles': profiles})


@login_required(login_url='/accounts/login/')
def response(request, post_id):
    form = ResponseForm()
    post = Post.objects.filter(pk=post_id).first()
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            respo = form.save(commit=False)
            respo.user = request.user
            respo.post = post
            respo.save()
    return redirect('index')


def events(request, year, month):
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    user = request.user
    profiles = Profile.objects.filter(user=user).all()
    now = datetime.now()
    time = now.strftime('%I:%M %p')
    cal = HTMLCalendar().formatmonth(
        year, month_number
    )
    return render(request, 'events.html', {'year': year, 'month': month, 'month_number': month_number, 'cal': cal, 'profiles': profiles, 'time': time})


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)

        context['calendar'] = mark_safe(html_cal)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    user = request.user
    pk = user.id
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'event.html', {'form': form})


def map(request):
    user = request.user

    locations = Response.objects.filter(user=user).all().order_by('-posted_at')

    return render(request, 'map.html', {'locations': locations})


@login_required(login_url='/accounts/login/')
def mechanical_issue(request):
    posts = Post.objects.all().order_by('-posted_at')
    advice = Advice.objects.all().order_by('-posted_at')
    respos = Response.objects.all().filter().order_by('-posted_at')
    current_user = request.user
    form = ResponseForm()
    try:
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        current_user = request.user
        profile = Profile.objects.get(user=current_user)

    except ObjectDoesNotExist:
        return redirect('update_profile')
    profiles = Profile.objects.filter(user_id=current_user.id).all()
    if request.method == 'POST':
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            com = form.save(commit=False)
            com.user = request.user
            com.save()
            return redirect('index')
    else:
        form = ResponseForm()
    return render(request, 'mechanical.html', {'profiles': profiles, 'posts': posts, 'advice': advice, 'form': form, 'respos': respos, 'current_user': current_user})


@login_required(login_url='/accounts/login/')
def contact(request):

    return render(request, 'contact.html')
