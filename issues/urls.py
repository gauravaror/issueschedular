from django.conf.urls import patterns,url


urlpatterns = patterns('',
    url(r'^issue/(?P<issuenumber>\d+)$','issues.views.issues',name="issueshome"),
    url(r'^update/(?P<issuenumber>\d+)$','issues.views.update_issue',name="issuesupdate"),
    url(r'^list$','issues.views.list_issues',name="listissues"),
    url(r'^create$','issues.views.create_issue',name="createissue"),
    url(r'^submit$','issues.views.submit_issue',name="submitissue"),
    url(r'^accesstoken/(?P<cod>[a-z,0-9,A-Z]*)$','issues.views.get_accesstoken',name="tokengenerator"),
    url(r'^authorize$','issues.views.authorize',name="autherizationredirector"),
    )
