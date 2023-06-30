from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_sign, name='user_sign'),
    path('user_index', views.user_index, name='user_index'),
    path('user_login', views.user_login, name='user_login'),
    path('user_home', views.user_home, name='user_home'),
    path('edit_profile/<id>', views.edit_profile, name='edit_profile'),
    path('logout/<id>', views.logout, name='logout'),
    path('verify_otp', views.otp_log, name='otp_log'),
    path('verify_otp_log', views.otp_verify, name='otp_log_verify'),
    path('login_otp/', views.login_otp, name='login_otp'),
    path('profile/<id>', views.profile, name='profile'),
    path('change_psw/<id>', views.change_psw, name='change_psw'),
    path('detail_view/<id>/<uid>', views.detail_view_user, name='detail_view_user'),
    
    path('cart_view/<id>/<pid>', views.add_cart, name='add_cart'),
    path('cart_user_view', views.cart_view, name='cart_user_view'),
    path('remove_cart/<id>', views.remove_cart, name='remove_cart'),
    path('cart_view', views.cart_view, name='view_cart'),
    path('cart_update', views.cart_update, name='cart_update'),
    path('apply',views.apply_coupon,name='apply'),
    path('payment_conplete',views.payment_complete,name='payment_complete'),
    path('order_view', views.order_view, name='order_view'),
    path('address',views.add_address,name='address'),
    path('view_address',views.view_address,name='view_address'),
    path('address_chose',views.address_chose,name='address_chose'),
    path('order_complete',views.order_complete,name='order_complete'),
    path('view_wish', views.view_wishlist, name='view_wish'),
    path('payment_method_razor/<id>/<add>',views.payment_method_razor,name='payment_method_razor'),
    path('add_wishlist/<pid>/<id>', views.add_wishlist, name='add_wish'),
    
    path('remove_wish/<id>', views.remove_wish, name='remove_wish'),
    
    path('view_order_detail/<id>', views.view_order_detail, name='view_order_detail'),
    path('order_cancel/<id>', views.user_order_cancel, name='order_cancel'),
   
    path('user_product_cancel/<id>', views.user_product_cancel, name='user_product_cancel'),
    path('filter/<id>/<str:name>', views.filter_prod, name='filter'),
    path('filter_product',views.filter_product,name='filter_product'),
    path('sort/<str:name>',views.sort_price,name="sort"),
    path('download/<id>',views.download,name='download'),
    path('user_order_returned/<id>',views.user_order_returned,name='user_order_returned'),
    path('payment_complete_razor/<id>/<add>',views.payment_complete_razor,name='payment_complete_razor'),
    path('address_checkout/<id>', views.address_checkout, name='address_checkout'),
    path('payment/<id>/<amt>/<add>',views.payment_methods, name='payment_methods'),
    path('payment_confirm/<id>/<add>/<amt>',views.payment_confirm,name='payment_confirm'),
    path('filter_price/<id>/<m>',views.filter_price,name='filter_price'),
    


]
# path('add/<id>/<pid>', views.add_qty, name='add_qty'),
#     path('sub/<id>/<pid>', views.sub_qty, name='sub_qty'),
