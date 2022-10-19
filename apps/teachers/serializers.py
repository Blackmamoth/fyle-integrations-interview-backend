from re import L
from rest_framework import serializers
from apps.students.models import Assignment

class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, data):
        instance = self.instance
        context = self.context
        if data.get('student'):
            raise serializers.ValidationError({'non_field_errors': 'Teacher cannot change the student who submitted the assignment'})
        if data.get('content'):
            raise serializers.ValidationError({'non_field_errors': 'Teacher cannot change the content of the assignment'})
        if instance.state == "DRAFT":
            raise serializers.ValidationError({'non_field_errors': 'SUBMITTED assignments can only be graded'})
        if instance.state == "GRADED":
            raise serializers.ValidationError({'non_field_errors': 'GRADED assignments cannot be graded again'})
        if not context.get('teacher_id') == instance.teacher.id:
            raise serializers.ValidationError({'non_field_errors': 'Teacher cannot grade for other teacher\'s assignment'})
        instance.grade = data.get('grade')
        instance.state = data.get('state')
        return data

    def validate_grade(self, grade):
        valid_choices = [choice[0] for choice in self.instance.grade.field.choices]
        if not grade in valid_choices:
            raise serializers.ValidationError('is not a valid choice.')
        print('2')
        return grade