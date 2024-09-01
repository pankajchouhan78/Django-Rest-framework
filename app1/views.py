from app1.models import Student
from app1.serializer import StudentSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import io


@csrf_exempt
def students(request, pk=None):

    if request.method == "GET": 
        if pk is not None:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')   
        else:
            student = Student.objects.all()
            serializer = StudentSerializer(student, many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
           
    elif request.method == 'POST':
        json_data = request.body.decode('utf-8')
        stream = io.BytesIO(json_data.encode('utf-8'))
        python_data = JSONParser().parse(stream)
        serializer = StudentSerializer(data = python_data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Data Created Successfully'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        else:
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')
        
    if request.method == "PUT":
        json_data = request.body.decode('utf-8')
        stream = io.BytesIO(json_data.encode('utf-8'))
        python_data = JSONParser().parse(stream)
        pk = python_data.get('id', None)
        if pk is not None:
            try:
                student = Student.objects.get(pk=pk)
            except Student.DoesNotExist:
                res = {
                    'msg':'Student Not Found'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            serializer = StudentSerializer(instance=student, data=python_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {
                    'msg':'Data successfully updated'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            
            res = {'msg':serializer.errors}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
    
    elif request.method == 'DELETE':
        json_data = request.body.decode('utf-8')
        stream = io.BytesIO(json_data.encode('utf-8'))
        python_data = JSONParser().parse(stream)
        pk = python_data.get('id', None)
        if pk is None:
            res = {"msg": "id is required "}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, context_type='application/json')
        
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            res = {
                'msg':'Student Not Found'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        student.delete()
        res = {"msg": "Data successfully deleted"}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, context_type='application/json')


