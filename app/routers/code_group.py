from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common_code import CodeGroupCreate, CodeGroupUpdate, CodeGroupResponse, CodeGroupWithCodes
from app.crud import code_group as crud

router = APIRouter(prefix="/code-groups", tags=["코드 그룹"])


@router.get("", response_model=list[CodeGroupResponse])
def list_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_groups(db, skip=skip, limit=limit)


@router.get("/{group_cd}", response_model=CodeGroupWithCodes)
def get_group(group_cd: str, db: Session = Depends(get_db)):
    obj = crud.get_group(db, group_cd)
    if not obj:
        # FAIL코드 404 : Not Found
        raise HTTPException(status_code=404, detail="코드 그룹을 찾을 수 없습니다.")
    return obj

# REST api 관례로 post의 결과코드 201 : Created > 생성됨
@router.post("", response_model=CodeGroupResponse, status_code=201)
def create_group(data: CodeGroupCreate, db: Session = Depends(get_db)):
    existing = crud.get_group(db, data.group_cd)
    if existing:
        # FAIL코드 409 : Conflict(중복등록)
        raise HTTPException(status_code=409, detail="이미 존재하는 그룹 코드입니다.")
    return crud.create_group(db, data)


@router.patch("/{group_cd}", response_model=CodeGroupResponse)
def update_group(group_cd: str, data: CodeGroupUpdate, db: Session = Depends(get_db)):
    obj = crud.update_group(db, group_cd, data)
    if not obj:
        # FAIL코드 404 : Not Found
        raise HTTPException(status_code=404, detail="코드 그룹을 찾을 수 없습니다.")
    return obj


# REST api 관례로 delete의 결과코드 204 : No Content > 보낼 데이터 없음
@router.delete("/{group_cd}", status_code=204)
def delete_group(group_cd: str, db: Session = Depends(get_db)):
    if not crud.delete_group(db, group_cd):
        # FAIL코드 404 : Not Found
        raise HTTPException(status_code=404, detail="코드 그룹을 찾을 수 없습니다.")
