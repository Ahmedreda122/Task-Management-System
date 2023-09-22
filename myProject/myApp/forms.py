from django import forms
from django.forms.widgets import DateTimeInput
from .models import Task
from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class TaskForm(forms.ModelForm):
    description = forms.CharField(
      label="Task Name", 
      widget=forms.TextInput(attrs={"class" : "form-control", "placeholder":"Add Task Name"})
      )
    deadline = forms.DateTimeField(
      label="Deadline",
      required=False,
      widget=DateTimeInput(attrs={"type": "datetime-local", "class" : "form-control" , "placeholder":"deadline date"}),
      )
    priority =  forms.ChoiceField(
        label="Priority",
        widget=forms.Select(attrs={"class" : "form-select", "placeholder":"Select Priority"}),
        choices=[
            (0, "No Priority"),
            (3, "High"),
            (2, "Medium"),
            (1, "Low"),
        ],
    )
    class Meta:
        # Specify the Model that the form represents
        model = Task
        # the model fields to show
        fields = [
          "description",
          "deadline",
          "priority"
        ]

    # The constructor
    def __init__(self, *args, **kwargs):
        # Call the parent class __init__ method
        super().__init__(*args, **kwargs)
    
    # Validate deadline date    
    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        
        if deadline and deadline < timezone.now():
            raise forms.ValidationError("Deadline must be in the future.")
        return deadline    
      
      
class NewUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ("username", "password1", "password2")
  # super(NewUserForm, self).save(commit=False) line calls the save method of the parent class (UserCreationForm).
  # This parent class is responsible for handling the form data 
  # And creating a new instance of the User model with the provided data.
	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		if commit:
			user.save()
		return user