"""ar_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.conf import settings
from accounts.views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    url(r'^login/$', auth_views.LoginView.as_view(), {'next_page': settings.LOGIN_REDIRECT_URL}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^signup/$', signup_view, name='signup'),

    # path('accounts/', include('django.contrib.auth.urls')),
]
