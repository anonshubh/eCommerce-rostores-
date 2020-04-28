from django.shortcuts import render
from .forms import ContactForm
from django.http import JsonResponse,HttpResponse

def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        if request.is_ajax():
            return JsonResponse({"message":"Thank You for your submission."})
    if form.errors:
        errors = form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors,status=400,content_type='application/json')
    return render(request,'contact_us/view.html', {'form':form})


    
