from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .tasks import process_payment_task

# Create your views here.


def user_login(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        user= authenticate(request, email=email, password=password)
    
        if user is not None:
            login(request, user)
            return redirect("home")
                
        else:
            error_message= "Invalid Username or Password"
            return render(request, "login.html", {"error_message":error_message})
    return render(request, "login.html")



@login_required(login_url='/login/')
def home(request):
    context = {}
    if request.method == 'POST':
        pi_amount = request.POST['amount']
        seed = request.POST['seed']
        destination = request.POST['destination']

        while True: 
            process_payment_task(pi_amount, seed, destination)

    return render(request, 'index.html', context)
