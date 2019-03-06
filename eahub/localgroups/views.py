from django import urls
from django.contrib.auth import mixins as auth_mixins
from django.views.generic import detail as detail_views
from django.views.generic import edit as edit_views
from rules.contrib import views as rules_views
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from .forms import LocalGroupForm
from .models import LocalGroup


class LocalGroupCreateView(auth_mixins.LoginRequiredMixin, edit_views.CreateView):
    model = LocalGroup
    form_class = LocalGroupForm
    template_name = "eahub/edit_group.html"

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        if hasattr(user, "profile"):
            initial["organisers"] = [user]
        return initial

    def form_valid(self, form):
        form.instance.geocode()
        return super().form_valid(form)


class LocalGroupDetailView(detail_views.DetailView):
    model = LocalGroup
    template_name = "eahub/group.html"
    context_object_name = "group"


class LocalGroupUpdateView(rules_views.PermissionRequiredMixin, edit_views.UpdateView):
    model = LocalGroup
    form_class = LocalGroupForm
    template_name = "eahub/edit_group.html"
    permission_required = 'localgroups.change_local_group'

    def form_valid(self, form):
        if "city_or_town" in form.changed_data or "country" in form.changed_data:
            form.instance.geocode()
        return super().form_valid(form)


class LocalGroupDeleteView(rules_views.PermissionRequiredMixin, edit_views.DeleteView):
    model = LocalGroup
    template_name = "eahub/delete_group.html"
    success_url = urls.reverse_lazy('groups')
    permission_required = 'localgroups.delete_local_group'


@login_required
@require_POST
def claim_group(request, slug):
    group = get_object_or_404(LocalGroup, slug=slug)
    subject = "EA Group claimed: {0}".format(group.name)
    try:
        user_eahub_url = "https://{0}/profile/{1}".format(get_current_site(request).domain,request.user.profile.slug)
    except Profile.DoesNotExist:
        user_eahub_url = "about:blank"
    message = render_to_string('emails/claim_group.html', {
        'user_eahub_url': user_eahub_url,
        'user_name': request.user.profile.name,
        'group_name': group.name,
        'group_url': "https://{0}/group/{1}".format(get_current_site(request).domain,group.slug),
        'user_email': request.user.email
    })
    mail_managers(subject, message)
    messages.success(
        request,
        ''' Thank you, we have received your request to claim this group. Our admin team will send you an email once they have checked your request. ''',
    )
    return redirect('/group/{}'.format(group.slug))


@login_required
@require_POST
def report_group_inactive(request, slug):
    group = get_object_or_404(LocalGroup, slug=slug)
    subject = "EA Group reported as inactive: {0}".format(group.name)
    try:
        user_eahub_url = "https://{0}/profile/{1}".format(get_current_site(request).domain,request.user.profile.slug)
    except Profile.DoesNotExist:
        user_eahub_url = "about:blank"
    message = render_to_string('emails/report_group_inactive.html', {
        'user_eahub_url': user_eahub_url,
        'user_name': request.user.profile.name,
        'group_name': group.name,
        'group_url': "https://{0}/group/{1}".format(get_current_site(request).domain,group.slug),
        'user_email': request.user.email
    })
    mail_managers(subject, message)
    messages.success(
        request,
        ''' Thank you, we have received your report. Our admin team will send you an email once they have looked into it. ''',
    )
    return redirect('/group/{}'.format(group.slug))
