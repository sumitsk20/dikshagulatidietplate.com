from django.shortcuts import render, get_list_or_404, get_object_or_404
import settings
# Create your views here.
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context

from services.models import Service
from .forms import ContactForm
from services.forms import AppointmentForm
from django.template.loader import get_template
from blog.models import Post
import json
from django.core.mail import send_mail
from django.views.decorators.vary import vary_on_headers


def index(request):
    return render(request, "layout/index.html")


def about(request):
    return render(request, "layout/about.html")


def contact(request):
    form_class = ContactForm(auto_id=False)
    # new logic!
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            contact_subject = form.cleaned_data['contact_subject']
            form_content = form.cleaned_data['content']

            # Email the profile with the
            # contact information
            template = get_template('contact/contact_us.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'contact_subject': contact_subject,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                subject="[DietPlate] New Contact Form submission",
                body=content,
                from_email="DietPlate <info@dikshagulatidietplate.com>",
                to=['dietplate.dp@gmail.com'],  # main id of dietplate
                bcc=['diksha.gulati1310@gmail.com'],  # bcc gmail id of dietplate
            )
            res = email.send(fail_silently=False)
            if res:
                template = get_template('contact/contact_reply.html')
                trending_post = Post.objects.active().order_by('-published_on')[:3]
                ctx = Context({
                    'contact_name': contact_name,
                    'trending_post': trending_post,
                })
                content_reply = template.render(ctx)
                email_reply = EmailMessage(
                    subject="[DietPlate] Message",
                    body=content_reply,
                    from_email="DietPlate <info@dikshagulatidietplate.com>",
                    to=[contact_email],  # reply to user
                )
                email_reply.content_subtype = "html"
                email_reply.send(fail_silently=False)
            return redirect(reverse('contact_success'))

    return render(request, 'contact/contact_us.html', {'form': form_class, 'title': "Contact"})


def contact_success(request):
    trending_post = Post.objects.active().order_by('-published_on')[:3]
    context = Context({
        'trending_post': trending_post,
        'title': "Successfuly sent"
    })

    return render(request, "contact/contact_us_success.html", context)


@vary_on_headers('X-Requested-With')
def book_appointment(request):
    if request.is_ajax() and request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            service=Service.objects.filter(id=request.POST.get("service", "")).values_list('name', flat=True)[0]
            template = get_template('services/appoint_success_response_email.html')
            context = Context({
                'name': request.POST.get("name", ""),
                'mobile': request.POST.get("number", ""),
                'email': request.POST.get("email", ""),
                'category': service,
                'message': request.POST.get("message", ""),
            })
            content = template.render(context)
            email = EmailMessage(
                subject="[DietPlate] New Appointment",
                body=content,
                from_email="DietPlate <info@dikshagulatidietplate.com>",
                # to=['sumitsk20@gmail.com'],  # main id of dietplate
                to=['dietplate.dp@gmail.com'],  # main id of dietplate
                bcc=['diksha.gulati1310@gmail.com'],  # bcc gmail id of dietplate
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)

            data = {'message': "Your appointment request has been saved, someone from DietPlate will contact you soon.",
                    "status": "success"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            errors = {field: error for field, error in form.errors.items()}
            data = {'message': "Oops! There is some problem with your form submission. Please try again.",
                    'errors': errors,
                    "status": "failure"}
            print data
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        raise Http404
