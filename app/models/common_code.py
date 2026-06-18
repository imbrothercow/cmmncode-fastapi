from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class CodeGroup(Base):
    __tablename__ = "code_group"

    id = Column(Integer, primary_key=True, index=True)
    group_cd = Column(String(50), unique=True, nullable=False, index=True)  # 예: "STATUS"
    group_nm = Column(String(100), nullable=False)                          # 예: "상태코드"
    description = Column(String(255), nullable=True)
    use_yn = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    codes = relationship("CommonCode", back_populates="group", cascade="all, delete-orphan")


class CommonCode(Base):
    __tablename__ = "common_code"

    id = Column(Integer, primary_key=True, index=True)
    group_cd = Column(String(50), ForeignKey("code_group.group_cd"), nullable=False)
    code = Column(String(50), nullable=False)       # 예: "ACTIVE"
    code_nm = Column(String(100), nullable=False)   # 예: "활성"
    code_val = Column(String(255), nullable=True)   # 부가 값 (선택)
    sort_order = Column(Integer, default=0)
    use_yn = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    group = relationship("CodeGroup", back_populates="codes")
