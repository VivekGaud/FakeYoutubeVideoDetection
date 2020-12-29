"""youtube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from pages.views import home_view,search_view,video_fake_percent
from YTpage.views import YThome_view,YTsearch_view,YTvideo_fake_percent

urlpatterns = [
    url(r'^home/', home_view, name='home'),
    url(r'^search/', search_view, name='search'),
    url(r'^videoFakePercent/', video_fake_percent, name='video_fake_percent'),


    url(r'^YTsearch/', YTsearch_view, name='YTsearch'),
    url(r'^YThome/', YThome_view, name='YThome'),
    url(r'^YTvideoFakePercent/', YTvideo_fake_percent, name='YTvideo_fake_percent'),


    url(r'^admin/', admin.site.urls),
]
