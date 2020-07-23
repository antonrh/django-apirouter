from apirouter import APIRouter
from tests.routers.inner import router as inner_router
from tests.routers.method import router as method_router
from tests.routers.named import router as named_router
from tests.routers.root import router as root_router

router = APIRouter(name="test")
router.include_router(root_router)
router.include_router(method_router)
router.include_router(inner_router, prefix="/inner/")
router.include_router(named_router, prefix="/named/")

urlpatterns = router.urls
