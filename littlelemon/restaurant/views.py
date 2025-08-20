from django.shortcuts import render
from .models import MenuItem, Booking
from .serializers import MenuItemSerializer, BookingSerializer
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework import generics,mixins
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views,login, authenticate
from django.shortcuts import render, redirect

# Create your views here.

# static page
def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html')

def login_view(request):
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
                print("request.POST.get('next')",request.POST)
                return redirect('/restaurant/')  # Redirect to a success page
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
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


    
class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            # admin could get all the bookings
            return Booking.objects.all()
        else:
            # customer can only get all the bookings that booking name is the customer's username
            return Booking.objects.filter(name=self.request.user.username)

    def get_permissions(self):
        return [IsAuthenticated()]
    
class SingleBookingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # only admin could check/delete single bookings
    
    def get_permissions(self):
        return [IsAdminUser()]