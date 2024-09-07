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
        
        
from django.db.models import Count
from .models import *

class QuestionsAllowForm(forms.ModelForm):
    pass
    class Meta:
        model = QuestionsAllow
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the queryset for 'sub' field to exclude objects that have been associated three times
        queryset = add_subjects.objects.annotate(num_questions=Count('questionsallow')).exclude(num_questions__gte=3)
        self.fields['sub'].queryset = queryset


class CodingQuestionsAllowForm(forms.ModelForm):
    pass
    class Meta:
        model = CodingQuestionsAllow
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the queryset for 'sub' field to exclude objects that have been associated three times
        queryset = add_subjects.objects.annotate(num_questions=Count('codingquestionsallow')).exclude(num_questions__gte=3)
        self.fields['coding_sub'].queryset = queryset


