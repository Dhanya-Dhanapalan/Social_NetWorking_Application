from django.db import models
from django.contrib.auth.models import User


gender_choices=[('Female','Female'),('Male','Male'),('Others','Others')]


class Posts(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name="likes")

    @property
    def post_comments(self):
        return self.comments_set.all()

    @property
    def like_count(self):
        return self.like.all().count()


    def __str__(self):
        return self.title

class Comments(models.Model):
    comment=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Details(models.Model):
    profile_img=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    work=models.CharField(max_length=200)
    hobby=models.CharField(max_length=200)
    gender=models.CharField(max_length=200,choices=gender_choices,default='Female')





