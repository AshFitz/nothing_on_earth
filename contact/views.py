from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .forms import Contact
# Create your views here.

def contact(request):
    admin_email = settings.EMAIL_HOST_USER
    subject = render_to_string('emails/contact_request_subject.txt')
    
    if request.method == 'POST':
        form = Contact(request.POST)

        if form.is_valid():
            reply_email = request.POST.get('email')
            body = render_to_string('emails/contact_request_body.txt')
            subject = render_to_string('emails/contact_request_subject.txt')
            form.save()
            try:
                send_email(
                    subject,
                    body,
                    reply_email
                    [admin_email],
                )
                messages.info(request, 'Your message has been sent succesfully')
            except Exception as e:
                messages.error(request, f'Message not sent, Error {e}')
            return redirect(reverse('contact_success'))
        else:
            messages.error(request, 'Sorry something went wrong, please check all fields are filled out correctly')
    else:
        form = Contact()

    template = 'contact/contact.html'

    context = {
        'form': form,
    }
    return render(request, template, context)


def contact_success(request):
    template = 'contact/contact_success.html'

    return render(request, template)

