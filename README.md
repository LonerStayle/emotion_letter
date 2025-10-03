## ⚙️ .env 세팅 필수 입니다.

LANGCHAIN_TRACING_V2=true  
LANGCHAIN_API_KEY= "..."   
LANGCHAIN_PROJECT="..."   
OPENAI_API_KEY = "..."


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