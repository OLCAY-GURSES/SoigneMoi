from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from book.models import Hospital


# Create your views here.

@csrf_exempt
def home(request):
    hospitals = Hospital.objects.all()
    context = {'hospitals': hospitals}
    return render(request, 'book/home.html', context)