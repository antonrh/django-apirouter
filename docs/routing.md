## Function views

```python
from apirouter import APIRouter, Response, Request

router = APIRouter()


@router.route("/items", methods=["GET", "POST"])
def items_view(request: Request):
    if request.method == "POST":
        return Response("POST /items")
    return Response("GET /items")
```

***GET** `https://127.0.0.1:8000/items`*

Response [200 OK]:

```
GET /items
```

***POST** `https://127.0.0.1:8000/items`*

Response [200 OK]:

```
POST /items
```


## Class based views

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

***GET** `https://127.0.0.1:8000/items`*

Response [200 OK]:

```json
[
  {
    "id": 1
  },
  {
    "id": 2
  }
]
```
