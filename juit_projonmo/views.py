from django.shortcuts import render

# app_name = 'templates'

def home(request) :
    return render(request,'home.html')