from django import urls

from ..base import views

LEGACY_URLS = {
    "about/newsletter/": "newsletter",
    "actions/": "https://www.effectivealtruism.org/get-involved/",
    "actions/donating/": "https://donationswap.eahub.org/charities",
    "contact/": "https://resources.eahub.org/contact-lean/",
    "eahub.org/groups/resources/recruiting-managing-members/": "https://resources.eahub.org/guides_and_tips/tips-from-local-organisers/",
    "groups/facebook-invites/": "https://stackoverflow.com/questions/27080936/how-can-i-select-all-friends-in-new-facebook-events-invite-ui#33698935",
    "groups/get-a-website/": "https://github.com/rtcharity/lean-site-template",
    "groups/local-group-support-overview-lean-cea-and-eaf/": "https://forum.effectivealtruism.org/posts/Cvi7hnTYMk5qutkDg/local-effective-altruism-network-s-new-focus-for-2019",
    "groups/resources/giving-games/": "https://docs.google.com/document/d/1g5G0PvYFs7cAbAZ8ANI_wnsv7DjtBmq4_SQcg44-HDA/edit",
    "groups/<slug:slug>/": "group",
    "index.php/": "index",
    "links/": "https://resources.eahub.org",
    "map/": "profiles",
    "map/people/all/": "profiles",
    "map/people/only-on-map/": "profiles",
    "profile/login/": "account_login",
    "profile/signup/": "account_signup",
    "register/": "account_signup",
    "user/": "my_profile",
    "user/<int:legacy_record>/": "profile_legacy",
    "user/<slug:slug>/": "profile",
    "user/profiles/": "profiles",
    "user.php/": "my_profile",
    "wp-login.php/": "account_login",
}

urlpatterns = [
    urls.path(
        route,
        (
            views.LegacyRedirectView.as_view(url=target)
            if target.startswith("http://") or target.startswith("https://")
            else views.LegacyRedirectView.as_view(pattern_name=target)
        ),
    )
    for route, target in LEGACY_URLS.items()
]
