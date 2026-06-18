from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.common_code import CommonCode, CodeGroup
from app.schemas.common_code import CommonCodeCreate, CommonCodeUpdate

def get_code(db: Session, group_cd: str, code: str) -> CommonCode | None:
    return db.scalar(
        select(CommonCode)
        .where(CommonCode.group_cd == group_cd, CommonCode.code == code)
    )


def get_codes_by_group(db: Session, group_cd: str, use_yn: bool | None = None) -> list[CommonCode]:
    stmt = select(CommonCode).where(CommonCode.group_cd == group_cd)
    if use_yn is not None:
        stmt = stmt.where(CommonCode.use_yn == use_yn)
    stmt = stmt.order_by(CommonCode.sort_order)
    return list(db.scalars(stmt).all())


def create_code(db: Session, data: CommonCodeCreate) -> CommonCode:
    # group_cd 유효성 체크
    group = db.scalar(select(CodeGroup).where(CodeGroup.group_cd == data.group_cd))
    if not group:
        return None
    
    obj = CommonCode(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_code(db: Session, group_cd: str, code: str, data: CommonCodeUpdate) -> CommonCode | None:
    obj = get_code(db, group_cd, code)
    if not obj:
        return None
    for key, val in data.model_dump(exclude_none=True).items():
        setattr(obj, key, val)
    db.commit()
    db.refresh(obj)
    return obj


def delete_code(db: Session, group_cd: str, code: str) -> bool:
    obj = get_code(db, group_cd, code)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
