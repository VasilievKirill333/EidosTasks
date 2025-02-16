from django import forms
from .models import Task, Project

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "is_completed"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"}),
            "description": forms.Textarea(attrs={"class": "w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 h-32 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "h-5 w-5 border-gray-300 text-indigo-500 focus:ring-indigo-500"})
        }


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out'}),
            "description": forms.Textarea(attrs={"class": "w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 h-32 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out"}),
        }
