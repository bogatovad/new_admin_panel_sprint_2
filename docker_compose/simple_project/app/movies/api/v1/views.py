from django.views.generic.detail import BaseDetailView

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesMixin:
    model = Filmwork
    http_method_names = ['get']

    @staticmethod
    def array_agg_person(role: str):
        return ArrayAgg(
            "person__full_name", filter=Q(persons__role=role)
        )

    @staticmethod
    def array_agg_genre():
        return ArrayAgg(
                "genres__name", distinct=True
            )

    def get_queryset(self):
        return self.model.objects.prefetch_related("genre", "persons").values().annotate(
            actors=self.array_agg_person(role='actor'),
            directors=self.array_agg_person(role='director'),
            writers=self.array_agg_person(role='writer'),
            genres=self.array_agg_genre()
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesMixin, BaseListView):
    paginate_by: int = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return kwargs['object']
