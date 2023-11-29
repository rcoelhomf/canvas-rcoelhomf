from rest_framework.generics import CreateAPIView
from .models import Account
from .serializers import AccountSerializer


class UserView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
