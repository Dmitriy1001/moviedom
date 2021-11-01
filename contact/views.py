from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

from .forms import ContactForm
from .models import Contact


class ContactView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/#contact-form'
    success_message = "подписка оформлена"


