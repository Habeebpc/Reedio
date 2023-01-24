from property.models import (
    TransactionCategory,
    Transaction,
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from user_auth.permission import IsAuthenticatedUser

from property.serializers import (
    TransactionCategorySerializer,
    TransactionSerializer
)


class TransactionCategoryListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer


class TransactionCategoryRetrieveUpdateDestroyView(
        RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer


class TransactionListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}


class TransactionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedUser,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
