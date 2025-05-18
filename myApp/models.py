from django.db import models
from django.conf import settings


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
    
    class Meta:
        ordering = ['-like']
        indexes = [
            models.Index(fields=['like'])
        ]

    
    class MPTTMeta:
        order_insetion_by = ['created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.body[:20]}"
    
    



class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"