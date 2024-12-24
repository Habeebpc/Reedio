from rest_framework.filters import BaseFilterBackend


class PodcastPurchaseFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": "month",
                "in": "query",
                "schema": {
                    "type": "string",
                },
            },
            {
                "name": "year",
                "in": "query",
                "schema": {
                    "type": "string",
                },
            }
        ]
