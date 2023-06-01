from django.shortcuts import render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Flight, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages


def home(request):
    # if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    # else:
    #     return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findflight(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        destination_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        tclass_r = request.POST.get('tclass')
        flight_list = Flight.objects.filter(source=source_r, destination=destination_r, date=date_r, tclass=tclass_r)
        if flight_list:
            return render(request, 'myapp/list.html', locals())
        else:
            context["error"] = "Sorry no flightes availiable"
            return render(request, 'myapp/findflight.html', context)
    else:
        return render(request, 'myapp/findflight.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('flight_id')
        seats_r = int(request.POST.get('no_seats'))
        flight = Flight.objects.get(id=id_r)
        if flight:
            if flight.atickets > int(seats_r):
                name_r = flight.flight_name
                cost = int(seats_r) * flight.price
                source_r = flight.source
                destination_r = flight.destination                
                tclass_r = flight.tclass
                price_r = flight.price
                date_r = flight.date
                time_r = flight.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                atickets_r = flight.atickets - seats_r
                Flight.objects.filter(id=id_r).update(atickets=atickets_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, flight_name=name_r, source=source_r,
                                           flightid=id_r, destination=destination_r, price=price_r, tickets=seats_r, date=date_r, 
                                           time=time_r,status='BOOKED', tclass=tclass_r)
                        
                return render(request, 'myapp/bookings.html', locals())
            else:
                messages.error(request, 'We apologize for the inconvenience, but we do not have enough seats available for this flight at the moment. Please click OK and then use the browser back button to return to the previous list of flights. You can either choose a different flight or book the same flight with a lower number of seats. Thank you for your understanding!')
                
                # context["error"] = "Sorry select fewer number of seats"
                return render(request, 'myapp/findflight.html', context)
        # else:
        #     return render(request, 'myapp/findflight.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('booking_id')

        try:
            book = Book.objects.get(id=id_r)
            flight = Flight.objects.get(id=book.flightid)
            atickets_r = flight.atickets + book.tickets
            Flight.objects.filter(id=book.flightid).update(atickets=atickets_r)
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(tickets=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
          pass
        return render(request, 'myapp/findflight.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no flightes booked"
        return render(request, 'myapp/findflight.html', context)

def signup(request):
    context = {}
    if request.method == 'POST':
        # Get the form data
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        
        # Check if user already exists
        try:
            user = User.objects.create_user(name_r, email_r, password_r,)
        except IntegrityError:
            context["error"] = "User already exists"
            return render(request, 'myapp/signup.html', context)
        
        # If user is created successfully, redirect to login page
        if user is not None:
            messages.success(request, 'Congratulations, your account has been created successfully! Please sign in to access your account.')
            return render(request, 'myapp/signin.html')
    
    return render(request, 'myapp/signup.html',context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/home.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/home.html', context)
