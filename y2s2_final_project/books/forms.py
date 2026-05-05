from django import forms
from .models import Book, Request_Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        
        
class RequestBookForm(forms.ModelForm):
    class Meta:
        model = Request_Book
        fields = ('book_name', 'author')
        