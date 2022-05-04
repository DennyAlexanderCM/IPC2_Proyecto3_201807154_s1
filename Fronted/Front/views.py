from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'index.html', )

def receptFile(request):
    if request.method == 'POST':
        file = request.Files["uploadedFile"]
        print(type(file))

        return render(request, 'index.html', )