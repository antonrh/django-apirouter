Django API Router provides decorator based routing system build on top Django 
of [URL dispatcher](https://docs.djangoproject.com/en/3.0/topics/http/urls/).

## APIRouter class

*project/urls.py*
 
```python
from apirouter import APIRouter

router = APIRouter()

urls = router.urls
```

`router.urls` converts APIRouter routes to Django URLPattern list.

## Function-based views

Here's simple function view that returns plain text based on HTTP method. 

```python
from apirouter import APIRouter, Response, Request

router = APIRouter()


@router.route("/items")
def items(request: Request):
    if request.method == "POST":
        return Response("Create item")
    return Response("Get items")
```

Or simple function view that accepts only particular request methods.

```python
from apirouter import APIRouter, Response, Request

router = APIRouter()


@router.route("/items/clear", methods=["DELETE"])
def items_create(request: Request):
    return Response("Delete items")
```

`method` argument supports `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`, `TRACE` HTTP methods.

## Class-based views

Here is simple class-based view that accepts only particular request methods.

```python
from django.views import View

from apirouter import APIRouter, JsonResponse, Request

router = APIRouter()


@router.view("/items")
class ItemsView(View):
    def get(self, request: Request):
        return JsonResponse([{"id": 1}, {"id": 2}])

    def post(self, request: Request):
        return JsonResponse({"id": 3})
```

## Named routes

In order to perform URL reversing, you’ll need to use named routes.

```python
from django.views import View

from apirouter import APIRouter, Request, Response

router = APIRouter(name="root")


@router.route("/route1", name="route1")
def route1(request: Request):
    return Response("This is route1")


@router.view("/route2", name="route2")
class Route2View(View):
    def get(self, request: Request):
        return Response("This is route2")
```

Now you can perform URL reversing with Django [`reverse`](https://docs.djangoproject.com/en/3.0/ref/urlresolvers/#django.urls.reverse) function:

```python
from django.urls import reverse

reverse("root:route1")  # returns /route1
reverse("root:route2")  # returns /route2
```

## Sub routers

Django API Router supports sub routing by including other routers.

```python
from apirouter import APIRouter, Request, Response

users_router = APIRouter(name="users")


@users_router.route("/", name="list")
def users_list(request: Request):
    return Response("Get users")


accounts_router = APIRouter(name="accounts")


@accounts_router.route("/", name="list")
def accounts_list(request: Request):
    return Response("Get account")


@accounts_router.route("/<int:account_id>", name="detail")
def accounts_detail(request: Request, account_id: int):
    return Response("Get account details")


root = APIRouter(name="root")
root.include_router(users_router, prefix="/users/")
root.include_router(accounts_router, prefix="/accounts/")


urlpatterns = root.urls
```

It is also possible to perform URL reversing from sub routes.

```python
from django.urls import reverse

reverse("root:users:list")  # returns /users/
reverse("root:accounts:list")  # returns /accounts/
reverse("root:accounts:detail", kwargs={"account_id": "100"})  # returns /accounts/100/
```

## Path helper

You can also add Django compatible path URL patters using router `.path(route, view, kwargs=None, name=None)` method.

```python
from apirouter import APIRouter, Request, Response


def index(request: Request):
    return Response("Router view")


router = APIRouter()


urlpatterns = [router.path("", index, name="index")]
```