Django APIRouter provides fully compatible with Django [Request](https://docs.djangoproject.com/en/3.0/ref/request-response/#httprequest-objects) class 
with additional properties and methods.

## Request class

Additional method and properties:

* `.query_params -> QueryDict` - A dictionary-like HTTP GET parameters. 
* `.form -> QueryDict` - A dictionary-like HTTP POST parameters.
* `.files -> MultiValueDict` - A dictionary-like object containing all uploaded files.
* `.cookies -> Dict[str, str]` - Returns dictionary-like cookies. Keys and values are strings.
* `.json(self) -> Any` - Parse JSON body or raise `apirouter.exceptions.APIException(400)`

## Custom request class 

You can override request class globally or on route level.

* Set `APIROUTER_DEFAULT_REQUEST_CLASS=apirouter.request.Request` config
* Set in router class
```python
from apirouter import APIRouter, Request


class MyRequest(Request):
    pass


router = APIRouter(request_class=MyRequest)
```
* Set in route
```python
from apirouter import APIRouter, Request, Response


class MyRequest(Request):
    pass


router = APIRouter()


@router.route("/", request_class=MyRequest)
def index(request: MyRequest):
    return Response("OK")
```
