from django.urls import include, path

urlpatterns = [
    path('', include('apps.core.urls')),
    path('organizations/', include('apps.organizations.urls')),
    path('workspaces/', include('apps.workspaces.urls')),
    path('projects/', include('apps.projects.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('comments/', include('apps.comments.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('ai/', include('apps.ai_assistant.urls')),
    path('audit/', include('apps.audit_logs.urls')),
    path('profiles/', include('apps.user_profiles.urls')),
]
