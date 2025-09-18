from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login_view(request):
    if(request.method =='POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html',{'error': 'Invalid cred'})
        
    return render(request, 'login.html')
    # return render(request, 'home.html')

def signup_view(request):
    if request.method ==  'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error':'username already exits'})
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')

def home_view(request):
    user = request.user
    return render(request, 'home.html', {'user':user})

@login_required
def edit_profile_view(request):
   if request.method == "POST":
       user = request.user
       profile = user.profile

       email = request.POST.get("email")
       bio = request.POST.get("bio")
       avatar = request.FILES.get("avatar")

       if email:
           user.email = email
           user.save()
        
       if bio is not None:
           profile.bio = bio

       if avatar:
           profile.avatar = avatar
       profile.save()

       return redirect("home")
   return render(request, "myapp/home.html", {"user":user})

def start_quiz_view(request):
    return render(request, "quiz.html")

def logout_view(request):
    logout(request)
    return redirect('login')