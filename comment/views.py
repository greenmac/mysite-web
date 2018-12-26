from django.shortcuts import render, redirect # redirect重新定向
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse # 返回
from .models import Comment

def updateComment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home')) # 回到登入的那頁

    # 數據檢查
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message':'用戶未登入', 'redirect_to':referer})
    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request, 'error.html', {'message':'評論內容為空白', 'redirect_to':referer})

    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message':'評論對象不存在', 'redirect_to':referer})

    # 檢查通過, 保存數據
    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)