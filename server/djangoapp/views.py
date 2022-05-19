from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel, CarMake
#from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.core import serializers 
import uuid


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        # Obtener nombre y contraseña, y autentificar al usuario
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password) 

        if user is not None:
            # Si es user valido, entonces redireccionar a index
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            # Si es user invalido
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    print("Log out the user `{}`".format(request.user.username))
    # Logout user
    logout(request)
    # Redireccionar user
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # rend 
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Obtener datos de new user
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            # crear user
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://5b32d086.us-south.apigw.appdomain.cloud/api/dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)



def get_dealer_details(request, id):
    if request.method == "GET":
        #obtener obj de dealer
        context = {}
        dealer_url = "https://5b32d086.us-south.apigw.appdomain.cloud/api/dealerships"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
        #obtener obj reviews del dealer
        review_url = "https://5b32d086.us-south.apigw.appdomain.cloud/api/reviews"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)
        
    


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    # If it is a GET request, just render the add_review page
    if request.method == 'GET':
        url = "https://5b32d086.us-south.apigw.appdomain.cloud/api/dealerships"
        # Get dealers from the URL
        dealer = get_dealer_by_id_from_cf(url, id=dealer_id)
        print(dealer.full_name)
        context = {
            "dealer_id": dealer_id,
            "dealer_name": dealer.full_name,
            "cars": CarModel.objects.all()
        }
        #print(context)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = dict()
            review["id"]=0#placeholder
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            print(request.POST["car"])
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("|")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car_parts[0]
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None
            json_result = post_request("https://5b32d086.us-south.apigw.appdomain.cloud/api/reviews", review, dealerId=dealer_id)
            print(json_result)
            if "error" in json_result:
                context["message"] = "ERROR: Review was not submitted."
            else:
                context["message"] = "Review was submited"
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
