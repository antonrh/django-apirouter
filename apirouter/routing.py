from dataclasses import dataclass
from typing import Optional


@dataclass()
class APIRoute:
    name: Optional[str] = None


class APIRouter:
    pass
