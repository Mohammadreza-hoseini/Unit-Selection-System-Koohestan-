from rest_framework import serializers
from .models import Professor


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('firstname',
                  'lastname',
                  'professor_number',
                  'password',
                  'email',
                  'national_code',
                  'faculty',
                  'major',
                  'expertise',
                  'degree',
                  'past_teaching_lessons',
                  )
