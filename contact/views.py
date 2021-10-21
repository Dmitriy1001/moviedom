from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm


class ContactView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/#contact-form'
    success_message = "подписка оформлена"


