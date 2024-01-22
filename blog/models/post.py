#!/usr/bin/env python3
"""
Post model
"""

from blog.models.base_model import BaseModel, models
from blog.models.user import MainUser as User


def project_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project_images/<project_id>/<filename>
    return f'project_images/{instance.id}/{filename}'


class BlogPost(BaseModel):
    """
    Post model class
    columns:
    - title: title of the post
    content: content of the post
    sub_title: subtitle of the post
    author: author of the post
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, db_column='user_id')
    project_picture = models.ImageField(blank=True, upload_to=project_image_path)

    class Meta:
        db_table = 'blog_posts'
