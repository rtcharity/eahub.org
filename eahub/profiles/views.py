import logging

from django import http
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from flags.state import flag_enabled

from ..base.models import FeedbackURLConfig, MessagingLog, User
from ..base.utils import get_admin_email
from ..base.views import (
    ReportAbuseView,
    SendMessageView,
    get_private_profiles,
    get_profiles_data,
)
from ..localgroups.models import LocalGroup
from .forms import (
    DeleteProfileForm,
    EditProfileCareerForm,
    EditProfileCauseAreasForm,
    EditProfileCommunityForm,
    EditProfileForm,
)
from .models import (
    CauseArea,
    ExpertiseArea,
    GivingPledge,
    Membership,
    OrganisationalAffiliation,
    Profile,
    ProfileAnalyticsLog,
    ProfileSlug,
)


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
        raise http.Http404("user has no profile")
    return profile_detail_or_redirect(
        request, slug=request.user.profile.slug, first_visit=first_visit
    )


@login_required
def my_profile_first_visit(request):
    return my_profile(request, True)


@login_required
def download(request):
    if not hasattr(request.user, "profile"):
        raise http.Http404("user has no profile")
    profile = Profile.objects.get(pk=request.user.profile.id)
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{profile.slug}.zip"'
    profile.write_data_export_zip(request, response)
    return response


class ReportProfileAbuseView(ReportAbuseView):
    def profile(self):
        return Profile.objects.get(slug=self.kwargs["slug"])

    def get_type(self):
        return "profile"


class SendProfileMessageView(SendMessageView):
    def get_recipient(self):
        profile = Profile.objects.get(slug=self.kwargs["slug"])
        if profile is None:
            raise Exception("Could not find profile")
        return profile

    def form_valid(self, form):
        message = form.cleaned_data["your_message"]
        recipient = self.get_recipient()
        sender_name = form.cleaned_data["your_name"]
        subject = f"{sender_name} wants to connect with {recipient.name}!"
        sender_email_address = form.cleaned_data["your_email_address"]
        feedback_url = FeedbackURLConfig.get_solo().site_url
        admins_email = get_admin_email()
        profile_edit_url = self.request.build_absolute_uri(reverse("edit_profile"))

        txt_message = render_to_string(
            "emails/message_profile.txt",
            {
                "sender_name": sender_name,
                "recipient": recipient.name,
                "message": message,
                "admin_email": admins_email,
                "feedback_url": feedback_url,
                "profile_edit_url": profile_edit_url,
            },
        )
        html_message = render_to_string(
            "emails/message_profile.html",
            {
                "sender_name": sender_name,
                "recipient": recipient.name,
                "message": message,
                "admin_email": admins_email,
                "feedback_url": feedback_url,
                "profile_edit_url": profile_edit_url,
            },
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=txt_message,
            from_email=admins_email,
            to=[recipient.user.email],
            reply_to=[sender_email_address],
        )
        email.attach_alternative(html_message, "text/html")

        email.send()

        log = MessagingLog(
            sender_email=sender_email_address,
            recipient_email=recipient.user.email,
            recipient_type=MessagingLog.USER)
        log.save()

        messages.success(
            self.request, "Your message to " + recipient.name + " has been sent"
        )
        return redirect(reverse("profile", args=([recipient.slug])))

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("profiles.message_users"):
            raise PermissionDenied
        recipient = self.get_recipient()
        if not flag_enabled("MESSAGING_FLAG", request=request):
            raise Http404("Messaging toggled off")
        if recipient.get_can_receive_message():
            return super().get(request, *args, **kwargs)
        else:
            raise Http404("Messaging not enabled for this user")

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm("profiles.message_users"):
            raise PermissionDenied
        recipient = self.get_recipient()
        if not flag_enabled("MESSAGING_FLAG", request=request):
            raise Http404("Messaging toggled off")
        if recipient.get_can_receive_message():
            return super().post(request, *args, **kwargs)
        else:
            raise Http404("Messaging not enabled for this user")


@login_required
def edit_profile(request):
    if not hasattr(request.user, "profile"):
        raise http.Http404("user has no profile")
    profile = Profile.objects.get(pk=request.user.profile.id)
    if request.method == "POST":
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            profile = form.save(commit=False)
            profile = profile.geocode()
            profile.save()
            return redirect("my_profile")
    else:
        form = EditProfileForm(instance=request.user.profile)
    opportunities = []
    if profile.open_to_job_offers:
        opportunities.append("job offers")
    if profile.available_to_volunteer:
        opportunities.append("volunteering opportunities")
    if profile.available_as_speaker:
        opportunities.append("speaking opportunities")
    return render(
        request,
        "eahub/edit_profile.html",
        {"form": form, "profile": profile, "opportunities": opportunities},
    )


