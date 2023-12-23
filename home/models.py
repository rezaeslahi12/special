from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from unidecode import unidecode
from django.utils.text import slugify

class Post (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    body = models.TextField()
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(upload_to='%Y/%m/%d',blank=True , null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.slug} {self.updated} "

    def get_absolute_url(self):
        return reverse('home:PostDetail',kwargs={"id": self.id, "slug": self.slug})

    def post_like_count(self):
        return self.pvote.count()

    def post_can_like(self,user):
        user_like = user.uvote.filter(post=self)
        if user_like.exists():
            return True
        else:
            return False

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(unidecode(self.body))
    #     super().save(*args, **kwargs)
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ucomment')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pcomment')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='rcomments' ,blank=True , null= True)
    body = models.TextField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} to {self.body}"

class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uvote')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pvote')
    def __str__(self):
        return f"{self.user} Like {self.post}"
