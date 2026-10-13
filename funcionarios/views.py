from rest_framework import permissions, viewsets
from .models import Funcionario
from .serializers import FuncionarioSerializer

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    # Dados de funcionários (CPF, endereço) só para administradores (is_staff).
    permission_classes = [permissions.IsAdminUser]
