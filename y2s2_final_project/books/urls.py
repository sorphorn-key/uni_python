from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.Usersignup, name="Usersignup"),
    path("user_login/", views.User_login, name="User_login"),
    path("logout/", views.Logout, name="Logout"),
    
#     For admin
    path("all_books/", views.Admin, name="Admin"),
    path("customers_list/", views.customers_list, name="customers_list"),
    path("add_books/", views.Add_Books, name="add_new_books"),
    path("all_books/delete_<int:myid>/", views.Delete_Books, name="delete_book"),
    path("see_requested_books/", views.see_requested_books, name="see_requested_books"),
    path("delete_requested_books/delete_<int:myid>/", views.delete_requested_books, name="delete_requested_books"),
    path("customers_list/orders_<int:myid>/", views.orders_list, name="orders_list"),
    path("customers_list/orders_<int:myid>/data/", views.data_view, name="data"),
 
    
#     For customers
    path("for_users/", views.Users, name="Users"),
    path("request_books/", views.request_books, name="request_books"),   
    path("checkout/", views.checkout, name="checkout"),    
]
