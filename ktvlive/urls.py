from django.conf.urls import patterns, include, url
from django.contrib import admin
from pptv_live.sports import get_list,spider, read_m3u8, read_ts, get_precast, read_live_m3u8, read_live_ts, get_current_live
urlpatterns = patterns("",
    # Examples:
    # url(r'^$', 'ktvlive.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^pptvlive/getlist',get_list),
    url(r'^pptvlive/spider',spider),
    url(r'^pptvlive/readm3u8[0-9]*.m3u',read_m3u8),
    url(r'^pptvlive/readts[0-9]*.ts',read_ts),
    url(r'^pptvlive/getprecast',get_precast),
    url(r'^pptvlive/readlivem3u8[0-9]*.m3u',read_live_m3u8),
    url(r'^pptvlive/readlivets[0-9_]*.ts',read_live_ts),
    url(r'^pptvlive/getlivelist',get_current_live),
    #url(r'^pptvlive/getlist',include(get_list)),
)
