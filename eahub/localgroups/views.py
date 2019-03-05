from django import urls
from django.contrib.auth import mixins as auth_mixins
from django.views.generic import detail as detail_views
from django.views.generic import edit as edit_views
from rules.contrib import views as rules_views

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
