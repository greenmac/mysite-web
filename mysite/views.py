import datetime
from django.shortcuts import render, redirect # redirect重新定向
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse # 返回
from read_statistics.utils import getSevenDaysReadDate, getTodayHotDate, getYesterdayHotDate
from blog.models import Blog
from .forms import LoginForm, RegForm

def getSevendayHotDate():
    today = timezone.now().date()
    date = today-datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = getSevenDaysReadDate(blog_content_type)

    # 獲取7天熱門文章的緩存數據
    seven_days_hot_date = cache.get('seven_days_hot_date')
    if seven_days_hot_date is None:
        seven_days_hot_date = getSevendayHotDate()
        cache.set('seven_days_hot_date', seven_days_hot_date, 3600)
        print('calc')
    else:
        print('use caches')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_date'] = getTodayHotDate(blog_content_type)
    context['yesterday_hot_date'] = getYesterdayHotDate(blog_content_type)
    context['seven_days_hot_date'] = seven_days_hot_date
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from'), reverse('home'))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 創建帳號
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登入帳號
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from'), reverse('home'))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
