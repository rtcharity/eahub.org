from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from djangocms_helpers.utils.send_email import send_email

from eahub.base.models import FeedbackURLConfig, MessagingLog, User
from eahub.base.utils import get_admin_email
from eahub.base.views import ReportAbuseView, SendMessageView
from eahub.profiles.forms import DeleteProfileForm, ProfileForm
from eahub.profiles.models import Profile, ProfileSlug


def profile_detail_or_redirect(request, slug, first_visit=False):
    slug_entry = get_object_or_404(ProfileSlug, slug=slug)
    profile = slug_entry.content_object
    if not (profile and request.user.has_perm("profiles.view_profile", profile)):
        raise Http404("No profile exists with that slug.")
    if slug_entry.redirect:
        return redirect("profile", slug=profile.slug, permanent=True)
    return render(
        request, "eahub/profile.html", {"profile": profile, "first_visit": first_visit}
    )


def profile_redirect_from_legacy_record(request, legacy_record):
    user = request.user
    profile = get_object_or_404(
        Profile.objects.visible_to_user(user), legacy_record=legacy_record
    )
    assert user.has_perm("profiles.view_profile", profile)
    return redirect("profile", slug=profile.slug, permanent=True)


@login_required
def my_profile(request, first_visit=False):
    if not hasattr(request.user, "profile"):
        raise Http404("user has no profile")
    return profile_detail_or_redirect(
        request, slug=request.user.profile.slug, first_visit=first_visit
    )


class ReportProfileAbuseView(ReportAbuseView):
    def profile(self):
        return Profile.objects.get(slug=self.kwargs["slug"])

    def get_type(self):
        return "profile"


class SendProfileMessageView(SendMessageView):
    def get_recipient(self):
        profile = Profile.objects.get(slug=self.kwargs["slug"])
        if profile is None:
            raise Http404("Could not find profile")
        return profile

    def form_valid(self, form) -> HttpResponse:
        recipient = self.get_recipient()
        sender_name = form.cleaned_data["your_name"]
        send_email(
            email_subject=f"{sender_name} sent you a message",
            template_path_without_extension="emails/message_profile",
            template_context={
                "sender_name": sender_name,
                "recipient": recipient.get_full_name(),
                "message": form.cleaned_data["your_message"],
                "admin_email": get_admin_email(),
                "feedback_url": FeedbackURLConfig.get_solo().site_url,
                "profile_edit_url": self.request.build_absolute_uri(
                    reverse("edit_profile")
                ),
            },
            email_destination=recipient.user.email,
            email_from=get_admin_email(),
            email_reply_to=form.cleaned_data["your_email_address"],
        )
        MessagingLog.objects.create(
            sender_email=form.cleaned_data["your_email_address"],
            recipient_email=recipient.user.email,
            recipient_type=MessagingLog.USER,
        )
        messages.success(
            self.request, f"Your message to {recipient.first_name} has been sent"
        )
        return redirect(reverse("profiles_app:profile", args=([recipient.slug])))

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("profiles.message_users"):
            raise PermissionDenied()
        recipient = self.get_recipient()
        if recipient.is_can_receive_message():
            return super().get(request, *args, **kwargs)
        else:
            raise Http404("Messaging not enabled for this user")

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm("profiles.message_users"):
            raise PermissionDenied()
        recipient = self.get_recipient()
        if recipient.is_can_receive_message():
            return super().post(request, *args, **kwargs)
        else:
            raise Http404("Messaging not enabled for this user")


@method_decorator(login_required, name="dispatch")
class ProfileUpdate(UpdateView):
    model = Profile
    template_name = "eahub/edit_profile.html"
    form_class = ProfileForm

    def get_object(self, queryset=None) -> Profile:
        return Profile.objects.get(user=self.request.user)


@login_required
def delete_profile(request) -> HttpResponse:
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        user.delete()
        return redirect("account_logout")
    else:
        form = DeleteProfileForm()
        return render(request, "eahub/delete_profile.html", {"form": form})


def profiles(request) -> HttpResponse:
    return render(request, "eahub/profiles.html")
