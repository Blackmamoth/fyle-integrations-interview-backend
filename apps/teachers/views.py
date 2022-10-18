from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from apps.students.models import Assignment
from .serializers import TeacherAssignmentSerializer

# Create your views here.
class TeacherAssignmentsView(APIView):
    
    def get(self,  request: Request):
        assignments = Assignment.objects.filter(teacher__user=request.user)
        serializer = TeacherAssignmentSerializer(assignments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request: Request):
        assignment_id = request.data.get('id')
        assignment = Assignment.objects.get(id=assignment_id)
        serializer = TeacherAssignmentSerializer(instance=assignment, data=request.data, partial=True, context={'teacher_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        