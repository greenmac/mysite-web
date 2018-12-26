from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Blog, BlogType
from read_statistics.utils import readStatisticsOnceRead
from comment.models import Comment
from .serializers import BlogSerializer
from rest_framework import viewsets

# each_page_blogs_num = 2  # 每2篇進行分頁

# Create your views here.
def getBlogListCommonDate(request, blog_all_list):
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1) # 獲取url的頁面參數(GET請求)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 獲取當前頁碼
    # 獲取前後各兩頁的頁碼
    page_range = list(range(max(current_page_num - 2, 1), min(paginator.num_pages + 1, current_page_num + 3)))
    # 加上省略標記
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首頁和尾頁
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    
    # 獲取日期歸檔對應的文章數量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog')) # annotate(標註文字用)
    context['blog_dates'] = blog_dates_dict
    return context

def blogList(request):
    blog_all_list = Blog.objects.all()
    context = getBlogListCommonDate(request, blog_all_list)
    return render(request, 'blog/blog_list.html', context)

def blogsWithType(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = getBlogListCommonDate(request, blog_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

def blogWithDate(request, year, month):
    blog_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = getBlogListCommonDate(request, blog_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month);
    return render(request, 'blog/blogs_with_date.html', context)

def blogDetail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = readStatisticsOnceRead(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['comments']= comments
    response = render(request, 'blog/blog_detail.html', context) # 響應
    response.set_cookie(read_cookie_key, 'true') # 閱讀cookie標記
    return response


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer