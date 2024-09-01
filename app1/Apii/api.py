from app1.models import Student
from app1.Apii.serializer import StudentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status

@api_view(['GET','POST', 'PUT', 'PATCH', 'DELETE'])
def students(request, pk=None):
    if request.method == 'GET':
        if pk is None:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PUT':
        if pk is None:
            return Response({'details': "please enter id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':"Student not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentSerializer(instance=student , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail':"Student updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PATCH':
        if pk is None:
            return Response({'details': "please enter id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':"Student not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentSerializer(instance=student , data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail':"Student updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        if pk is None:
            return Response({'details': "please enter id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':"Student not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        student.delete()
        return Response({'detail':"Student deleted successfully"}, status=status.HTTP_200_OK)
    
class StudentAPIView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':"Student not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        if pk is None:
            return Response({'details': "please enter id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':"Student not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentSerializer(instance=student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail':'Student successfully updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        if pk is None:
            return Response({'details': "please enter id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':"Student not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentSerializer(instance=student, data=request.data,  partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail':'Student successfully updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if pk is None:
            return Response({'details': "please enter id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':"Student not found"}, status=status.HTTP_400_BAD_REQUEST)
        student.delete()
        return Response({'detail':'Student successfully deleted'}, status=status.HTTP_200_OK)
        

class StudentGenericsView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentGenericsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentGenericsfilter(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.all()
        name = self.request.GET.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class StudentMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

    def post(self, request,  *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class StudentMixinDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    

class StudentViewsets(viewsets.ViewSet):
    def list(self, request):
        serializer = StudentSerializer(Student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if pk is None:
            return Response({'detail':'please enter id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':'Student not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StudentSerializer(instance=student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail':'Student successfully updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        if pk is None:
            return Response({'detail':'please enter id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':'Student not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StudentSerializer(instance=student, data=request.data, partail=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail':'Student successfully updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if pk is None:
            return Response({'detail':'please enter id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail':'Student not found'}, status=status.HTTP_400_BAD_REQUEST)
        student.delete()
        return Response({'detail':'Student successfully deleted'}, status=status.HTTP_200_OK)
    
class StudentModelViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()