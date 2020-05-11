from django.contrib.auth import get_user_model
from rest_framework import serializers
from admin_user.models import AdminUser



User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'mobile',
            'password',
            'token',
            'expires',
            'message'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "User registered. Wait for authorization."

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=300)

    def validate_email(self, value):
        user_qs = User.objects.filter(email__iexact=value)
        if user_qs.exists():
            raise serializers.ValidationError("User with this email already registered")
        return value

    def validate_mobile(self, value):
        user_qs = User.objects.filter(mobile=value)
        if user_qs.exists():
            raise serializers.ValidationError(
                "Different user with same mobile already exists")
        return value

    def get_token(self, obj):  # instance of the model
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')


        user_obj = User(
            email=validated_data.get('email'),
            mobile=validated_data.get('mobile'),
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = True
        user_obj.save()
        return user_obj




class AdminUserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(style={'input_type': 'text'})
    last_name = serializers.CharField(style={'input_type': 'text'})
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.CharField(style={'input_type': 'email'})
    mobile = serializers.CharField(style={'input_type': 'text'})
    # password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = AdminUser
        # fields = ['email','user']
        fields = (
            'first_name',
            'last_name',
            'email',
            'mobile',
            'password',
            # 'dms_job_card'
        )

        extra_kwargs = {
            'password': {'write_only': True}}
            

    def get_message(self, obj):
        return "User and Device registered. Wait for authorization."

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=24 * 3600)  # 24 hours

    def get_token(self, obj):  # instance of the user model
        user = obj.user
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate_email(self, value):
        user_qs = User.objects.filter(email__iexact=value)
        AppUser_qs = AdminUser.objects.filter(email__iexact=value)

        if AppUser_qs.exists() or user_qs.exists():
            raise serializers.ValidationError("email already registered")
        return value

    def validate_mobile(self, value):
        user_qs = User.objects.filter(email__iexact=value)
        AppUser_qs = AdminUser.objects.filter(mobile=value)

        if AppUser_qs.exists() or user_qs.exists():
            raise serializers.ValidationError(
                "mobile already registered")
        return value

    def create(self, validated_data):
        user_data = {
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name'),
            'email': validated_data.get('email'),
            'mobile': validated_data.get('mobile'),
            'password': validated_data.pop('password')
        }
        user = UserRegisterSerializer.create(UserRegisterSerializer(), validated_data=user_data)
        print (user)
        AppUser_obj = AdminUser.objects.create(user=user,**validated_data)
        return AppUser_obj




