from django.conf.urls import patterns, include, url
from django.contrib import admin
from pptv_live.sports import get_list,spider
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ktvlive.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^pptvlive/getlist',get_list),
    url(r'^pptvlive/spider',spider),
    #url(r'^pptvlive/getlist',include(get_list)),
)
