from django.conf.urls import patterns, include, url
from django.contrib import admin
import stock_app.views

urlpatterns = patterns(
    # Examples:
    # url(r'^$', 'stock_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', stock_app.views.index, name='index'),
    url(r'^symbol/$', stock_app.views.symbol, name='symbol'),
    url(r'^buy/$', stock_app.views.buy, name='buy')
)
