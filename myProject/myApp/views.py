from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task

# priority Dictionary to express every priority degree in a understandable sentence
priority = { 
        0 : "No Priority",
        1 : "Low", 
        2 : "Medium",
        3 : "High" 
}
# Create your views here.
def index(request):
    if request.method == "POST":
        # Get the Form Data Sent by User
        form = TaskForm(request.POST or None)
        # Check that form has no common errors
        if form.is_valid():
            # Assign the form data to new task object to save it into DB
            task = Task(
                description= form.cleaned_data["description"],
                deadline = form.cleaned_data["deadline"],
                priority= int(form.cleaned_data["priority"])
            )   
            # Save the Task data into the DB
            task.save()
    else:
        # Get Django Task Form Created in forms.py
        form = TaskForm()
    
    # Get Tasks Objects from Task Model ordered by their status(active or not) then their priority then their deadline date
    Tasks = Task.objects.all().order_by("-active", "-priority", "deadline").values() 

    context = {"Tasks": Tasks, "form": form, "prioritySentence": priority} 
    # Render home page with help of context data (the Dynamic content)          
    return render(request, "Home/home.html", context)  


def toggleTask(request,id):
    obj = Task.objects.get(ID=id)
    # toggle active value by using the following xor operation 
    obj.active = obj.active ^ True
    obj.save()
    return redirect("index")
    
    
def deleteTask(request,id):
    obj = Task.objects.get(ID=id)
    obj.delete()
    return redirect("index")

def updateTask(request,id):
    # Get object from Task Model by its ID
    task = Task.objects.get(ID=id)
    
    if request.method == "POST":
        # Get the Form Data Sent by User
        form = TaskForm(request.POST, instance=task)
        # Check that form has no common errors
        if form.is_valid():
            # Update the object with the new values provided by the user. 
            # The `save()` method will automatically handle the update operation 
            # and persist the changes to the database. 
            form.save()
            return redirect("index")
    else:
        # Get Django Task Form Created in forms.py and apply old values to its fields
        form = TaskForm(instance=task)
        
    context = {"Task":task,"form": form}
    # Render home page with help of context data (the Dynamic content)        
    return render(request, "Home/update.html", context)  