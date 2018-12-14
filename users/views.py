from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

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
    return JsonResponse({
        'user_id':request.user.id,
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'email':request.user.email
    })