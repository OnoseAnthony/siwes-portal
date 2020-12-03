from django.views.generic import TemplateView
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from accounts.models import NewzUpdate



def HomePage(request):
    news = NewzUpdate.objects.all()
    args = {'news': news}
    return render(request, 'index.html',args)

class AboutPage(TemplateView):
    template_name = 'about.html'


def ContactPage(request):
    context = {}
    if request.method == 'POST':
        subject = request.POST.get('subject')
        from_email = request.POST.get('email')
        message = request.POST.get('message')
        try:
            send_mail(subject, message, from_email, [settings.EMAIL_HOST_USER], fail_silently=True)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        context['success'] = "Received. we'd get back to you soon !!"
    return render(request, "contact.html", context)
