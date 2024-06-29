"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, register_converter
from books.converters import DateConverter
from books.views import index, book_list, book_list_by_date

register_converter(DateConverter, 'date')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('books/', book_list, name='book_list'),
    path('books/<str:pub_date>/', book_list_by_date, name='book_list_by_date'),
]
