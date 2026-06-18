from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ── CodeGroup ──────────────────────────────────────────

class CodeGroupBase(BaseModel):
    group_cd: str
    group_nm: str
    description: Optional[str] = None
    use_yn: bool = True


class CodeGroupCreate(CodeGroupBase):
    pass


class CodeGroupUpdate(BaseModel):
    group_nm: Optional[str] = None
    description: Optional[str] = None
    use_yn: Optional[bool] = None


class CodeGroupResponse(CodeGroupBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CodeGroupWithCodes(CodeGroupResponse):
    codes: List["CommonCodeResponse"] = []


# ── CommonCode ─────────────────────────────────────────

class CommonCodeBase(BaseModel):
    group_cd: str
    code: str
    code_nm: str
    code_val: Optional[str] = None
    sort_order: int = 0
    use_yn: bool = True


class CommonCodeCreate(CommonCodeBase):
    pass


class CommonCodeUpdate(BaseModel):
    code_nm: Optional[str] = None
    code_val: Optional[str] = None
    sort_order: Optional[int] = None
    use_yn: Optional[bool] = None


class CommonCodeResponse(CommonCodeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
