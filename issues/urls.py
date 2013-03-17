from django.conf.urls import patterns,url


urlpatterns = patterns('',
    url(r'^$','issues.views.issues',name="issueshome"),
    url(r'^list$','issues.views.list_issues',name="listissues")
    )
