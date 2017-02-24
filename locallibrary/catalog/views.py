from django.shortcuts import render

from .models import Book, Author, BookInstance, Genre

def index(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count() # The 'all()' is implied by default

	# Number of visits to this view, as counted in the session variable
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	return render(
		request,
		'index.html',
		context={
			'num_books':num_books,
			'num_instances':num_instances,
			'num_instances_available':num_instances_available,
			'num_authors':num_authors,
			'num_visits': num_visits
		},
	)

from django.views import generic

class BookListView(generic.ListView):
	model = Book
	paginate_by = 2


class BookDetailView(generic.DetailView):
	model = Book

# What the BookDetailView would be like if you implemented it as a function:
# def book_detail_view(request, pk):
# 	try:
# 		book_id = Book.objects.get(pk=pk)
# 	except Book.DoesNotExist:
# 		raise Http404('Book does not exist')

# 	# book_id=get_object_or_404(Book, pk=pk)

# 	return render(
# 		request,
# 		'catalog/book_detail.html',
# 		context={'book': book_id}
# 	)
