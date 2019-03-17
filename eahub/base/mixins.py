class AssertPermissionMixin:
    """Like PermissionRequiredMixin, but raises AssertionError on failure.

    Intended for defense-in-depth in cases where something equivalent to permissions are
    already being checked elsewhere, such as in a queryset filter.
    """

    def dispatch(self, request, *args, **kwargs):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        assert request.user.has_perms(perms, self.get_object())
        return super().dispatch(request, *args, **kwargs)
