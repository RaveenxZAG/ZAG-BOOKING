from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('findflight', views.findflight, name="findflight"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),    
    path('signout', views.signout, name="signout"),

]
