from rest_framework import serializers
from .models import Person  # Ensure this import is correct

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'  # Ensuring all fields are included

    def validate(self, data):
        name = data.get("name")  # Use .get() to avoid KeyError
        phone = data.get("phone")
        age = data.get("age")

        if name and not name.replace(" ", "").isalpha():
            raise serializers.ValidationError({"name": "Name should only contain alphabets"})

        if phone and (not str(phone).isdigit() or len(str(phone)) != 10):
            raise serializers.ValidationError({"phone": "Phone number must be a 10-digit numeric value"})

        if age and age < 18:
            raise serializers.ValidationError({"age": "Age should be greater than 18"})

        return data


