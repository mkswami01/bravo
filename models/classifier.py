from typing import Literal, Optional
from pydantic import BaseModel, Field

class Classification(BaseModel):
    domain: Optional[Literal["github", "linear", ]]
    complexity: Literal["simple", "complex"]


class DomainClassification(BaseModel):
    query: str
    domain: Literal["github", "linear"]