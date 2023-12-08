from rest_framework.views import APIView
from rest_framework import status,viewsets
from rest_framework.response import Response
from  django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *

# Create your views here.
class UserSignUpAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = SignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message":"User created successfully", "user":SignUpSerializer(user).data},status=status.HTTP_201_CREATED)
        
        return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)        

# custom login
class CustomLoginUserAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email is None or password is None:
            error_data = {}
            if email is None:
                error_data['email'] = 'Email field cannot be empty.'
            if password is None:
                error_data['password'] = 'Password field cannot be empty.'
            
            return Response({"errors":error_data},status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email,password=password)
        
        if user is None:
            return Response({"error":"Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)
        
        token_serializer =TokenObtainPairSerializer(data={'email':email,'password':password})
        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data
        serializer = UserSerializer(user)
        
        return Response({'user':serializer.data,'access_token':tokens['access'],'refresh_token':tokens['refresh']},status=status.HTTP_200_OK)
       
#User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # Note: We're excluding POST method to handle user registration separately
    http_method_names = ["get", "put", "patch", "delete"]

# Change Password
class ChangePasswordAPIView(APIView):
    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        current_password = serializer.validated_data.get("current_password")
        new_password = serializer.validated_data.get("new_password")
        
        if not user.check_password(current_password):
            return Response({'error':'Your Current password does not match '}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 8 :
            return Response({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)


 




