from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from eahub.jobs.models import Job
from eahub.jobs.models import JobTag
from eahub.jobs.models import JobTagStatus
from eahub.jobs.models import JobTagType
from eahub.jobs.serializers import JobSerializer
from eahub.jobs.serializers import JobTagSerializer
from eahub.tags.views import create_tag_view_factory


class JobViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Job.objects.filter()
    serializer_class = JobSerializer


create_tag_view = create_tag_view_factory(
    tag_model=JobTag,
    tagged_model=Job,
    tag_status_enum=JobTagStatus,
    tag_type_model=JobTagType,
    tag_serializer=JobTagSerializer,
)


def jobs_list_view(request: HttpRequest) -> HttpResponse:
    return render(request, "jobs/job_list.html")


class JobCreateView(CreateView):
    model = Job
    template_name = "jobs/job_create.html"
    fields = [
        "title",
        "company",
        "company_logo",
        "description_teaser",
        "description",
        "experience_min",
        "experience_max",
        "salary_min",
        "salary_max",
        "salary_currency",
        "visibility",
        "is_visa_sponsor",
        "is_remote_only",
        "expires_at",
    ]

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = Job.objects.create(
            author=self.request.user.profile,
        )
        return super().get(request, *args, **kwargs)
