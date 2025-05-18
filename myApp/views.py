from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey



class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        
    def __str__(self):
        return self.title
    
    
class Comment(MPTTModel):
    body = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    like = models.IntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['created_at']
   
    class Meta:
        ordering = ['-like']
        indexes = [
            models.Index(fields=['like'])
        ]

    
    def __str__(self):
        return f"{self.user.username}: {self.body[:20]}"



class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"