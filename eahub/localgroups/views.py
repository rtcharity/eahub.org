from django import urls
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic import detail as detail_views
from django.views.generic import edit as edit_views
from rules.contrib import views as rules_views

from ..base.views import ReportAbuseView
from ..profiles.models import Profile
from .forms import LocalGroupForm
from .models import LocalGroup


class LocalGroupCreateView(
    auth_mixins.LoginRequiredMixin,
    auth_mixins.PermissionRequiredMixin,
    edit_views.CreateView,
):
    model = LocalGroup
    form_class = LocalGroupForm
    template_name = "eahub/edit_group.html"
    permission_required = "localgroups.create_local_group"

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        if hasattr(user, "profile"):
            initial["organisers"] = [user]
        return initial

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "user": self.request.user}

    def form_valid(self, form):
        form.instance.geocode()
        print(self.kwargs)
        send_mail_on_change(self.request, form.cleaned_data["name"], "create_group.txt")
        return super().form_valid(form)


class LocalGroupDetailView(detail_views.DetailView):
    queryset = LocalGroup.objects.filter(is_public=True)
    template_name = "eahub/group.html"
    context_object_name = "group"


class LocalGroupUpdateView(rules_views.PermissionRequiredMixin, edit_views.UpdateView):
    queryset = LocalGroup.objects.filter(is_public=True)
    form_class = LocalGroupForm
    template_name = "eahub/edit_group.html"
    permission_required = "localgroups.change_local_group"

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "user": self.request.user}

    def form_valid(self, form):
        if "city_or_town" in form.changed_data or "country" in form.changed_data:
            form.instance.geocode()
        send_mail_on_change(self.request, form.cleaned_data["name"], "update_group.txt", self.kwargs["slug"])

        return super().form_valid(form)


class LocalGroupDeleteView(rules_views.PermissionRequiredMixin, edit_views.DeleteView):
    queryset = LocalGroup.objects.filter(is_public=True)
    template_name = "eahub/delete_group.html"
    success_url = urls.reverse_lazy("groups")
    permission_required = "localgroups.delete_local_group"

    def form_valid(self, form):
        send_mail_on_change(self.request, form.cleaned_data["name"], "delete_group.txt", self.kwargs["slug"])
        return super().form_valid(form)


class ReportGroupAbuseView(ReportAbuseView):
    def profile(self):
        return LocalGroup.objects.get(slug=self.kwargs["slug"], is_public=True)

    def get_type(self):
        return "group"


@login_required
@require_POST
def claim_group(request, slug):
    group = get_object_or_404(LocalGroup, slug=slug, is_public=True)
    subject = "EA Group claimed: {0}".format(group.name)
    try:
        user_eahub_url = "https://{0}/profile/{1}".format(
            get_current_site(request).domain, request.user.profile.slug
        )
        user_name = request.user.profile.name
    except Profile.DoesNotExist:
        user_eahub_url = "about:blank"
        user_name = request.user.email
    message = render_to_string(
        "emails/claim_group.txt",
        {
            "user_eahub_url": user_eahub_url,
            "user_name": user_name,
            "group_name": group.name,
            "group_url": "https://{0}/group/{1}".format(
                get_current_site(request).domain, group.slug
            ),
            "user_email": request.user.email,
        },
    )
    recipient_list = [email for email in settings.LEAN_MANAGERS]
    recipient_list.append(settings.GROUPS_EMAIL)
    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list=recipient_list
    )
    messages.success(
        request,
        "Thank you, we have received your request to claim this group. "
        "Our admin team will send you an email once they have checked your request.",
    )
    return redirect("/group/{}".format(group.slug))


@login_required
@require_POST
def report_group_inactive(request, slug):
    group = get_object_or_404(LocalGroup, slug=slug, is_public=True)
    subject = "EA Group reported as inactive: {0}".format(group.name)
    try:
        user_eahub_url = "https://{0}/profile/{1}".format(
            get_current_site(request).domain, request.user.profile.slug
        )
    except Profile.DoesNotExist:
        user_eahub_url = "about:blank"
    message = render_to_string(
        "emails/report_group_inactive.txt",
        {
            "user_eahub_url": user_eahub_url,
            "user_name": request.user.profile.name,
            "group_name": group.name,
            "group_url": "https://{0}/group/{1}".format(
                get_current_site(request).domain, group.slug
            ),
            "user_email": request.user.email,
        },
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list=settings.LEAN_MANAGERS,
    )
    messages.success(
        request,
        "Thank you, we have received your report. "
        "Our admin team will send you an email once they have looked into it.",
    )
    return redirect("/group/{}".format(group.slug))

@login_required
@require_POST
def send_mail_on_change(request, template, name, slug=None):
    subject = "EA Group changed: {0}".format(name)
    try:
        user_eahub_url = "https://{0}/profile/{1}".format(
            get_current_site(request).domain, request.user.profile.slug
        )
        user_name = request.user.profile.name
    except Profile.DoesNotExist:
        user_eahub_url = "about:blank"
        user_name = request.user.email
    info = {
        "user_eahub_url": user_eahub_url,
        "user_name": user_name,
        "group_name": name
    }
    if slug is not None:
        info["group_url"] = "https://{0}/group/{1}".format(
                get_current_site(request).domain, slug
            )
    message = render_to_string(
        "emails/{0}".format(template),
        info,
    )
    recipient_list = [email for email in settings.LEAN_MANAGERS]
    recipient_list.append(settings.GROUPS_EMAIL)
    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list=recipient_list
    )