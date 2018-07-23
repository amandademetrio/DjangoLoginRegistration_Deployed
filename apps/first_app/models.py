from django.db import models
import re
from django.contrib import messages
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        #Checking for length
        if len(postData['first_name']) < 2:
            errors['first_name_len'] = "First name should have at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name_len'] = "Last name should have at least 2 characters"
        if len(postData['email']) < 2:
            errors['email_len'] = "Email should have at least 2 characters"
        if len(postData['password']) < 2:
            errors['password_len'] = "Password should have at least 2 characters"
        #Making sure names are only letters
        if not postData['first_name'].isalpha():
            errors['first_name_alpha'] = "First name must contain only letters"
        if not postData['last_name'].isalpha():
            errors['last_name_alpha'] = "Last name must contain only letters"
        #Making sure email matches format
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Invalid email format"
        #Making sure email isn't already in the list
        if User.objects.filter(email=postData['email']):
            errors['already_registered'] = "Email is already in the database"
        #Making sure both passwords match
        if postData['password'] != postData['confirm_password']:
            errors['password_match'] = "Both passwords need to match"
        return errors
    
    def login_validator(self,postData):
        errors = {}
        #Checking length
        if len(postData['email']) < 2:
            errors['email_len_login'] = "Email should have at least 2 characters"
        if len(postData['password']) < 2:
            errors['password_len_login'] = "Password should have at least 2 characters"
        #Checking email format
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format_login'] = "Invalid email format"
        #Checking if email is in the database
        if not User.objects.filter(email=postData['email']):
            errors['email_db_check'] = "Invalid credentials"
        else:
            log_user = User.objects.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), log_user.password.encode()):
                errors['pw_db_check'] = "Invalid credentials"
        return errors
    
    def update_validator(self,postData):
        errors = {}
        #Checking length
        if len(postData['new_first_name']) < 1:
            errors['new_first_name_len'] = "First name cannot be empty"
        if len(postData['new_last_name']) < 2:
            errors['new_last_name_len'] = "Last name cannot be empty"
        if len(postData['new_email']) < 2:
            errors['new_email_len'] = "Email cannot be empty"
        #Checking email format
        if not EMAIL_REGEX.match(postData['new_email']):
            errors['email_format_update'] = "Invalid email format"
        #Checking if email is in the database
        if User.objects.filter(email=postData['new_email']):
            errors['email_db_check'] = "This email is already in our database"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class AuthorManager(models.Manager):
    def author_validator(self,postData):
        errors = {}
        #Checking for length
        if len(postData['author']) < 3:
            errors['author_name_len'] = "Author name must be at least 3 characters long"
        return errors

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AuthorManager()

class QuoteManager(models.Manager):
    def quote_validator(self,postData):
        errors = {}
        #Checking for length
        if len(postData['quote']) < 10:
            errors['quote_len'] = "Quote must be at least 10 characters long"
        return errors

class Quote(models.Model):
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    posted_by = models.ForeignKey(User, related_name="posted_quotes")
    said_by = models.ForeignKey(Author, related_name="said_quotes")
    objects = QuoteManager()

class Like(models.Model):
    liked_message = models.ForeignKey(Quote, related_name="likes")
    liker = models.ForeignKey(User, related_name="liked_messages")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)