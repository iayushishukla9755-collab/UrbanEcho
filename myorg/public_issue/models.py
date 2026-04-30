from django.db import models

# User / Citizen Table
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=100)   # Added password here
    city = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user_name


# Issue Table
class Issue(models.Model):
    issue_id = models.CharField(max_length=100, primary_key=True)
    issue_type = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_id')
    description = models.TextField()
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=30)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    issue_img = models.ImageField(upload_to = 'issue/', null=True, blank=True)

    def __str__(self):
        return self.issue_id


# Rating Table
class Rating(models.Model):
    rating_id = models.CharField(max_length=100, primary_key=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    rating_value = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.rating_id