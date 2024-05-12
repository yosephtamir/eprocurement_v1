"""
URL configuration for procurement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
# from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as user_views
from requestion import views as req_views
from proforma import views as pro_views

urlpatterns = [
    path('Home/', pro_views.Home.as_view(), name='Home'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('blog/', pro_views.Home.as_view(), name='blog'),
    path('blog/<int:pk>/', pro_views.BlogDetail.as_view(), name='blogdetails'),
    path('notifications/', pro_views.Notifications_list.as_view(), name='notificationslist'),
    path('requestion/', req_views.RequestionList.as_view(), name='requestionlist'),
    path('requestion/<pk>/', req_views.RequestionDetails.as_view(), name='requestiondetails'),
    path('requestion/<pk>/expired', req_views.ExpiredRequestionDetails.as_view(), name='expiredrequestiondetails'),
    path('requestion/<pk>/fill/', pro_views.ProformaSubmit.as_view(), name='requestionfill'),
    path('business/new', user_views.BusinessRegistration.as_view(), name='newbusiness'),
    path('business/<pk>/', user_views.BusinessDetails.as_view(), name='businessdetails'),
    re_path('none', pro_views.schema_view),
    path('', include("proforma.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)