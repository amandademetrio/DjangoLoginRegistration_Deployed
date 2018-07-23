from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import *
from django.contrib import messages

def index(request):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'quotes':Quote.objects.all(),
            'user':User.objects.get(id=request.session['user_id']),
            'likes':Like.objects.all()
        }
        return render(request,'first_app/success.html',context)
    else:
        return render(request,'first_app/index.html')

def loaduser(request,number):
    if 'logged_in' in request.session and 'user_id' in request.session:
        context = {
            'user':User.objects.get(id=number),
            'quotes':Quote.objects.filter(posted_by=number)
        }
        print(context)
        return render(request,'first_app/userprofile.html',context)
    else:
        return redirect('/')

def loadedituser(request,number):
    context = {
        'user_info':User.objects.get(id=number)
    }
    return render(request,'first_app/editaccount.html',context)

def registration(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags='registration_errors')
        return redirect('/')
    
    else:
        new_user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        new_user.save()
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        request.session['email'] = new_user.email
        request.session['logged_in'] = True
        request.session['user_id'] = new_user.id
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    
    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags='login_errors')
        return redirect('/')
    
    else:
        login_user = User.objects.get(email=request.POST['email'])
        request.session['logged_in'] = True
        request.session['first_name'] = login_user.first_name
        request.session['user_id'] = login_user.id
        return redirect('/')

def addquote(request):
    author_errors = Author.objects.author_validator(request.POST)

    quote_errors = Quote.objects.quote_validator(request.POST)

    if len(author_errors) or len(quote_errors):
        for key,value in author_errors.items():
            messages.error(request,value,extra_tags='author_errors')

        for key,value in quote_errors.items():
            messages.error(request,value,extra_tags='quote_errors')
        return redirect('/')
    else:
        #create the author
        author = Author.objects.create(name=request.POST['author'])
        #get user object
        current_user = User.objects.get(id=request.session['user_id'])
        #create a new quote     
        new_quote = Quote.objects.create(quote=request.POST['quote'],posted_by=current_user,said_by=author)
        return redirect('/')

def edituser(request):
    current_user_id = request.POST['user_id']
    print(current_user_id)
    errors = User.objects.update_validator(request.POST)

    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags='update_errors')
        return redirect(loadedituser,number=current_user_id)
    else:
        user_info = User.objects.get(id=current_user_id)
        user_info.first_name = request.POST['new_first_name']
        user_info.last_name = request.POST['new_last_name']
        user_info.email = request.POST['new_email']
        user_info.save()
        return redirect('/')

def createlike(request):
    if Like.objects.filter(liked_message=request.POST['quote_id']) and Like.objects.filter(liker=request.session['user_id']):
        messages.error(request,"You're not allowed to like a post more than once",extra_tags="like_error")
        return redirect("/")

    else:
        quote = Quote.objects.get(id=request.POST['quote_id'])
        current_user = User.objects.get(id=request.session['user_id'])
        new_like = Like.objects.create(liked_message=quote,liker=current_user)
        new_like.save()
        return redirect('/')

def deletequote(request,number):
    quote_to_delete = Quote.objects.get(id=number)
    quote_to_delete.delete()
    return redirect('/')