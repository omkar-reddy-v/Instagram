from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from . models import instasignup,photos,Videos
from . models import Fbsignup
from django.contrib.auth.models import User
from datetime import date

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def signin(request):
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            userdata = authenticate(username = username , password = password)
            if userdata is not None:
                login(request,userdata)
                return render(request,'instagram/acdetails/home.html')
            else:
                 messages.error(request,"Userdata Not Found ?")
        return render(request,'instagram/login.html')

def forgotpass(request):
    # This view is still in process
    return render(request,'instagram/forgotpass.html')



def signup(request):

    if request.method=="POST":
        mobile = request.POST.get("number")
        fullname = request.POST.get("fullname")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmpass = request.POST.get('confirmpass')
        image = request.FILES.get('image')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        # To check the when user given password and confirmpassword is same or not 
        if password != confirmpass:
            messages.warning(request,"Password does not match")
            return redirect('signup')
        
        if password == confirmpass:        
            user = User.objects.create_user(
                    username=username,
                    password=password
                )
            instasignup.objects.create(
                    mobile = mobile,
                    fullname = fullname,
                    image = image,
                    uid_id = user.id
                )
            return redirect("insta")        
    return render(request,'instagram/signup.html')


def signout(request):
    logout(request)
    return redirect('insta')



@login_required(login_url='insta')
def home(request):
    if request.user.is_authenticated:
        video_s = Videos.objects.all()

        # Check if the user exists in the instasignup table
        try:
            userdata = instasignup.objects.get(uid_id=request.user.id)
            profile_type = "Instagram"
        except instasignup.DoesNotExist:
            # If the user does not exist in the instasignup table, check Fbsignup table
            try:
                userdata = Fbsignup.objects.get(fbuid=request.user)
                profile_type = "Facebook"
            except Fbsignup.DoesNotExist:
                # Handle the case if the user doesn't exist in either table
                return Http404('User Data Not Found ?...')
        
        return render(request, 'instagram/acdetails/home.html', {'userdata': userdata, 'profile_type': profile_type,'videos':video_s})
    else:
        return render(request, 'instagram/login.html')  # Render login page if user is not authenticated


@login_required(login_url='insta')
def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            # Search for users by username
            users = User.objects.filter(username=query)
            return render(request, "instagram/acdetails/search.html", {'users': users, 'query': query})
        else:
            return render(request, "instagram/acdetails/search.html", {'users': None})
    else:
        return render(request, "instagram/acdetails/search.html", {'users': None})
    
@login_required(login_url='insta')
def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        try:
            userdata = instasignup.objects.get(uid_id=user.id)
        except instasignup.DoesNotExist:
            try:
                userdata = Fbsignup.objects.get(fbuid=user)
            except Fbsignup.DoesNotExist:
                return Http404('User Data Not Found')
            
         # Retrieve photos and videos associated with the user
        photo_s = photos.objects.filter(photoid=user)
        video_s = Videos.objects.filter(videoid=user)
        return render(request, 'instagram/acdetails/user_profile.html', {'userdata': userdata,'photos':photo_s,'videos':video_s})
    except User.DoesNotExist:
        return Http404('User Not Found')
    

@login_required(login_url='insta')
def profile(request):
    if request.user.is_authenticated:
        # Check if the user exists in the instasignup table
        try:
            userdata = instasignup.objects.get(uid_id=request.user.id)
            profile_type = "Instagram"
        except instasignup.DoesNotExist:
            # If the user does not exist in the instasignup table, check Fbsignup table
            try:
                userdata = Fbsignup.objects.get(fbuid=request.user)
                profile_type = "Facebook"
            except Fbsignup.DoesNotExist:
                # Handle the case if the user doesn't exist in either table
                return Http404('User Data Not Found') 

        # Retrieve photos and videos associated with the user
        photo_s = photos.objects.filter(photoid=request.user)
        video_s = Videos.objects.filter(videoid=request.user)

        return render(request, 'instagram/acdetails/profile.html', {'userdata': userdata, 'profile_type': profile_type, 'photos': photo_s, 'videos': video_s})
    else:
        return render(request, 'login.html')  # Redirect to login page if user is not authenticated
    

@login_required(login_url='insta')
def reels(request):
    video_s = Videos.objects.all()
    return render(request,'instagram/acdetails/reels.html',{'videos':video_s})

@login_required(login_url='insta')
def more(request):
     return render(request,'instagram/acdetails/more.html')

