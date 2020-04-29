from django.shortcuts import render
from .forms import ContactForm
from django.http import JsonResponse,HttpResponse
from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('content')
        send_mail(name,msg,email,['rolinstores@gmail.com'],fail_silently=False)
        if request.is_ajax():
            return JsonResponse({"message":"Thank You for your submission."})
    if form.errors:
        errors = form.errors.as_json()
        if request.is_ajax():
            print(errors)
            return HttpResponse(errors,status=400,content_type='application/json')
    return render(request,'contact_us/view.html', {'form':form})


    
