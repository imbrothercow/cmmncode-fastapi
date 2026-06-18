from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.common_code import CodeGroup
from app.schemas.common_code import CodeGroupCreate, CodeGroupUpdate


def get_group(db: Session, group_cd: str) -> CodeGroup | None:
    return db.scalar(select(CodeGroup).where(CodeGroup.group_cd == group_cd))


def get_groups(db: Session, skip: int = 0, limit: int = 100) -> list[CodeGroup]:
    return list(db.scalars(select(CodeGroup).offset(skip).limit(limit)).all())


def create_group(db: Session, data: CodeGroupCreate) -> CodeGroup:
    obj = CodeGroup(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_group(db: Session, group_cd: str, data: CodeGroupUpdate) -> CodeGroup | None:
    obj = get_group(db, group_cd)
    if not obj:
        return None
    for key, val in data.model_dump(exclude_none=True).items():
        setattr(obj, key, val)
    db.commit()
    db.refresh(obj)
    return obj


def delete_group(db: Session, group_cd: str) -> bool:
    obj = get_group(db, group_cd)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
