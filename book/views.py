from django.contrib.auth import  authenticate,login, logout
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from book.models import Hospital, User


# Create your views here.

@csrf_exempt
def home(request):
    hospitals = Hospital.objects.all()
    context = {'hospitals': hospitals}
    return render(request, 'book/home.html', context)




@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True)
def logoutUser(request):
    logout(request)
    messages.success(request, 'Utilisateur déconnecté')
    return redirect('hospital_home')