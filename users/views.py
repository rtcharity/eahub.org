from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from .models import Profile
from .forms import ProfileCreationForm

class SignUp(generic.CreateView):
    template_name = 'registration/signup.html'    
    form_class = ProfileCreationForm
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid

@login_required(login_url=reverse_lazy('login'))
def ProfileView(request):
    return render(request, 'eahub/profile.html', {
        'user': request.user
    })