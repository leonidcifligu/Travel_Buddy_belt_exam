from django.db import models
import re
import dateutil.parser
import datetime
import bcrypt


# User Validations

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if 'name' not in postData or len(postData['name']) < 3:
            errors['name'] = "Name can't be shorter than 3 characters!"
        if 'username' not in postData or len(postData['username']) < 3:
            errors['username'] = "Username can't be shorter than 3 characters!"
        username_usage = self.filter(username=postData['username'])
        if username_usage:
            errors['username'] = "Username already exists!"
        
        if 'password' not in postData or len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters!"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "The passwords do not match!"
        return errors

    def authenticate(self, username, password):
        users = self.filter(username=username)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, postData):
        pw = bcrypt.hashpw(
            postData['password'].encode(), bcrypt.gensalt()).decode()

        return self.create(
            name=postData['name'],
            username=postData['username'],
            password=pw
        )

# Travel Validations


class TravelManager(models.Manager):
    def travel_validator(self, postData):
        errors = {}
        if 'destination' not in postData or len(postData['destination']) < 1:
            errors['destination'] = "Destination should be at least 1 character!"
        if 'desc' not in postData or len(postData['desc']) < 1:
            errors['desc'] = "Description should be at least 1 character!"
        if 'start_date' not in postData or len(postData['start_date']) < 1:
            errors['start_date'] = "Start Date should be at least 1 character!"
        if 'end_date' not in postData or len(postData['end_date']) < 1:
            errors['end_date'] = "End Date should be at least 1 character!"
        if 'start_date' in postData and len(postData['start_date']) > 1:
            start_date = dateutil.parser.parse(postData['start_date'])
            end_date = dateutil.parser.parse(postData['end_date'])
            if start_date < datetime.datetime.today():
                errors['start_date'] = 'Start date should be in the future'
            if start_date > end_date:
                errors['end_date'] = 'Start date can not be ahead of the end date'
        return errors


class User(models.Model):
    name = models.CharField(max_length=225)
    username = models.CharField(max_length=225)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Travel(models.Model):
    destination = models.CharField(max_length=225)
    desc = models.TextField()
    creator = models.ForeignKey(
        User, related_name="travels_uploaded", on_delete=models.CASCADE)
    traveler = models.ManyToManyField(User, related_name="added_travels")
    start_date = models.DateField(max_length=10)
    end_date = models.DateField(max_length=10)
    objects = TravelManager()
