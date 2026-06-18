# init py는 패키지 import를 가능하도록 하는 파일. 다만, 변수선언도 가능하다.
from app.routers import code_group, common_code

default_prefix = "/api/v1"
all_routers = [
    {"router": code_group.router},
    {"router": common_code.router}
]