from django.contrib.auth.models import User
# from django.contrib.sites.models import get_current_site
# from django.contrib.sites.models import Site
from .. import models as mod
from django.db import models
from django.urls import reverse
from django.shortcuts import get_object_or_404
import uuid


class Author(models.Model):
    """ Authors represent a user in the social app's context, note they are distinct from users for modularity.

    Authors can establish relations to other authors on the site and to their github profile.

    Authors can make posts and comments which are the primary content of the site.
    """

    # Django Metadata on class
    class Meta:
        ordering = ['displayName'] # Order By Display Name By Default

    # Identifiers
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    # Relations
    localuser = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    friends = models.ManyToManyField("Author", blank=True, related_name="friend_by")
    friend_requests = models.ManyToManyField("Author", blank=True, related_name="sent_friend_requests")

    # Data
    github = models.CharField(max_length=150, blank=False)
    displayName = models.CharField(max_length=150, blank=False)
    bio =  models.TextField(blank=True, default="No bio")
    host = models.URLField(blank=True)
    image = models.URLField(blank=True)
    feed = models.URLField(blank=True)

    # Methods
    def __str__(self):
        return self.displayName

    def get_absolute_url(self):
        return reverse('author-id', args=[str(self.id)])

    def get_friends(self):
        output = set()
        for friend in self.friends.all():
            if friend.friends.filter(pk=self.id):
                output.add(friend)
        return output

    def get_friends_of_friends(self):
        output = set()

        for friend in self.friends.all():
            if friend.friends.filter(pk=self.id):
                output.add(friend)
                for friend_of_friend in friend.friends.all():
                    if friend_of_friend.friends.filter(pk=friend.id):
                        output.add(friend_of_friend)
        return output

    def get_posts_of_friends(self):
        output = mod.Post.objects.none()

        for f in self.friends.all():
            if f.friends.filter(pk=self.id):
                output = output | mod.Post.objects.filter(author=f,visibility='FRIENDS',unlisted=False)
        return output


    def get_posts_of_friends_of_friends(self):
        output = mod.Post.objects.none()

        for f in self.friends.all():
            if f.friends.filter(pk=self.id):
                output = output | mod.Post.objects.filter(author=f,visibility='FOAF',unlisted=False)
            for fof in f.friends.all():
                if fof.friends.filter(pk=f.id):
                    output = output | mod.Post.objects.filter(author=fof,visibility='FOAF',unlisted=False)
        return output

    def get_private(self):
        return mod.Post.objects.filter(visibleTo=self,unlisted=False)


    def is_friend(self, id):
        user =mod.Author.objects.get(id=id)
        return user.friends.filter(pk=self.id).exists() 

    def is_friend_of_friend(self, id):
        user =mod.Author.objects.get(id=id)
        if user.friends.filter(pk=self.id).exists():
            return True
        else:
            for friend in user.friends.all():
                if friend.friends.filter(pk=self.id).exists():
                    return True
        return False

    def get_my_feed(self):
        return mod.Post.objects.filter(author=self)

    def get_server(self): #todo dont hardcode
        return mod.Post.objects.filter(visibility='SERVERONLY',unlisted=False,origin="http://127.0.0.1:8000")
        # return mod.Post.objects.none()

    def get_public(self):
        return mod.Post.objects.filter(visibility='PUBLIC',unlisted=False)

    def post_permission(self, post):
        user = post.author
        visibility  = post.visibility

        if user!=self:
            if visibility=="PRIVATE":
                if user!=self:
                    if post.visibleTo.filter(pk=self.id).exists()==False:
                        return False 
            elif visibility=="FRIENDS" or visibility=="FOAF":
                if visibility=="FRIENDS" and user.friends.filter(pk=self.id).exists()==False:
                    return False
                if visibility=="FOAF":
                    friend_check = user.friends.filter(pk=self.id).exists()
                    for fof in user.friends.all():
                        if fof.friends.filter(pk=self.id).exists()==False and friend_check == False:
                            return False
            elif visibility=='SERVERONLY':
                if post.origin!="http://127.0.0.1:8000":
                    return False

            # if ('http://'+get_current_site(request).domain) != post.origin:
            #     return False
            pass
        return True

    def is_me(self, author):
        return (author == self)

    def get_all_posts(self):
        output = self.get_my_feed()
        output |= self.get_posts_of_friends()
        output |= self.get_posts_of_friends_of_friends()
        output |= self.get_private()
        output |= self.get_server()
        output |= self.get_public()

        return output


    def send_friend_request(self, target_author):
        # Adds target_author to this author's friends and sends the other author a friend request
        # If the target_author has sent this author a friend request, no additional request is sent
        # it is taken as the current author accepting the friend request.

        self.friends.add(target_author)

        if target_author in self.friend_requests.all():
            self.friend_requests.remove(target_author)
            return

        if self not in target_author.friend_requests.all():
            target_author.friend_requests.add(self)


    def remove_from_friends(self, target_author):
        # Removes target_author from friends
        # As a consequence, if the two authors are friends (not that one is following the other), from the target author's perspective, they become a follower of this author.
        self.friends.remove(target_author)

    def accept_friend_request(self, sender_author):
        self.friends.add(sender_author)
        self.friend_requests.remove(sender_author)

    def decline_friend_request(self, sender_author):
        self.friend_requests.remove(sender_author)

    def get_friend_requests(self):
        output = set()
        for friend_request in self.friend_requests.all():
            output.add(friend_request)
        return output

    def is_follower(self, other_author):
        return (self in other_author.friends.all()) and (other_author not in self.friends.all())

    def is_following(self, other_author):
        return (other_author in self.friends.all()) and (self not in other_author.friends.all())

