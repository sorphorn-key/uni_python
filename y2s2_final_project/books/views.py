from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .decorators import restricted_login, admin_or_user
from .forms import BookForm, RequestBookForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def index(request):
    return render(request, "index.html")

def Usersignup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=="POST":   
            username = request.POST['username']
            email = request.POST['email']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if len(username) > 15:
                messages.info(request, "Username must be under 15 characters.")
                return redirect('/signup')
            if not username.isalnum():
                messages.info(request, "Username must contain only letters and numbers.")
                return redirect('/signup')
            if password1 != password2:
                messages.info(request, "Passwords do not match.")
                return redirect('/signup')

            user = User.objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return render(request, 'user_login.html')     
    return render(request, "signup.html")


def User_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=="POST":
            user_username = request.POST['user_username']
            user_password = request.POST['user_password']

            user = authenticate(username=user_username, password=user_password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect("/for_users")
            else:
                messages.error(request, "Please provide a valid username and password")
    return render(request, "user_login.html")

def Logout(request):
    logout(request)
    thank = True
    return render(request, "index.html", {'thank':thank})

@admin_or_user
def Admin(request):
    books = Book.objects.all()
    total_books = books.count()
    return render (request, "for_admin.html", {'books':books, 'total_books':total_books})

def Delete_Books(request, myid):
    books = Book.objects.get(id=myid)
    if request.method == "POST":
        books.delete()
        return redirect('/all_books')
    return render(request, 'delete_book.html', {'books':books})

@login_required(login_url = '/user_login')
def Users(request):
    books = Book.objects.all()
    total_books = books.count()
    return render (request, "for_user.html", {'books':books, 'total_books':total_books})

def Add_Books(request):
    if request.method=="POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "add_books.html")
    else:
        form=BookForm()
    return render(request, "add_books.html", {'form':form})

def request_books(request):
    if request.method=="POST":
        user = request.user
        book_name = request.POST['book_name']
        author = request.POST['author']
        book = Request_Book(user=user, book_name=book_name, author=author)
        book.save()
        thank = True
        return render(request, "request_books.html", {'thank':thank})
    return render(request, "request_books.html")

def see_requested_books(request):
    requested_book = Request_Book.objects.all()
    requested_books_count = requested_book.count()
    return render(request, "see_requested_books.html", {'requested_book':requested_book, 'requested_books_count':requested_books_count})

def delete_requested_books(request, myid):
    delete_book = Request_Book.objects.get(id=myid)
    if request.method == "POST":
        delete_book.delete()
        return redirect('/see_requested_books')
    return render(request, "delete_requested_books.html", {'delete_book':delete_book})

def customers_list(request):
    customers = Order.objects.all()
    customer_count = customers.count()
    return render(request, "customers_list.html", {'customers':customers, 'customer_count':customer_count})

def orders_list(request, myid):
    customer = Order.objects.filter(id=myid)
    return render(request, "orders_list.html", {'customer':customer})

def data_view(request, myid):
    orders = Order.objects.get(id=myid)
    return JsonResponse({'data':orders.items_json})


def checkout(request):
    if request.method=="POST":
        user = request.user
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        price = request.POST.get('price', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        order = Order(user=user, items_json=items_json, name=name, email=email, address=address, phone=phone, price=price)
        order.save()
        thank = True
        return render(request, 'mycart.html', {'thank':thank})
    return render(request, "mycart.html")




