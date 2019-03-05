
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


@login_required
@require_POST
def claim_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    subject = "EA Group claimed: {0}".format(group.name)
    user_eahub_url = "https://{0}/profile/{1}".format(get_current_site(request).domain,request.user.profile.slug)
    message = render_to_string('emails/claim_group.html', {
        'user_eahub_url': user_eahub_url,
        'user_name': request.user.profile.name,
        'group_name': group.name,
        'user_email': request.user.email
    })
    mail_managers(subject, message)
    messages.success(
        request,
        ''' Thank you, we have received your request to claim this group. Our admin team will send you an email once they have checked your request. ''',
    )
    return redirect('/group/{}'.format(group.slug))
