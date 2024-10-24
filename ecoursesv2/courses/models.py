from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    
class ItemBase(models.Model):
    #khi migrate and makemigrations thi khong tao bang nay
    #chi la cai chung de cac class khac ke thua
    class Meta:
        abstract = True
        
    subject = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='courses/%y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.subject
    
class Category(ItemBase):
    name = models.CharField(max_length=100, null=False, unique=True)
    
    def __str__(self):
        return self.name
    
class Course(ItemBase):
    class Meta:
        unique_together = ('subject', 'category')       #khong trung subject and category
        ordering = ['-id']      #giam theo id
        
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
class Lesson(ItemBase):
    class Meta:
        unique_together = ('subject', 'course')
        
    content = models.TextField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='lessons', blank=True)
    
class Comment(models.Model):
    content = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class ActionBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
        
class Action(ActionBase):
    LIKE, HAHA, HEART = range(3)
    ACTIONS = [
        (LIKE, 'like'),
        (HAHA, 'haha'),
        (HEART, 'heart')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)
    
class Rating(ActionBase):
    rate = models.PositiveSmallIntegerField(default=0)
    
class LessonView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    
class MemberView(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.name