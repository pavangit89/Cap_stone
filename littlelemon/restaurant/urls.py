from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # static page
    path('', views.index, name='index'),   
    path('about', views.about, name='about'),   
    #path('login/', views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'), # Redirects to home after logout
    

        
    # api

    # show menuitems
    path('api/menu/', views.MenuItemsView.as_view(),name='menu'),
    path('api/menu/<int:pk>', views.SingleMenuItemView.as_view(),name='menu_item'),

    # bookings
    path('api/book/', views.BookingView.as_view()),
    path('api/book/<int:pk>', views.SingleBookingView.as_view()),

    # user managements
    path('auth/', include('djoser.urls')),
    #path('api/', include('djoser.urls.authtoken')),
]