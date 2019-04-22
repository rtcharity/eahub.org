from django import http


class Quiet404(http.Http404):
    pass
