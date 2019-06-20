from django import urls
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Q
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

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "user": self.request.user}

    def form_valid(self, form):
        form.instance.geocode()
        return super().form_valid(form)


class LocalGroupDetailView(detail_views.DetailView):
    model = LocalGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.id in self.object.organisers.values_list("id", flat=True):
            _filter = {}
        else:
            _filter = {"profile__is_public": True}
        for field in ["organisers", "past_organisers"]:
            context["visible_" + field] = (
                getattr(self.object, field)
                .filter(Q(**_filter))
                .order_by("profile__name", "profile__slug")
            )
        return context

    template_name = "eahub/group.html"
    context_object_name = "group"


class LocalGroupUpdateView(rules_views.PermissionRequiredMixin, edit_views.UpdateView):
    model = LocalGroup
    form_class = LocalGroupForm
    template_name = "eahub/edit_group.html"
    permission_required = "localgroups.change_local_group"

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "user": self.request.user}

    def form_valid(self, form):
        if "city_or_town" in form.changed_data or "country" in form.changed_data:
            form.instance.geocode()
        return super().form_valid(form)


class LocalGroupDeleteView(rules_views.PermissionRequiredMixin, edit_views.DeleteView):
    model = LocalGroup
    template_name = "eahub/delete_group.html"
    success_url = urls.reverse_lazy("groups")
    permission_required = "localgroups.delete_local_group"


class ReportGroupAbuseView(ReportAbuseView):
    def profile(self):
        return LocalGroup.objects.get(slug=self.kwargs["slug"])

    def get_type(self):
        return "group"


@login_required
@require_POST
def claim_group(request, slug):
    group = get_object_or_404(LocalGroup, slug=slug)
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
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list=settings.LEAN_MANAGERS,
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
    group = get_object_or_404(LocalGroup, slug=slug)
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
