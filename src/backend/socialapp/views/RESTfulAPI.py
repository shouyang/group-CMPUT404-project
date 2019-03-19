from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .. import serializers
from .. import models
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """ Defines the pagination for a modelViewSet
    """
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 100





class PublicPostsViewSet(ListAPIView):
    # Returns all public posts on the server
    queryset = models.Post.objects.filter(visibility='PUBLIC',unlisted=False)
    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination


class PostViewSet(ListAPIView):
    # Returns a single post
    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # TODO: Check Author Has Permissions To See The Post
        # TODO: Check if Hindle actually wants this as a list of one item?
        post = get_object_or_404(models.Post, id= self.kwargs.get("pk"))
        return [post]

class PostCommentsViewSet(ListAPIView):
    # Returns a list of the comments attached to the post
    serializer_class = serializers.CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        post = get_object_or_404(models.Post, id=self.kwargs.get("pk"))

        return post.comments.all()

    # TODO: Bind this same url to take comments via POST and create them server side

class AuthorViewSet(ListAPIView):
    # Returns a single author
    serializer_class = serializers.AuthorAltSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # TODO: Check if Hindle actually wants this as a list of one item?
        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        return [author]




class AuthorFeedViewSet(ListAPIView):
    # Returns the logged in author's feed of posts
    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        author = self.request.user.author
        return author.get_all_posts()


class AuthoredByPostsViewSet(ListAPIView):
    # Returns all posts by a particular author denoted by author pk
    # Results may differ depending on authentication

    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        return author.posts_by.all()


class FriendsViewSet(ListAPIView):
    pass

class isFriendsViewSet(ListAPIView):
    pass

class FriendsRequestViewSet(ListAPIView):
    pass
