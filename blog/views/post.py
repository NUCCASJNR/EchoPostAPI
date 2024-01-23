from rest_framework import viewsets
from blog.models.post import BlogPost as Post, User
from blog.serializers.post import  CreateBlogPostSerialzer, BlogPostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime



class PostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateBlogPostSerialzer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        current_user = request.user

        if current_user.verified:
            if serializer.is_valid():
                post = Post.custom_save(user_id=current_user, **serializer.validated_data)
                image_url = Post.to_dict(post)['image']
                created_at_isoformat = Post.to_dict(post)['created_at']
                formatted_date = datetime.fromisoformat(created_at_isoformat).strftime('%Y-%m-%d %H:%M:%S')
                
                # Include the formatted date in the response data
                response_data = {
                    'message': 'Blog Post successfully created!',
                    'title': Post.to_dict(post)['title'],
                    'content': Post.to_dict(post)['content'],
                    'image': image_url if image_url else None,
                    'date': formatted_date,
                    'id': Post.to_dict(post)['id'],
                    'status_code': status.HTTP_201_CREATED
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'You need to verify your account to create a blog post'}, status=status.HTTP_403_FORBIDDEN)



class ViewAPostAPIView(APIView):
    """View for viewing a blog post with the id"""
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer
    def get(self, request, post_id, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        current_user = request.user
        post = Post.custom_get(**{"user_id": current_user.id, "id": post_id})
        if post:
            serialized_post = BlogPostSerializer(post)
            created_at_isoformat = Post.to_dict(post)['created_at']
            formatted_date = datetime.fromisoformat(created_at_isoformat).strftime('%Y-%m-%d %H:%M:%S')
            response_data = {
                    'message': 'Blog post details successfully retrieved',
                    'title': serialized_post.data['title'],
                    'content': serialized_post.data['content'],
                    'image': serialized_post.data['image'],
                    'username': User.custom_get(**{'id': current_user.id}).username,
                    'date': formatted_date,
                    'status_code': status.HTTP_200_OK
                    }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)

class ViewBlogPostsAPIView(APIView):
    """View for viewing all blog posts"""
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        current_user = request.user
        posts = Post.find_objs_by(**{"user_id": current_user.id})
        if posts:
            serialized_posts = BlogPostSerializer(posts, many=True, partial=True)
            response_data = {
                    'message': 'Blog posts successfully retrieved',
                    'posts': serialized_posts.data,
                    'status_code': status.HTTP_200_OK
                    }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'No blog posts found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateBlogPostAPIView(APIView):
    """View for updating a blog post"""
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer
    def put(self, request, post_id, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        current_user = request.user
        post = Post.custom_get(**{"user_id": current_user.id, "id": post_id})
        if post:
            if serializer.is_valid():
                Post.custom_update(filter_kwargs={"user_id": current_user.id, "id": post_id},
                                    update_kwargs=serializer.validated_data)
                formatted_date = datetime.fromisoformat(Post.to_dict(post)['updated_at']).strftime('%Y-%m-%d %H:%M:%S')
                response_data = {
                    'message': 'Blog post successfully updated!',
                    'title': Post.to_dict(post)['title'],
                    'content': Post.to_dict(post)['content'],
                    'image': Post.to_dict(post)['image'],
                    'date': formatted_date,
                    'status_code': status.HTTP_200_OK
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)
        

class DeleteBlogPostAPIView(APIView):
    """View for deleting a blog post"""
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer
    def delete(self, request, post_id, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        current_user = request.user
        post = Post.custom_get(**{"user_id": current_user.id, "id": post_id})
        if post:
            Post.custom_delete(**{"user_id": current_user.id, "id": post_id})
            response_data = {
                'message': 'Blog post successfully deleted!',
                'status_code': status.HTTP_200_OK
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)