from rest_framework import serializers
from .models import Student

def city_is_ujjain(value):
    if value.lower() != 'ujjain':
        raise serializers.ValidationError("city must be ujjain")

class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    roll = serializers.IntegerField()
    city = serializers.CharField(max_length=50, validators=[city_is_ujjain])

    # field level validation
    # def validate_name(self, value):
    #     if not value.isalpha():
    #         raise serializers.ValidationError("Name should only contain alphabets")
    #     return value
    
    # def validate_roll(self, value):
    #     if value < 0:
    #         raise serializers.ValidationError("Enter Positive roll number")
    #     return value

    # object level validation
    def validate(self, data): 
        if not data['name'].isalpha():
            raise serializers.ValidationError("Name should only contain alphabets")
        
        if data['roll'] < 0:
            raise serializers.ValidationError("Enter Positive roll number")
        
        return data
    

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
    
    def update(self, instace,validated_data):
        instace.name = validated_data.get('name', instace.name)
        instace.roll = validated_data.get('roll', instace.roll)
        instace.city = validated_data.get('city', instace.city)
        instace.save() # validated_data means new data from user for update
        return instace # instace means old data stored in database 