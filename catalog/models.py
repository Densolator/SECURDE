import uuid
from datetime import date
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser


# class RegisteredUser(AbstractBaseUser):
# 	email = models.EmailField(
# 		verbose_name='email address',
# 		max_length=255,
# 		unique=True,
# 	)
# 	id_number = models.IntegerField(null=True)
# 	active = models.BooleanField(default=True)
# 	staff = models.BooleanField(default=False) # a admin user; non super-user
# 	admin = models.BooleanField(default=False) # a superuser
#     # notice thef absence of a "Password field", that is built in.

# 	USERNAME_FIELD = 'email'
# 	REQUIRED_FIELDS = ['first_name','last_name','id_number'] # Email & Password are required by default.

# 	def __str__(self):              # __unicode__ on Python 2
# 		return self.email

# 	def has_perm(self, perm, obj=None):
# 		"Does the user have a specific permission?"
# 		# Simplest possible answer: Yes, always
# 		return True

# 	def has_module_perms(self, app_label):
# 		"Does the user have permissions to view the app `app_label`?"
# 		# Simplest possible answer: Yes, always
# 		return True

# 	@property
# 	def is_staff(self):
# 		"Is the user a member of staff?"
# 		return self.staff

# 	@property
# 	def is_admin(self):
# 		"Is the user a admin member?"
# 		return self.admin

# 	@property
# 	def is_active(self):
# 		"Is the user active?"
# 		return self.active

# Create your models here.
class UserIDNumber(models.Model):
	id_number = models.IntegerField(null = True, blank = True)
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		"""String for representing the Model object"""
		return str(self.id_number)


class Genre(models.Model):
	"""Model representing a book genre."""
	name = models.CharField(max_length=200, help_text = 'Enter a book genre(e.g. Science Fiction)')
	
	def __str__(self):
		"""String for representing the Model object"""
		return self.name

class Book(models.Model):
	"""Model representing a book (but not a specific copy of a book)."""
	title = models.CharField(max_length=200)
	
	# Foreign Key used because book can only have one author, but authors can have multiple books
	# Author as a string rather than object because it hasn't been delcared yet in the file
	author = models.ForeignKey('Author', on_delete = models.SET_NULL, null= True)
	publisher = models.CharField(max_length = 50, null = True)
	publication_year = models.DateField(blank = True, null = True)
	summary = models.TextField(max_length = 1000, help_text = 'Enter a brief description of the book')
	isbn = models.CharField('ISBN', max_length = 13, help_text = 'Select a genre for this book')
	genre = models.ManyToManyField(Genre, help_text = 'Select a Genre for this book')

	def __str__(self):
		"""String for representing the Model object."""
		return self.title

	def get_absolute_url(self):
        # "Returns the url to access a detail record for this book."
		return reverse('book-detail', args=[str(self.id)])

class Language(models.Model):
	"""Model representing a book instance"""
	name = models.CharField(max_length = 100)
	
		
	def __str__(self):
		"""String for representing the Model object."""
		return f'{self.name}'
		
class BookInstance(models.Model):
	"""Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
	id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text = 'Unique ID')
	book = models.ForeignKey('Book', on_delete = models.SET_NULL, null = True)
	imprint = models.CharField(max_length = 200)
	due_back = models.DateField(null=True, blank = True)
	language = models.ManyToManyField(Language, help_text = 'Select a language for this book instance')
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	
	LOAN_STATUS = (
		('m', 'Maintenance'),
		('o', 'On Loan'),
		('a', 'Available'),
		('r', 'Reserved'),
	)
	
	status = models.CharField(
		max_length = 1,
		choices = LOAN_STATUS,
		blank = True,
		default = 'm',
		help_text = 'Book Availability',
	)
	
	

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		return False

	class Meta:
		ordering = ['due_back']
		permissions = (("can_mark_returned", "Set book as returned"),)
		
	def book_language(self):
		return "\n".join([str(p) for p in self.language.all()])

	def __str__(self):
		"""String for representing the Model object."""
		return f'{self.id} ({self.book.title})'
		
class Author(models.Model):
	"""Model representing an author"""
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	date_of_birth = models.DateField(null = True, blank = True)
	date_of_death = models.DateField('Died', null = True, blank = True)
	
	class Meta:
		ordering = ['last_name', 'first_name']

	def __str__(self):
		"""String for representing the Model object."""
		return f'{self.last_name}, {self.first_name}'
	def get_absolute_url(self):
		return reverse('author-detail', args = [str(self.id)])

class BookReview(models.Model):
	"""Model representing the review left by a user for a certain book."""
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	book = models.ForeignKey(Book, on_delete = models.SET_NULL, null = True, blank = True)
	content = models.TextField(max_length=500)


	def __str__(self):
		return f'Review by {self.user} for {self.book}'
