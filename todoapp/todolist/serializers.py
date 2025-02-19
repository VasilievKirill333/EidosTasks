import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Task, Project

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description']

class ProjectCustomSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    cr_date = serializers.DateTimeField(read_only=True)

def encode():
    object_1 = Project.objects.create(title='Antonio', description='is a great soccer player')
    object_sr = ProjectCustomSerializer(object_1)
    json_dumped = JSONRenderer().render(object_sr.data)

def decode():
    stream = io.BytesIO(b'{"title": "A", "description": "boba"}')
    data = JSONParser().parse(stream)
    serialz = ProjectCustomSerializer(data=data)
    serialz.is_valid()

