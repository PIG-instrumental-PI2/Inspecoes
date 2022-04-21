from typing import Optional

from pydantic import BaseModel


class PIGModel(BaseModel):
    id: Optional[str]
    pig_number: Optional[str]
    name: Optional[str]
    company_id: Optional[str]
    description: Optional[str]
    current_inspection: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_none"] = True
        return BaseModel.dict(self, *args, **kwargs)


class PIGUpdateModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    company_id: Optional[str]
    description: Optional[str]
    current_inspection: Optional[str]
