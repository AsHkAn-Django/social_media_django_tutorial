# Social Media Django Tutorial

Just a quick little project I made while practicing Django and backend development.  
This is part of my journey as I learn and improve my skills.

## About the Project

A mini social media platform where users can follow others, view a personalized news feed, like, and comment on posts.
This project is built using Django and includes basic frontend styling with HTML, CSS, Bootstrap, and some JavaScript.  
I usually focus on the backend side of things and try to keep things simple and clean.  
Each project I make is a way for me to learn something new or reinforce what I already know.


## Features

- comming soon


## Technologies Used

- Python
- Django
- HTML
- CSS
- Bootstrap
- JavaScript

## About Me

Hi, I'm Ashkan — a junior Django developer who recently transitioned from teaching English as a second language to learning backend development.  
I’m currently focused on improving my skills, building projects, and looking for opportunities to work as a backend developer.  
You can find more of my work here: [My GitHub](https://github.com/AsHkAn-Django)

## How to Use

1. Clone the repository  
   `git clone https://github.com/AsHkAn-Django/social_media_django_tutorial.git`
2. Navigate into the folder  
   `cd social_media_django_tutorial`
3. Create a virtual environment and activate it
4. Install the dependencies  
   `pip install -r requirements.txt`
5. Run the server  
   `python manage.py runserver`

## Tutorial (if any)

### Nested Comments With django-mttp

1. install django-mpttp
```shell
pip install django-mptt
```

2. Add to INSTALLED_APPS in your settings.py:
```python
INSTALLED_APPS = [
    # … other built-in apps …
    'mptt',                # django-mptt
    'myApp',               # your app containing Comment
]
```

3. Create models.py in myApp/ and define:
```python
from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
class Comment(MPTTModel):
    body = models.CharField(max_length=150)
    user = models.ForeignKey(
                   settings.AUTH_USER_MODEL,
                   related_name="user_comments",
                   on_delete=models.CASCADE
                 )
    post = models.ForeignKey(
                   'myApp.Post',
                   related_name="post_comments",
                   on_delete=models.CASCADE
                 )
    created_at = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey(
                   'self',
                   on_delete=models.CASCADE,
                   null=True,
                   blank=True,
                   related_name='children'
                 )

    class MPTTMeta:
        order_insertion_by = ['created_at']

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return f"{self.user.username}: {self.body[:20]}…"
```

4. Generate and apply migrations to add your Comment table with the MPTT fields:
```shell
python manage.py makemigrations myApp
python manage.py migrate
```

5. In myApp/admin.py, use the MPTT-aware admin class:
```python
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display      = ('body', 'user', 'created_at', 'parent')
    mptt_level_indent = 20  # pixels per level indent
```

6. In myApp/forms.py, define a ModelForm that carries a hidden ```parent_id```
```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model  = Comment
        fields = ['body', 'parent_id']
```

7. In myApp/views.py, add the comment-saving logic:
```python 
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            parent_id = form.cleaned_data.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(pk=parent_id)
            comment.save()
            return redirect('myApp:post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'myApp/post_detail.html', {
        'post': post,
        'form': form,
    })
```

8. Rendering Comments in Templates
```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% load mptt_tags %}
 <!-- Load the MPTT template tags, including `recursetree` for nested trees -->

{% block content %}
<div class="container mt-5">

  <!-- Post Details -->
  {# You’d render title/body/date/author here before comments… #}

  <!-- Comments -->
  <h4>Comments ({{ post.post_comments.count }})</h4>
  {% if post.post_comments.exists %}
    <ul class="list-group">
      {% recursetree post.post_comments.all %}
      <li class="list-group-item">
        <div class="comment">
          <strong>{{ node.user.username }}</strong>
          <small class="text-muted">at {{ node.created_at }}</small>
          <p>{{ node.body }}</p>
        </div>
        <a href="#" class="reply-link" data-comment-id="{{ node.id }}">Reply</a>
        <div id="reply-form-{{ node.id }}" style="display:none; margin-top:1rem;">
          <form method="post" action="{% url 'myApp:add_comment' post.pk %}">
            {% csrf_token %}
            <input type="hidden" name="parent_id" value="{{ node.id }}">
            {% bootstrap_field form.body %}
            <button type="submit" class="btn btn-sm btn-primary">Post Reply</button>
          </form>
        </div>
        {% if not node.is_leaf_node %}
          <ul class="list-group ml-4">
            {{ children }}
          </ul>
        {% endif %}
      </li>
      {% endrecursetree %}
    </ul>
  {% else %}
    <p>No comments yet.</p>
  {% endif %}

  <!-- Top-level comment form -->
  <div class="mt-4">
    <h5>Leave a Comment</h5>
    <form method="post" action="{% url 'myApp:add_comment' post.pk %}">
      {% csrf_token %}
      <input type="hidden" name="parent_id">
      {% bootstrap_field form.body %}
      <button type="submit" class="btn btn-primary">Post Comment</button>
    </form>
  </div>

<script>
// Simple JS to toggle reply forms
document.querySelectorAll('.reply-link').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const id = link.getAttribute('data-comment-id');
    const container = document.getElementById(`reply-form-${id}`);
    container.style.display = container.style.display === 'none' ? 'block' : 'none';
  });
});
</script>
```