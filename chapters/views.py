from django.shortcuts import render, get_object_or_404
from .models import Chapter
from executives.models import Executive

# Create your views here.

def chapter_list(request):
    chapters = Chapter.objects.all()
    return render(request, 'chapters/chapter_list.html', {'chapters': chapters})

def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    executives = Executive.objects.filter(level='chapter', chapter=chapter)
    for exco in executives:
        if exco.photo:
            exco.photo_name = exco.photo.name.split('/')[-1]
        else:
            exco.photo_name = ''
    return render(request, 'chapters/chapter_detail.html', {'chapter': chapter, 'executives': executives})
