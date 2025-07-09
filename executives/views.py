from django.shortcuts import render
from .models import Executive

# Create your views here.

def national_executives(request):
    executives = Executive.objects.filter(level='national')
    # Prepare data with image file names for static usage
    for exco in executives:
        if exco.photo:
            exco.photo_name = exco.photo.name.split('/')[-1]
        else:
            exco.photo_name = ''
    return render(request, 'executives/national_executives.html', {'executives': executives})
