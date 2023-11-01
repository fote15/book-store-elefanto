"""
Views for author module
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Author
from . serializers import AuthorListSerializer
# Create your views here.


@api_view(('GET',))
@permission_classes((AllowAny,))
def get_all_authors(req):
    queryset = Author.objects.filter().all()
    serializer = AuthorListSerializer(queryset, many=True)
    return Response(serializer.data)
