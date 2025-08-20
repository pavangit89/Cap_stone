from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework.authtoken import views as v1
urlpatterns = [
    # static page
    path('', views.index, name='index'),   
    path('about', views.about, name='about'),   
    #path('authen/', views.login, name='authen'),
    path('authenticate/', views.login_view, name='authenticate'),
    path('userlogout/', auth_views.LogoutView.as_view(next_page='index'), name='userlogout'), # Redirects to home after logout
    

    #registration/login.html

        
    # api

    # show menuitems
    path('api/menu/', views.MenuItemsView.as_view(),name='menu'),
    path('api/menu/<int:pk>', views.SingleMenuItemView.as_view(),name='menu_item'),

    # bookings
    path('api/book/', views.BookingView.as_view()),
    path('api/book/<int:pk>', views.SingleBookingView.as_view()),

    # user managements
    path('auth/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
    path('api-token-auth/', v1.obtain_auth_token)
]