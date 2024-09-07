from django import forms
from mockapp.models import uploaddocument, Student_result, student

# Here the form is used to handle user input and file uploads.

class DocumentForm(forms.ModelForm):
    class Meta:
        model = uploaddocument
        fields = ['course_name', 'document']

class StudentForm(forms.ModelForm):
    class Meta:
        model = student
        fields = '__all__'


