from rest_framework import serializers
from app1.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = ['id', 'name', 'roll','city']
        fields = '__all__'
        # exclude = ['id']
    
    def validate(self, data):
        name = data.get('name', None)
        if name is not None:
            if len(name) < 5:
                raise serializers.ValidationError({'name': 'Name should be at least 5 characters long.'})
            return data
