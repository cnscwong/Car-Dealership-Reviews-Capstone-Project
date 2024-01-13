from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealers_by_state, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')

def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print(f"user: {user}")
            print(f"request: {request}")
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        context['message'] = "Error: Please try again"
        return render(request, 'djangoapp/user_login.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://cncw18-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_from_cf(url)
        context["dealers"] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealerships_by_state(request, state):
    context = {}
    if request.method == "GET":
        url = "https://cncw18-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_by_state(url, state)
        context["dealers"] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = f"https://cncw18-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id={dealer_id}"
        reviews = get_dealer_reviews_from_cf(url)
        context["dealer_id"] = dealer_id
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            context = {}
            context["dealer_id"] = dealer_id
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == "POST":
            url = "https://cncw18-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
            review = {
                "id": 1114,
                "name": "Upkar Lidder",
                "dealership": dealer_id,
                "review": "Great service!",
                "purchase": False,
                "another": "field",
                "purchase_date": "02/16/2021",
                "car_make": "Audi",
                "car_model": "Car",
                "car_year": 2021
            }
            json_payload = {}
            json_payload["review"] = review 
            res = post_request(url, json_payload, dealerId=dealer_id)
            return HttpResponse(res["message"])
    else:
        context = {}
        context['message'] = "You must be logged in to post a review"
        return render(request, 'djangoapp/user_login.html', context)
