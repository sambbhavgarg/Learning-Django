from django.urls import path

from . import views
'''
 the polls app has a detail view, and so might an app on the same project that
 is for a blog. How does one make it so that Django knows which app view to
 create for a url when using the {% url %} template tag?

 The answer is to add namespaces to your URLconf.
'''
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name = 'detail'),
    path('<int:question_id>/results/', views.results, name = 'results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
