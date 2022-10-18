from re import L
from rest_framework import serializers
from apps.students.models import Assignment

class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, data):
        instance = self.instance

        if instance.state == "DRAFT":
            raise serializers.ValidationError({'non_field_errors': 'SUBMITTED assignments can only be graded'})
        if instance.state == "GRADED":
            raise serializers.ValidationError({'non_field_errors': 'GRADED assignments cannot be graded again'})
        if data.get('content'):
            raise serializers.ValidationError({'non_field_errors': 'Teacher cannot change the content of the assignment'})
        return data

    def validate_grade(self, grade):
        valid_choices = ['A', 'B', 'C', 'D']
        if not grade in valid_choices:
            raise serializers.ValidationError('is not a valid choice.')
        return grade

    def save(self):
        assignment = self.instance
        assignment.state = "GRADED"
        assignment.save()