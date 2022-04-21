from typing import List, Optional

from pydantic import BaseModel


class ClusterModel(BaseModel):
    id: Optional[str]
    inspection_id: Optional[str]
    pickled_data: Optional[bytes]
