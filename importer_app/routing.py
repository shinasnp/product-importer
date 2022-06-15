from django.conf.urls import url

from importer_app import consumers

websocket_urlpatterns = [
    url(r"^ws/notification/file_stream/$", consumers.StreamFileProcess.as_asgi()),
]
