import datetime
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

from catalog.models import Book, Author, BookInstance, Genre

from django.views import generic

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm, BorrowBookForm

class AuthorSearchResultsView(generic.ListView):
    model = Author
    template_name = 'catalog/author_search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('author_query')
        object_list = Author.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
        return object_list

class BookSearchResultsView(generic.ListView):
    model = Book
    template_name = 'catalog/book_search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('book_query')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        )
        return object_list
    
# class BookInstanceSearchResultsView(generic.ListView):
#     model = BookInstance
#     template_name = 'catalog/book_instance_search_results.html'

#     def get_queryset(self): # new
#         query = self.request.GET.get('book_instance_query')
#         object_list = BookInstance.objects.filter(
#             Q(book__icontains = query) | Q(language__icontains=query)
#         )
#         return object_list

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class BookInstanceListView(generic.ListView):
    model = BookInstance

def index(request):
    """View function for home page of site."""

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
     
    num_authors = Author.objects.count()

    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request:
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed-books') )

    # If this is a GET method, create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

def borrow_book_instance(request, pk):
    # This method functions almost exactly like the renew method. Explanations for the different parts are described in the renew method
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = BorrowBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['borrow_date']
            book_instance.borrower = request.user
            book_instance.status = 'o'
            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed-books') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/borrow_book.html', context)