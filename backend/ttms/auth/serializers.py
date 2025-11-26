from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JWTTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer as JWTTokenRefreshSerializer
from django.contrib.auth import authenticate
from .models import TTMSUser


class TTMSUserSerializer(serializers.ModelSerializer):
    """
    Serializer for TTMS User model.
    Used for user profile and data representation.
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = TTMSUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'role_display', 'facility_id', 'phone_number',
            'employee_id', 'is_active', 'last_login_facility',
            'last_login_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'role_display', 'full_name', 'last_login_at',
            'created_at', 'updated_at'
        ]


class TTMSUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new TTMS users.
    Includes password handling.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = TTMSUser
        fields = [
            'email', 'first_name', 'last_name', 'password',
            'password_confirm', 'role', 'facility_id', 'phone_number',
            'employee_id'
        ]
    
    def validate_password(self, value):
        """Validate password strength."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def validate(self, data):
        """Validate password match."""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError(
                {'password_confirm': "Passwords do not match."}
            )
        return data
    
    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = TTMSUser.objects.create_user(
            email=validated_data['email'],
            password=password,
            **validated_data
        )
        return user


class TTMSTokenObtainPairSerializer(JWTTokenObtainPairSerializer):
    """
    Custom JWT Token Obtain Pair Serializer for TTMS.
    Authenticates user by email and password.
    """
    username_field = 'email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()
        if 'username' in self.fields:
            del self.fields['username']
    
    @classmethod
    def get_token(cls, user):
        """
        Add custom claims to JWT token.
        """
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['facility_id'] = user.facility_id
        token['full_name'] = user.get_full_name()
        
        return token
    
    def validate(self, attrs):
        """
        Override validate to use email instead of username.
        """
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(request=self.context.get('request'), username=email, password=password)
        
        if not user:
            raise serializers.ValidationError(
                {'detail': 'Invalid email or password.'}
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                {'detail': 'User account is inactive.'}
            )
        
        refresh = self.get_token(user)
        
        data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
        return data


class TTMSTokenRefreshSerializer(JWTTokenRefreshSerializer):
    """
    Custom JWT Token Refresh Serializer for TTMS.
    """
    pass


class TTMSUserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    Excludes sensitive fields.
    """
    class Meta:
        model = TTMSUser
        fields = [
            'first_name', 'last_name', 'phone_number',
            'facility_id', 'last_login_facility'
        ]


class TTMSChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    def validate_new_password(self, value):
        """Validate new password strength."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def validate(self, data):
        """Validate passwords match."""
        if data.get('new_password') != data.get('new_password_confirm'):
            raise serializers.ValidationError(
                {'new_password_confirm': "Passwords do not match."}
            )
        return data
    
    def save(self, user):
        """Save new password for user."""
        if not user.check_password(self.validated_data['old_password']):
            raise serializers.ValidationError(
                {'old_password': "Incorrect password."}
            )
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
