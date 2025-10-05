## 실행 커맨드
```uv run uvicorn app.backend.api.main:app```

## (로컬) database 세팅 

### 01. postgres DB 설치
- 맥북의 경우 
```
brew install postgresql
brew services start postgresql
```

- 윈도우의 경우 wsl 을 실행합시다.
```
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```


### 02. Dokcer로 PostgreSQL 실행
```
docker run --name postgres-local \
  -e POSTGRES_USER=seobi \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=emotion_letter \
  -p 5432:5432 \
  -d postgres:15
```

### 03. DB 접속 테스트 
```
docker exec -it postgres-local psql -U seobi -d emotion_letter
```
```위에 접속 성공하면 q 눌러서 탈출 ```

---
## ⚙️ .env 세팅 필수 입니다.

LANGCHAIN_TRACING_V2=true  
LANGCHAIN_API_KEY= "..."   
LANGCHAIN_PROJECT="..."   
OPENAI_API_KEY = "..."
BASE_URL="..."

## 📂 패키지 구조
```
app
├── tests
│   ├── rag_test.ipynb
│   └── api_test.ipynb
├── backend
│   ├── model
│   │   ├── ResponseData.py
│   │   └── RequestData.py
│   ├── api
│   │   └── main.py
│   └── services
│       ├── letter_service.py
│       ├── user_service.py
│       └── ai_proxy.py
└── ai_service
    ├── tools
    │   ├── rag_tools
    │   │   └── rag_tool.py
    │   ├── web_search.py
    │   └── mcp_tools
    │       └── mcp_tool.py
    ├── tools_setting
    │   ├── mcp
    │   │   ├── mcp_client.py
    │   │   └── mcp_server.py
    │   └── rag
    │       ├── chunking.py
    │       ├── retriever.py
    │       ├── embeddings.py
    │       └── loader.py
    ├── core
    │   ├── Config.py
    │   ├── enum
    │   │   └── Enum.py
    │   └── llm.py
    ├── memory
    │   ├── CacheMemory.py
    │   └── RedisMemory.py
    ├── graph
    │   ├── state
    │   │   └── GraphState.py
    │   ├── work_flow.py
    │   └── routes
    │       └── agent_route.py
    ├── agents
    │   ├── task_agent.py
    │   └── critic_agent.py
    └── preprocesser
        └── preprocessor.ipynb

```
자세한 내용은 guide/PACKAGE_STYPE.md 를 참고해주세요.


## 📝 코드 컨벤션
guide/CODE_CONVENTION.md 를 참고해주세요.

## 🌿 깃 허브 사용법
guide/GIT_BRANCH_GUIDE.md 를 참고해주세요.