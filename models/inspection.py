from typing import List, Optional

from pydantic import BaseModel


class InspectionModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    company_id: Optional[str]
    pig_id: Optional[str]
    pig_number: Optional[str]
    open: Optional[bool]
    place: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    clusters: Optional[List[list]]

    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_unset") is not None:
            kwargs["exclude_unset"] = True
        return BaseModel.dict(self, *args, **kwargs)
