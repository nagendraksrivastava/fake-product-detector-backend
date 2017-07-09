from django.conf.urls import url
from views import signup_user, login_user, logout_user

from views import CustomObtainAuthToken, get_user_profile
from category import get_categories

urlpatterns = [
    url(r'^get_token/$', CustomObtainAuthToken.as_view()),
    url(r'^show-auth/$', get_user_profile),
    url(r'^login/$', login_user),
    url(r'^signup/$', signup_user),
    url(r'^logout/$', logout_user),
    url(r'^category/$', get_categories),
]
