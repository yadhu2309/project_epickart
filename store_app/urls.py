from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('shop', views.product, name='productall'),
    path('add_cart/<pid>', views.add_cart_guest, name='add_cart_guest'),
    path('gcart_view',views.gcart_view,name='gcart_view'),
    path('gcart_update',views.gcart_update,name='gcart_update'),
    path('gcart_remove/<id>',views.gcart_remove,name='gcart_remove'),
    path('detail_view/<id>', views.detail_view, name='detail_view'),
    path('filter_prod/<id>/<name>',views.filter_prod,name='filter_prod'),
]