from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib import admin

from account.openid_consumer import PinaxConsumer

import os.path

#from microblogging.feeds import TweetFeedAll, TweetFeedUser, TweetFeedUserWithFriends
#tweets_feed_dict = {"feed_dict": {
#    'all': TweetFeedAll,
#    'only': TweetFeedUser,
#    'with_friends': TweetFeedUserWithFriends,
#}}
#
#from blog.feeds import BlogFeedAll, BlogFeedUser
#blogs_feed_dict = {"feed_dict": {
#    'all': BlogFeedAll,
#    'only': BlogFeedUser,
#}}
#
#from bookmarks.feeds import BookmarkFeed
#bookmarks_feed_dict = {"feed_dict": { '': BookmarkFeed }}

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'group_topics.views.topics', {'template_name': 'frontpage.html'}, name="home"),

    (r'^volunteering/', include('volunteering.urls')),

    
    (r'^about/', include('about.urls')),
    (r'^account/', include('account_extra.urls')),
    (r'^auto/tags/', include('tagging_utils.urls')),
    (r'^openid/(.*)', PinaxConsumer()),
    (r'^bbauth/', include('bbauth.urls')),
    (r'^authsub/', include('authsub.urls')),
    (r'^profiles/', include('profiles.urls')),
#    (r'^blog/', include('blog.urls')),
    (r'^tags/', include('tag_app.urls')),
    (r'^invitations/', include('friends_app.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^announcements/', include('announcements.urls')),
    (r'^tweets/', include('microblogging.urls')),
    (r'^comments/', include('mythreadedcomments.urls')),
    (r'^robots.txt$', include('robots.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
#    (r'^bookmarks/', include('bookmarks.urls')),

    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    (r'^admin/(.*)', admin.site.root),
#    (r'^photos/', include('photos.urls')),
    (r'^avatar/', include('avatar.urls')),
#    (r'^swaps/', include('swaps.urls')),
    (r'^flag/', include('flag.urls')),
#    (r'^locations/', include('locations.urls')),
    
    (r'^groups/', include('base_groups.urls')),
    (r'^networks/', include('networks.urls')),
    (r'^chapters/', include('networks.urls.chapters')),
    (r'^communities/', include('communities.urls')),
    (r'^events/', include('events.urls')),
    (r'^posts/', include('group_topics.urls')),
    (r'^creditcard/', include('creditcard.urls')),
    
    url(r'^unsubscribe/$', 'networks.views.unsubscribe', name='network_unsubscribe',),
    
#    (r'^feeds/tweets/(.*)/$', 'django.contrib.syndication.views.feed', tweets_feed_dict),
#    (r'^feeds/posts/(.*)/$', 'django.contrib.syndication.views.feed', blogs_feed_dict),
#    (r'^feeds/bookmarks/(.*)/?$', 'django.contrib.syndication.views.feed', bookmarks_feed_dict),
    url(r'^feeds/posts/(?P<group_slug>[-\w]+)/$', 'group_topics.views.feed', name="topic_feed"),
)

## @@@ for now, we'll use friends_app to glue this stuff together

#from photos.models import Image
#
#friends_photos_kwargs = {
#    "template_name": "photos/friends_photos.html",
#    "friends_objects_function": lambda users: Image.objects.filter(member__in=users),
#}
#
#from blog.models import Post
#
#friends_blogs_kwargs = {
#    "template_name": "blog/friends_posts.html",
#    "friends_objects_function": lambda users: Post.objects.filter(author__in=users),
#}
#
#from microblogging.models import Tweet
#
#friends_tweets_kwargs = {
#    "template_name": "microblogging/friends_tweets.html",
#    "friends_objects_function": lambda users: Tweet.objects.filter(sender_id__in=[user.id for user in users], sender_type__name='user'),
#}
#
#from bookmarks.models import Bookmark
#
#friends_bookmarks_kwargs = {
#    "template_name": "bookmarks/friends_bookmarks.html",
#    "friends_objects_function": lambda users: Bookmark.objects.filter(saved_instances__user__in=users),
#    "extra_context": {
#        "user_bookmarks": lambda request: Bookmark.objects.filter(saved_instances__user=request.user),
#    },
#}
#
#urlpatterns += patterns('',
#    url('^photos/friends_photos/$', 'friends_app.views.friends_objects', kwargs=friends_photos_kwargs, name="friends_photos"),
#    url('^blog/friends_blogs/$', 'friends_app.views.friends_objects', kwargs=friends_blogs_kwargs, name="friends_blogs"),
#    url('^tweets/friends_tweets/$', 'friends_app.views.friends_objects', kwargs=friends_tweets_kwargs, name="friends_tweets"),
#    url('^bookmarks/friends_bookmarks/$', 'friends_app.views.friends_objects', kwargs=friends_bookmarks_kwargs, name="friends_bookmarks"),
#)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('', 
        (r'^site_media/', include('staticfiles.urls'))
    )
