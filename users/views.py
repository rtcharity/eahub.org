from django.urls import reverse_lazy
from django.views import generic

from .forms import ProfileCreationForm

class SignUp(generic.CreateView):
    form_class = ProfileCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'