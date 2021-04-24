from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from djangocms_helpers.utils.send_email import send_email

from eahub.base.models import FeedbackURLConfig, MessagingLog, User
from eahub.base.utils import get_admin_email
from eahub.base.views import ReportAbuseView, SendMessageView
from eahub.feedback.forms import FeedbackForm
from eahub.profiles.forms import DeleteProfileForm, ProfileForm
from eahub.profiles.models import Profile, ProfileSlug


def profile_detail_or_redirect(request: HttpRequest, slug: str) -> HttpResponse:
    slug_entry = get_object_or_404(ProfileSlug, slug=slug)
    profile: Profile = slug_entry.content_object
    if not (profile and request.user.has_perm("profiles.view_profile", profile)):
        raise Http404("No profile exists with that slug.")
    if slug_entry.redirect:
        return redirect("profiles_app:profile", slug=profile.slug, permanent=True)
    return render(
        request,
        template_name="eahub/profile.html",
        context={
            "profile": profile,
            "is_render_cause_area_section": (
                profile.available_to_volunteer
                or profile.tags_pledge.exists()
                or profile.tags_cause_area.exists()
                or profile.tags_cause_area_expertise.exists()
                or profile.cause_areas_other
            ),
            "is_render_career_section": (
                profile.open_to_job_offers
                or profile.tags_expertise_area.exists()
                or profile.tags_career_interest.exists()
                or profile.expertise_areas_other
            ),
            "is_render_community_section": (
                profile.local_groups.exists()
                or profile.tags_affiliation.exists()
                or profile.tags_organisational_affiliation.exists()
                or profile.user.localgroup_set.exists
                or profile.topics_i_speak_about
                or profile.available_as_speaker
            ),
        },
    )


def profile_redirect_from_legacy_record(request, legacy_record):
    user = request.user
    profile = get_object_or_404(
        Profile.objects.visible_to_user(user), legacy_record=legacy_record
    )
    assert user.has_perm("profiles.view_profile", profile)
    return redirect("profile", slug=profile.slug, permanent=True)


@login_required
def my_profile(request: HttpRequest) -> HttpResponse:
    if not hasattr(request.user, "profile"):
        raise Http404("user has no profile")
    return profile_detail_or_redirect(request, slug=request.user.profile.slug)


class ReportProfileAbuseView(ReportAbuseView):
    def profile(self) -> Profile:
        return Profile.objects.get(slug=self.kwargs["slug"])

    def get_type(self) -> str:
        return "profile"


class SendProfileMessageView(SendMessageView):
    def get_initial(self) -> dict:
        data_initial = super().get_initial()
        profile = Profile.objects.get(user=self.request.user)
        data_initial["your_name"] = profile.get_full_name()
        data_initial["your_email_address"] = profile.user.email
        return data_initial

    def get_recipient(self) -> Profile:
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
                    reverse("profiles_app:edit_profile")
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

    def form_valid(self, form: ModelForm) -> HttpResponse:
        return super().form_valid(form)

    def _is_import_conformation_form(self) -> bool:
        return bool(self.request.GET.get("import"))


@login_required
def delete_profile(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        user.delete()
        return redirect("account_logout")
    else:
        form = DeleteProfileForm()
        return render(request, "eahub/delete_profile.html", {"form": form})


def profiles(request) -> HttpResponse:
    return render(request, "eahub/profiles.html", {"feedback_form": FeedbackForm()})
