from django.conf.urls import patterns, include, url
from . import views

app_name = 'blog'
urlpatterns = [
        url(r'^$', views.main_page, name='main_page'),
        url(r'^ajax/get', views.ajax_get_test, name='ajax_get_test'),
        url(r'^ajax/post', views.ajax_post_test, name='ajax_post_test'),
        url(r'^upload_file$', views.upload_file, name='upload_file'),
        url(r'^post$', views.post_list, name='post_list'),
        url(r'^post/new$', views.post_new, name='post_new'),
        url(r'^post/get_tag_cloud_list$', views.get_tag_cloud_list, name='get_tag_cloud_list'),
        url(r'^post/get_recent_posts_list$', views.get_recent_posts_list, name='get_recent_posts_list'),
        url(r'^post/recent_comments$', views.recent_comments, name='recent_comments'),
        url(r'^post/(?P<post_id>[0-9]+)/', include(
            [
                url(r'^$', views.post_detail, name='post_detail'),
                url(r'^edit$', views.post_edit, name='post_edit'),
                url(r'^publish$', views.post_publish, name='post_publish'),
                url(r'^remove$', views.post_remove, name='post_remove'),
                url(r'^like$', views.post_like, name='post_like'),
                url(r'^dislike$', views.post_dislike, name='post_dislike'),
                url(r'^new_comment$', views.post_new_comment, name="post_new_comment"),
                ]
            )),
        url(r'^drafts$', views.post_draft_list, name='post_draft_list'),
        url(r'^about$', views.about_me, name="about_me"),
        url(r'^message_board$', views.message_board, name="message_board"),
        url(r'^tag/(?P<tagname>\w+)$', views.get_tag_post_list, name="get_tag_post_list"),
        ]
