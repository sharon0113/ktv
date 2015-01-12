from django.conf.urls import patterns, include, url
from django.contrib import admin
from pptv_live.sports import get_list,spider, read_m3u8, read_ts
urlpatterns = patterns("",
    # Examples:
    # url(r'^$', 'ktvlive.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^pptvlive/getlist',get_list),
    url(r'^pptvlive/spider',spider),
    url(r'^pptvlive/readm3u8',read_m3u8),
    url(r'^pptvlive/readts[0-9]*.ts',read_ts),
    #url(r'^pptvlive/getlist',include(get_list)),
)
