from rest_framework.routers import SimpleRouter
from .views import KeyInfoViewset

router=SimpleRouter()
router.register('',KeyInfoViewset)

urlpatterns=[]
urlpatterns+=router.urls