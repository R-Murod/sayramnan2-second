"""sayramnan2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from os import path

from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path
from django.urls import re_path as url
from django.views.static import serve
from main.views import *

from sayramnan2 import settings

urlpatterns = [
    path('', indexHandler),
    path('get-item/', get_item),
    path('catalog/', catalogHandler),
    path('all/catalog/', allCatalogHandler),
    path('cart/', cartHandler),
    path('checkout/', checkoutHandler),
    path('orders/', ordersHandler),
    path('wishlist/', wishHandler),
    path('compare/', compareHandler),
    path('search/', searchHandler),
    path('orders/<int:order_id>/', ordersItemHandler),
    path('checkout/success/', checkoutSuccessHandler),
    path('catalog/<int:catalog_id>/', catalogItemHandler),
    path('product/<int:product_id>/', productHandler),
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        })
]