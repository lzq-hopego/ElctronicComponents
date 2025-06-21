"""ElctronicComponents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.contrib import admin
from ElctronicComponent import views as ElctronicComponent_views
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/components/',ElctronicComponent_views.components.as_view()),
    path('api/componentslog/',ElctronicComponent_views.componentslog.as_view()),
    path('api/edit/components/',ElctronicComponent_views.edit_components.as_view()),
    path('api/addnum/components/',ElctronicComponent_views.addnum_components.as_view()),
    path('api/removenum/components/',ElctronicComponent_views.removenum_components.as_view()),
    path('api/delete/components/',ElctronicComponent_views.delete_components.as_view()),
    path('api/records/',ElctronicComponent_views.records.as_view()),
    path('api/search/',ElctronicComponent_views.search_components.as_view()),
    path('api/get_sum_data/',ElctronicComponent_views.get_sum_data.as_view()),
    path('',ElctronicComponent_views.home),
    path('yuanqijianguanli',ElctronicComponent_views.home),
    path('churukujilu',ElctronicComponent_views.home),

]


