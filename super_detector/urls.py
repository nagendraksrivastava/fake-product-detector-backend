from django.conf.urls import url
from views import signup_user, login_user, logout_user

from views import CustomObtainAuthToken, get_user_profile
from category import get_categories, get_subcategory, get_brand, search_product

urlpatterns = [
    url(r'^get_token/$', CustomObtainAuthToken.as_view()),
    url(r'^show-auth/$', get_user_profile),
    url(r'^login/$', login_user),
    url(r'^signup/$', signup_user),
    url(r'^logout/$', logout_user),
    url(r'^category/$', get_categories),
    url(r'^subcategory/(?P<category_id>\d+)/$', get_subcategory),
    url(r'^brand/(?P<subcategory_id>\d+)/$', get_brand),
    url(r'^product/$', search_product),
]