def reorder_cause_areas(causes):
    return sorted(causes, key=lambda x: x[1].label)


@login_required
def edit_profile_cause_areas(request):
    if not hasattr(request.user, "profile"):
        raise http.Http404("user has no profile")
    if request.method == "POST":
        form = EditProfileCauseAreasForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            cause_areas = request.POST.getlist("cause_areas")
            profile.cause_areas = cause_areas
            giving_pledges = request.POST.getlist("giving_pledges")
            profile.giving_pledges = giving_pledges
            profile.save()
            return redirect("my_profile")
    else:
        form = EditProfileCauseAreasForm(instance=request.user.profile)
    return render(
        request,
        "eahub/edit_profile_cause_areas.html",
        {
            "form": form,
            "profile": Profile.objects.get(pk=request.user.profile.id),
            "cause_area_choices": reorder_cause_areas(CauseArea.choices()),
            "giving_pledge_choices": GivingPledge.choices,
        },
    )


@login_required
def edit_profile_career(request):
    if not hasattr(request.user, "profile"):
        raise http.Http404("user has no profile")
    if request.method == "POST":
        form = EditProfileCareerForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)

            expertise_areas = request.POST.getlist("expertise_areas")
            profile.expertise_areas = expertise_areas
            career_interest_areas = request.POST.getlist("career_interest_areas")
            profile.career_interest_areas = career_interest_areas

            profile.save()
            return redirect("my_profile")
    else:
        form = EditProfileCareerForm(instance=request.user.profile)
    return render(
        request,
        "eahub/edit_profile_career.html",
        {
            "form": form,
            "profile": Profile.objects.get(pk=request.user.profile.id),
            "expertise_area_choices": ExpertiseArea.choices,
        },
    )


def reorder_orgs(orgs):
    return sorted(orgs, key=lambda x: x[1].label)


@login_required
def edit_profile_community(request):
    if not hasattr(request.user, "profile"):
        raise http.Http404("user has no profile")
    if request.method == "POST":
        form = EditProfileCommunityForm(request.POST, instance=request.user.profile)
        old_local_groups = [
            group.name
            for group in LocalGroup.objects.filter(
                membership__profile=request.user.profile
            )
        ]
        if form.is_valid():
            profile = form.save(commit=False)
            profile.local_groups.clear()
            organisational_affiliations = request.POST.getlist(
                "organisational_affiliations"
            )
            profile.organisational_affiliations = [
                int(x) for x in organisational_affiliations
            ]
            profile.save()
            group_affiliations = request.POST.getlist("local_groups")
            local_groups = LocalGroup.objects.filter(id__in=group_affiliations)

            for group in local_groups:
                membership = Membership(profile=profile, local_group=group)
                membership.save()
            if old_local_groups != [x.name for x in local_groups.all()]:
                log = ProfileAnalyticsLog()
                log.profile = request.user.profile
                log.action = "Update"
                log.old_value = old_local_groups
                log.new_value = [x.name for x in local_groups.all()]
                log.field = "local_groups"
                log.save()

            return redirect("my_profile")
    else:
        form = EditProfileCommunityForm(instance=request.user.profile)
    return render(
        request,
        "eahub/edit_profile_community.html",
        {
            "form": form,
            "profile": Profile.objects.get(pk=request.user.profile.id),
            "organisation_choices": reorder_orgs(OrganisationalAffiliation.choices()),
        },
    )


@login_required
def delete_profile(request):
    if request.method == "POST":
        logging.info(
            "user_id={} email={} has deleted their account".format(
                request.user.id, request.user.email
            )
        )
        user = User.objects.get(id=request.user.id)
        user.delete()
        return redirect("account_logout")
    else:
        form = DeleteProfileForm()
        return render(request, "eahub/delete_profile.html", {"form": form})


def profiles(request):
    profiles_data = get_profiles_data(request.user)
    private_profiles = get_private_profiles(request.user)
    return render(
        request,
        "eahub/profiles.html",
        {
            "page_name": "Profiles",
            "profiles": profiles_data["rows"],
            "map_locations": {
                "profiles": profiles_data["map_data"],
                "private_profiles": private_profiles,
            },
        },
    )
