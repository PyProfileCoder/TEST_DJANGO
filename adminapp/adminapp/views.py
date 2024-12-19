from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Display a list of polls
def index(request):
    return HttpResponse("Welcome to django app")
