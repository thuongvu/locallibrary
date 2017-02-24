from django.db import models

# Create your models here.

class Genre(models.Model):
	"""
	Model representing a book genre e.g. science fiction, non fiction
	"""
	name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science fiction, non fiction, etc)")

	def __str__(self):
		return self.name


class Language(models.Model):
	"""
	Model representing a Language (e.g. English, French, Japanese, etc.)
	"""
	name = models.CharField(max_length=200, help_text="Enter a book's natural langauge, e.g. english, french, etc")

	def __str__(self):
		return self.name


from django.urls import reverse

class Book(models.Model):
	"""
	Model representing a book (but not a specific copy of a book).
	"""
	title = models.CharField(max_length=200)
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	# Foreign key used becausxe book can only have one author, but authors can have multiple books
	# Author as a string rather than an object because it hasn't declared yet in the file
	# null=True allows the DB to store a Null value if is no author is selected
	# on_delete models.SET_NULL will set the value of the author to Null if the associated author record is deleted
	summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
	isbn = models.CharField('ISBN', max_length=13, help_text='13 character')
	genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
	# ManyToManyField used because genre can contain many books. Books can cover many genres.
	# Genre class has already been defined so we can specify the object above.
	language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('book-detail', args=[str(self.id)])

	def display_genre(self):
		"""
		Creates a string for the Genre. This is required to display genre in Admin.
		"""
		return ', '.join([ genre.name for genre in self.genre.all()[:3] ])

	display_genre.short_description = 'Genre'


import uuid

class BookInstance(models.Model):
	"""
	Model representing a specific copy of a book (i.e. that can be borrowed from the library).
	"""

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id for this particular book")
	# UUIDField is used for the id field to set it as the primary_key for the model. this type of fields allocates a globally unique value for each instance
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)
	# due_back can be blank or null, which is needed when the book is available

	LOAN_STATUS = (
		('d', 'Maintenance'),
		('o', 'On Loan'),
		('a', 'Available'),
		('r', 'Reserved'),
	)	

	status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book availability')

	class Meta:
		ordering = ['due_back']

	def __str__(self):
		return '{} ({})'.format(self.id, self.book.title)


class Author(models.Model):
	"""
	Model representing an author.
	"""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField('Died', null=True, blank=True)

	def get_absolute_url(self):
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		return '{}, {}'.format(self.last_name, self.first_name)


# You can use models to represent selection-list options e.g. dropdown, rather than hard-coding the choices
# This is useful when the options aren't known up front or may change