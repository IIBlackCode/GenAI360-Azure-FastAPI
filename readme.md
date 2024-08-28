# GenAI360 Azure향 개발지원
## 파일구성
## 파일 구성
```shell
App/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── user.py
│   ├── item.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── item.py
├── templates/
│   ├── base.html
│   ├── index.html
└── static/
    ├── css/
    ├── js/
Terraform/
├── main.tf
├── output.tf
├── provider.tf
└── read.md
```
- App : FastAPI Project
- Terraform : Azure향 클라우드 인프라 IaaS 테라폼 코드