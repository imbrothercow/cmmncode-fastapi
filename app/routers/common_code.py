from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.schemas.common_code import CommonCodeCreate, CommonCodeUpdate, CommonCodeResponse
from app.crud import common_code as crud
from app.crud import code_group as crudGroup

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/common-codes", tags=["공통 코드"])


@router.get("/{group_cd}", response_model=list[CommonCodeResponse])
def list_codes(
    group_cd: str,
    use_yn: Optional[bool] = Query(default=None, description="사용여부 필터 (true/false)"),
    db: Session = Depends(get_db),
):
    return crud.get_codes_by_group(db, group_cd, use_yn=use_yn)


@router.get("/{group_cd}/{code}", response_model=CommonCodeResponse)
def get_code(group_cd: str, code: str, db: Session = Depends(get_db)):
    obj = crud.get_code(db, group_cd, code)
    if not obj:
        # FAIL코드 404 : Not Found
        raise HTTPException(status_code=404, detail="공통 코드를 찾을 수 없습니다.")
    return obj

# REST api 관례로 post의 결과코드 201 : Created > 생성됨
@router.post("", response_model=CommonCodeResponse, status_code=201)
def create_code(data: CommonCodeCreate, db: Session = Depends(get_db)):
    # group_cd 체크
    group_existing = crudGroup.get_group(db, data.group_cd)
    logger.info(f"{group_existing}")
    if not group_existing:
        raise HTTPException(status_code=404, detail="존재하지 않는 그룹코드입니다.")
    # code 체크
    code_existing = crud.get_code(db, data.group_cd, data.code)
    if code_existing:
        #FAIL 코드 409 : Conflict (중복)
        raise HTTPException(status_code=409, detail="이미 존재하는 코드입니다.")
    
    return crud.create_code(db, data)


@router.patch("/{group_cd}/{code}", response_model=CommonCodeResponse)
def update_code(group_cd: str, code: str, data: CommonCodeUpdate, db: Session = Depends(get_db)):
    obj = crud.update_code(db, group_cd, code, data)
    if not obj:
        # FAIL코드 404 : Not Found
        raise HTTPException(status_code=404, detail="공통 코드를 찾을 수 없습니다.")
    return obj

# REST api 관례로 delete의 결과코드 204 : No Content > 보낼 데이터 없음
@router.delete("/{group_cd}/{code}", status_code=204)
def delete_code(group_cd: str, code: str, db: Session = Depends(get_db)):
    if not crud.delete_code(db, group_cd, code):
        # FAIL코드 404 : Not Found
        raise HTTPException(status_code=404, detail="공통 코드를 찾을 수 없습니다.")
