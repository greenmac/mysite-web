"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
###----------
##本機開發設定
# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = get_wsgi_application()


###----------
##heroku設定
import os
 
from django.core.wsgi import get_wsgi_application
from dj_static import Cling
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
 
application = Cling(get_wsgi_application())