# Django APIRouter (in progress)

Django API router component.

*Inspired by [FastAPI](https://fastapi.tiangolo.com/) and [Django Rest Framework](https://www.django-rest-framework.org/).*

![tests](https://github.com/antonrh/django-apirouter/workflows/tests/badge.svg)
[![codecov](https://codecov.io/gh/antonrh/django-apirouter/branch/master/graph/badge.svg)](https://codecov.io/gh/antonrh/django-apirouter)
[![Documentation Status](https://readthedocs.org/projects/django-apirouter/badge/?version=latest)](https://django-apirouter.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![version](https://img.shields.io/pypi/v/django-apirouter.svg)](https://pypi.org/project/django-apirouter/)
[![license](https://img.shields.io/pypi/l/django-apirouter)](https://github.com/antonrh/django-apirouter/blob/master/LICENSE)

---

Documentation: https://django-apirouter.readthedocs.io/

---

## Installing

Install using `pip`:

```bash
pip install django-apirouter
```

## Quick Example

*project/urls.py*

```python
from apirouter import APIRouter, Request

router = APIRouter()


@router.route("/")
def index(request: Request):
    return "Hello, Django APIRouter!"


urlpatterns = router.urls
```

## TODO:

* Documentation
* Custom request / response classes
* OpenAPI support (Swagger, ReDoc)
* Pydantic support
* Async views support (with Django 3.1)
* etc.
