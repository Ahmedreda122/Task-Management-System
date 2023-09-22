from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TaskForm
from .models import Task
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm 

# priority Dictionary to express every priority degree in a understandable sentence
priority = { 
        0 : "No Priority",
        1 : "Low", 
        2 : "Medium",
        3 : "High" 
}
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # Get the Form Data Sent by User
            form = TaskForm(request.POST or None)
            # Check that form has no common errors
            if form.is_valid():
                # Assign the form data to new task object to save it into DB
                task = Task(
                    user = request.user,
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
        Tasks = Task.objects.filter(user=request.user).order_by("-active", "-priority", "deadline")
        context = {"Tasks": Tasks, "form": form, "prioritySentence": priority} 
        # Render home page with help of context data (the Dynamic content)          
        return render(request, "Home/home.html", context)  
    else:
        return redirect("login")


def toggleTask(request,id):
    if request.user.is_authenticated:
        obj = Task.objects.get(ID=id)
        # toggle active value by using the following xor operation 
        obj.active = obj.active ^ True
        obj.save()
        return redirect("index")
    else:
        return redirect("login")
    
def deleteTask(request,id):
    if request.user.is_authenticated:
        obj = Task.objects.get(ID=id)
        obj.delete()
        return redirect("index")
    else:
        return redirect("login")

def updateTask(request,id):
    if request.user.is_authenticated:
        # Get object from Task Model by its ID
        task = Task.objects.get(ID=id)
        
        if request.method == "POST":
            # Get Django Task Form Created in forms.py and apply old values (which exists in task) to its fields
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
    else:
        return redirect("login")


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
            # If the Request was POST and the form data is valid, the form will be saved and the user will be created
            # save() returns the user object
			user = form.save()
            # This User will be logged in
			login(request, user)
            # Will be Redirected to Home page showing a success message
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")

	form = NewUserForm()
	return render (request, "Authentication/register.html", context={"form":form})

def loginView(request):
	if request.method == "POST":
        # Get Prepared Django Login Form and fill it with user's data coming from POST request
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
            # Validate username and password (user credentials)
			user = authenticate(username=username, password=password)
            # If the user is authenticated
			if user is not None:
                # This User will be logged in and will be 
				login(request, user)
                # Will be Redirected to Home page showing a success message
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "Authentication/login.html", context={"form":form})

def logoutRequest(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("login")