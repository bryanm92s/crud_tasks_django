from django import forms  
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        # Cual modelo voy a utilizar
        model = Task
        fields = ['title','description','important']
        # Especificar otros atributos al formulario TaskForm
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'})
        }