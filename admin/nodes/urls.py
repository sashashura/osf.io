from django.conf.urls import url
from admin.nodes import views

app_name = 'admin'

urlpatterns = [
    url(r'^$', views.NodeSearchView.as_view(), name='search'),
    url(r'^flagged_spam$', views.NodeFlaggedSpamList.as_view(), name='flagged-spam'),
    url(r'^known_spam$', views.NodeKnownSpamList.as_view(), name='known-spam'),
    url(r'^known_ham$', views.NodeKnownHamList.as_view(), name='known-ham'),
    url(r'^doi_backlog_list/$', views.DoiBacklogListView.as_view(), name='doi-backlog-list'),
    url(r'^registration_list/$', views.RegistrationListView.as_view(), name='registrations'),
    url(r'^stuck_registration_list/$', views.StuckRegistrationListView.as_view(), name='stuck-registrations'),
    url(r'^ia_backlog_list/$', views.RegistrationBacklogListView.as_view(), name='ia-backlog-list'),
    url(r'^(?P<guid>[a-z0-9]+)/$', views.NodeView.as_view(), name='node'),
    url(r'^(?P<guid>[a-z0-9]+)/logs/$', views.AdminNodeLogView.as_view(), name='node-logs'),
    url(r'^(?P<guid>[a-z0-9]+)/schema_responses/$', views.AdminNodeSchemaResponseView.as_view(),
        name='schema-responses'),
    url(r'^(?P<guid>[a-z0-9]+)/update_embargo/$', views.RegistrationUpdateEmbargoView.as_view(), name='update-embargo'),
    url(r'^(?P<guid>[a-z0-9]+)/remove/$', views.NodeDeleteView.as_view(), name='remove'),
    url(r'^(?P<guid>[a-z0-9]+)/restore/$', views.NodeDeleteView.as_view(), name='restore'),
    url(r'^(?P<guid>[a-z0-9]+)/confirm_spam/$', views.NodeConfirmSpamView.as_view(), name='confirm-spam'),
    url(r'^(?P<guid>[a-z0-9]+)/confirm_ham/$', views.NodeConfirmHamView.as_view(), name='confirm-ham'),
    url(r'^(?P<guid>[a-z0-9]+)/confirm_unflag/$', views.NodeConfirmUnflagView.as_view(), name='confirm-unflag'),
    url(r'^(?P<guid>[a-z0-9]+)/reindex_share_node/$', views.NodeReindexShare.as_view(), name='reindex-share-node'),
    url(r'^(?P<guid>[a-z0-9]+)/reindex_elastic_node/$', views.NodeReindexElastic.as_view(),
        name='reindex-elastic-node'),
    url(r'^(?P<guid>[a-z0-9]+)/restart_stuck_registrations/$', views.RestartStuckRegistrationsView.as_view(),
        name='restart-stuck-registrations'),
    url(r'^(?P<guid>[a-z0-9]+)/remove_stuck_registrations/$', views.RemoveStuckRegistrationsView.as_view(),
        name='remove-stuck-registrations'),
    url(r'^(?P<guid>[a-z0-9]+)/remove_user/(?P<user_id>[a-z0-9]+)/$', views.NodeRemoveContributorView.as_view(),
        name='remove-user'),
    url(r'^(?P<guid>[a-z0-9]+)/modify_storage_usage/$', views.NodeModifyStorageUsage.as_view(),
        name='adjust-storage-usage'),
    url(r'^(?P<guid>[a-z0-9]+)/recalculate_node_storage/$', views.NodeRecalculateStorage.as_view(),
        name='recalculate-node-storage'),
    url(r'^(?P<guid>[a-z0-9]+)/make_private/$', views.NodeMakePrivate.as_view(), name='make-private'),
    url(r'^(?P<guid>[a-z0-9]+)/make_public/$', views.NodeMakePublic.as_view(), name='make-public'),
]
