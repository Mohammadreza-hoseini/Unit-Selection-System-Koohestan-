import random

from django.contrib.auth.hashers import make_password
from django.utils import timezone


from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from koohestan.tasks import send_email_task

from .models import UserRole, OTPCode


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def _generate_otp(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    def _generate_expire_time(self):
        return timezone.now() + timezone.timedelta(seconds=60)

    def validate(self, attrs):
        email = attrs['email']
        if not UserRole.objects.filter(email=email).exists():
            raise ValidationError('User does not exist')

        code = self._generate_otp()
        expire_time = self._generate_expire_time()
        OTPCode.objects.create(code=code, email=email, code_expire=expire_time)

        # send email
        send_email_task.delay(email, code)
        return attrs


class ChangePasswordAction(serializers.Serializer):
    code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        code = attrs['code']
        get_otp_code = OTPCode.objects.filter(code=code)
        if not get_otp_code.exists():
            raise ValidationError('This code does not exist')
        elif timezone.now() > get_otp_code.first().code_expire:
            raise ValidationError('The code has expired')
        elif code != get_otp_code.first().code:
            raise ValidationError('Code is wrong')
        return attrs

    def create(self, validated_data):
        get_otp_code = OTPCode.objects.filter(code=validated_data['code']).first()
        get_user = UserRole.objects.get(email=get_otp_code.email)
        get_user.password = make_password(validated_data['password'])
        get_user.save()
        get_user.student_user_role.password = make_password(validated_data['password'])
        get_user.student_user_role.save()
        return get_user


# End code of Mohammadreza hoseini

class UserRoleGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('id', 'username', 'role')
