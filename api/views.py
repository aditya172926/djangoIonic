from django.shortcuts import render
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        return Response({
            "status": "User Registered"
        })

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        rresponse = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key = rresponse.data['token'])
        return Response({'token': token.key, 'id': token.user_id})

@csrf_exempt
def userLogout(request):
    dictionary = json.loads(request.body)
    token_user_id = dictionary['key']
    Token.objects.get(user_id = token_user_id).delete()
    return HttpResponse('Done')
