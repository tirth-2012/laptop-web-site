from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [
    path('', views.index,name='index'),
    path('index/', views.index,name='index'),
    path('register', views.register,name='register'),
    path('login', views.login_user,name='login'),
    path('logout', views.logout_user,name='logout'),
    path('viewproduct/<int:pk>', views.viewproduct,name='viewproduct'),
    path('productcategory/<int:pk>', views.productcategory,name='productcategory'),
    path('addtocart/<int:pk>',views.addtocart,name='addtocart'),
    path('removefromcart/<int:pk>',views.removefromcart,name='removefromcart'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('checkout',views.checkout,name='checkout'),
    path('update-cart/<int:pk>/<str:action>/', views.update_cart, name='update_cart'),
    path("pay/", views.paymentrazor, name="payment"),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('success', views.success, name='success'),
    path('orderlist', views.orderlist, name='orderlist'),
    path('suborderdetail/<int:pk>', views.suborderdetail, name='suborderdetail'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)