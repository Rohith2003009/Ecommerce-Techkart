from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
 

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
 path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
     path('place_order/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),  #
       path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),

]