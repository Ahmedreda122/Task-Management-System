from django.shortcuts import render
from .forms import TaskForm
from .models import Task

# Create your views here.
def index(request):
    priority = { 
                0 : "No Priority",
                1 : "Low", 
                2 : "Medium",
                3 : "High" 
    }
    form = TaskForm()
    context = {"Tasks": Task.objects.all(), "form": form, "prioritySentence": priority}
    
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            # Do something with the valid form data
            # For example, save it to the database
            task = Task(
                description= form.cleaned_data["description"],
                deadline = form.cleaned_data["deadline"],
                priority= int(form.cleaned_data["priority"])
            )   
            # Save the Task data into the DB
            task.save()
            
    return render(request, "Home/home.html", context)  