@login_required(login_url='insta')
def create(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        user = request.user

        if image:  # Check if an image was uploaded
            photos.objects.create(
                image=image,
                photoid=user
            )
            messages.success(request, "Photo uploaded successfully.")
            return redirect('create')
        elif video:  # Check if a video was uploaded
            Videos.objects.create(
                video=video,
                videoid=user
            )
            messages.success(request, "Video uploaded successfully.")
            return redirect('create')
        else:
            return render(request, 'error_page.html', {'message': 'No media uploaded.'})

    return render(request, 'instagram/acdetails/create.html')

@login_required(login_url='insta')
def settings(request):
    if request.user.is_authenticated:
        try:
            userdata = instasignup.objects.get(uid_id=request.user.id)
            if request.method == "POST":
                fullname = request.POST.get('fullname')
                image =  request.FILES.get('image')
                userdata.fullname=fullname  
                userdata.image=image
                userdata.save()
        except instasignup.DoesNotExist:
            # If the user does not exist in the instasignup table, check Fbsignup table
            try:
                userdata = Fbsignup.objects.get(fbuid=request.user)
                if request.method == "POST":
                    fullname = request.POST.get('fullname')
                    image =  request.FILES.get('image')
                    userdata.fullname=fullname  
                    userdata.image=image
                    userdata.save()
            except Fbsignup.DoesNotExist:
                return render(request, 'login.html', {'message': 'User profile not found.'})
    return render(request,'instagram/acdetails/settings.html',{'userdata':userdata})
        
     





# This Views are used for Facebook


def fb(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userdata = authenticate(username = username , password = password)
        if userdata is not None:
            login(request,userdata)
            return render(request,'instagram/acdetails/home.html')
        else:
             messages.error(request,"Userdata Not Found ?")
    return render(request,'facebook/fb.html')



def forgottenac(request):
    # This view is used to login when user konw the username and password 
    if request.method=='POST':
        username = request.POST.get('loginusername')
        password = request.POST.get('password')
        userdata = authenticate(username = username , password = password)
        if userdata is not None:
            login(request,userdata)
            return render(request,'instagram/acdetails/home.html')
        else:
             messages.error(request,"Userdata Not Found ?")

    # This view is used  to search the user 
    if request.method == 'POST':
        username = request.POST.get('username')
        # Check if the username exists
        try:
            user = User.objects.get(username=username)
            request.session['user_id'] = user.id  # Store user ID in session
            return redirect('login')  # Redirect to login page
        except User.DoesNotExist:
            messages.error(request, "User not found.")
    return render(request, 'facebook/forgottenac.html')


def login_view(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            user = User.objects.get(id=user_id)
            if request.method == 'POST':
                password = request.POST.get('password')
                userdata = authenticate(username=user.username, password=password)
                if userdata is not None:
                    login(request, userdata)
                    return redirect('home')
                else:
                    messages.error(request, "Incorrect password.")
            return render(request, 'facebook/login.html', {'username': user.username})
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgottenac')
    else:
        return redirect('forgottenac')


def signupforfb(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        surname = request.POST.get('surname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpass = request.POST.get('confirmpass')
        day = int(request.POST.get('date'))
        month = request.POST.get('month')
        year = int(request.POST.get('year'))
        gender = request.POST.get('gender')
        image = request.FILES.get('image')
        
        # Convert month name to month number
        month_dict = {'January': 1, 'February': 2, 'March':3,'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
        month_number = month_dict.get(month)
        # Create a date object
        dob = date(year, month_number, day)


        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signupforfb')
        
        # To check the when user given password and confirmpassword is same or not 
        if password != confirmpass:
            messages.warning(request,"Password does not match")
            return redirect('signupforfb')
        
        if password == confirmpass:        
        # Save to UserProfile instance
            user = User.objects.create_user(
                    username=username,
                    password=password
                )
            Fbsignup.objects.create(
                firstname = firstname,
                surname = surname,                   
                dob=dob,
                gender = gender,
                image=image,
                fbuid = user
            )
            return redirect("instafacebook")        
    return render(request,'facebook/signupforfb.html')
    
def alreadyfbac(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userdata = authenticate(username = username , password = password)
        if userdata is not None:
            login(request,userdata)
            return render(request,'instagram/acdetails/home.html')
        else:
             messages.error(request,"Userdata Not Found ?")
    return render(request,'facebook/alreadyfbac.html')