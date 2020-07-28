## Function views
TODO

## Class based views

```python
from django.views import View

from apirouter import APIRouter, Request

router = APIRouter()


@router.view("/items")
class ItemsView(View):
    def get(self, request: Request):
        return [{"id": 1}, {"id": 2}]
```

***GET** https://127.0.0.1:8000/items*

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
