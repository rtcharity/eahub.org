import logging

from django import http
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..base.models import User
from ..base.views import ReportAbuseView, SendMessageView
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
    def form_valid(self, form):
        recipient = Profile.objects.get(slug=self.kwargs["slug"])
        message: dict = form.cleaned_data["your_message"]
        sender_email: dict = form.cleaned_data["your_email_address"]
        send_mail(
            f"{sender_email} sent you a message through the EA hub.",
            message,
            sender_email,
            [recipient.user.email],
        )
        messages.success(
            self.request, "Your message to " + recipient.name + " has been sent"
        )
        return redirect(reverse("profile", args=([recipient.slug])))


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


@login_required
def edit_profile_community(request):
    if not hasattr(request.user, "profile"):
        raise http.Http404("user has no profile")
    if request.method == "POST":
        form = EditProfileCommunityForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.local_groups.clear()
            organisational_affiliations = request.POST.getlist(
                "organisational_affiliations"
            )
            profile.organisational_affiliations = organisational_affiliations
            profile.save()
            group_affiliations = request.POST.getlist("local_groups")
            local_groups = LocalGroup.objects.filter(id__in=group_affiliations)
            for group in local_groups:
                membership = Membership(profile=profile, local_group=group)
                membership.save()
            return redirect("my_profile")
    else:
        form = EditProfileCommunityForm(instance=request.user.profile)
    return render(
        request,
        "eahub/edit_profile_community.html",
        {
            "form": form,
            "profile": Profile.objects.get(pk=request.user.profile.id),
            "organisational_affiliation_choices": OrganisationalAffiliation.choices,
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
