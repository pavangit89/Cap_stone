from django.shortcuts import render
import re
from .models import MenuItem, Booking
from .serializers import MenuItemSerializer, BookingSerializer
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework import generics,mixins
from rest_framework.exceptions import NotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views,login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from datetime import datetime
import json
from django.http import HttpResponse

# Create your views here.

# static page
def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html')

def login_view(request):
    name=""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                print("token",token.key)               
                return redirect('/restaurant/')  # Redirect to a success page
    else:
        #print("request.POST.get('next')",re.split(r'/', request.GET.get('next')[1:]))
        if request.GET.get('next'):
            name= re.split(r'/', request.GET.get('next'))[-2]        
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form,'name':name})
'''
class CustomLoginView(ObtainAuthToken,views.LoginView):
        def post(self, request, *args, **kwargs):
            print("Login View-->")
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
'''
# api
class MenuItemsView(LoginRequiredMixin,generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu.html' # Specify your HTML template
    

    def get_permissions(self):
        permission_class = [IsAuthenticated]
        if self.request.method != 'GET':
            permission_class.append(IsAdminUser)
        return [permission() for permission in permission_class]
    def get(self, request, *args, **kwargs):
        print("request",request.auth)
        queryset = MenuItem.objects.all()
        #print(queryset)
        #self.object = self.get_object()
        return Response({'menu': queryset})

class SingleMenuItemView(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu_item.html' # Specify your HTML template

    def get_permissions(self):
        permission_class = [IsAuthenticated]
        if self.request.method != 'GET':
            permission_class = [IsAdminUser]
        return [permission() for permission in permission_class]

    def get(self, request, *args, **kwargs):
        custom_id = self.kwargs.get(self.lookup_field)
        #print(custom_id)
        data = MenuItem.objects.get(pk=custom_id)
        #print(data)
        return Response({'menu_item': data})


    
class BookingView(LoginRequiredMixin,generics.ListCreateAPIView):
    print("dateBookingView")
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'book.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            # admin could get all the bookings
            return Booking.objects.all()
        else:
            # customer can only get all the bookings that booking name is the customer's username
                

            return Booking.objects.filter(name=self.request.user.username)

    def get_permissions(self):
        return [IsAuthenticated()]

class BookingDateView(LoginRequiredMixin,generics.ListCreateAPIView):
    #print("dateBookingView")
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    def get_queryset(self):
            print("Booking date else")                
            return Booking.objects.filter(date=self.request.query_params.get('date'))
    def get_permissions(self):
        return [IsAuthenticated()]
    
       
class SingleBookingView(generics.RetrieveUpdateDestroyAPIView):
    print("SingleBookingView")
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    ''' 
       def get(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        filter={}
        print("field ",self.lookup_field)
        obj = get_object_or_404(queryset,self.lookup_field)
        return obj

        def get_object(self):
     print("self.request.query_params.get('custom_id')",self.request.query_params.get('date'))
     custom_date=self.request.query_params.get('date')
     if custom_date:
         obj = get_object_or_404(self.get_queryset(), date=custom_date)
         print("obj",obj)
     else:
         print("obj else",obj)
         obj = super().get_object() 
     return obj
    
    def get(self,lookup_field = ['pk','date']):
            if self.request.GET.get('date'):
                print("date",self.request.GET.get('date'))
                data =Booking.objects.get(date=self.request.GET.get('date'),name=self.request.user.username)
                print("Booking Data", data)
                return Response({'menu_item': data})
            else:
                print("date",self.request.GET.get('pk'))
                data =Booking.objects.filter(pk=id)
                print("Booking Data", data)
                return Response({'menu_item': data})
                 '''
    def get_permissions(self):
        return [IsAdminUser()]

def bookings(request):
    date=request.GET.get('date',datetime.today().date())
    bookings=Booking.objects.all().filter(date=date)
    booking_json=serializers.serialize('json', bookings)
    print("booking_json",booking_json)
    return HttpResponse(booking_json,content_type='application/json')