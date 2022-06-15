from rest_framework.routers import SimpleRouter

from importer_app.views.products import ProductViewSet
from importer_app.views.webhooks import WebhooksViewSet

router = SimpleRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"webhooks", WebhooksViewSet, basename="webhooks")
urlpatterns = router.urls
