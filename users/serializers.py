from  rest_framework import serializers
from  .models import *

# signup serilaizer

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','username','created_at','password')
        extra_kwargs = {'password':{'write_only':True}}
        
    def create(self,validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
        

# UserSerilaizer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'is_superuser', 'is_staff', 'is_active', 'created_at']
        # exclude = ['updated_at', 'groups', 'user_permissions','password','last_login','date_joined',]
        # fields='__all__'


# change password serilaizer 
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)