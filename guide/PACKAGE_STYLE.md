# 📦 프로젝트 패키지 구조 안내

이 문서는 **패키지 구조와 역할**을 설명합니다.  
코딩에 미숙해도 프로젝트의 큰 그림을 알 수 있도록 작성했습니다.  
질문 있으시면 언제든지 말씀해주세요.

---

## 📂 전체 구조

```
├── tests
├── backend
│ ├── model
│ ├── api
│ └── services
└── ai_service
├── tools
│ ├── rag_tools
│ └── mcp_tools
├── tools_setting
│ ├── mcp
│ └── rag
├── core
│ ├── enum
├── memory
├── graph
│ ├── state
├── agents
```


---

## 🧪 tests (테스트 공간)
- **실험실** 같은 공간입니다.  
- 다른 패키지와 연결되지 않아도 자유롭게 테스트할 수 있습니다.  
- 예시:
  - `rag_test.ipynb` → 문서 검색(RAG) 관련 실험  등
  - `api_test.ipynb` → API 응답 실험 등

---

## 🖥️ backend (FastAPI 서버)
- 사용자와 직접 연결되는 **창구(입구)** 역할을 합니다.  
- 앱에서 요청을 받으면 여기서 처리됩니다.  
- FastAPI 사용합니다.  

구성:
- `api/` →  API 
- `model/` → API 요청/응답 데이터 정의  
- `services/` → 기능별 서비스 코드
- `services/` 예시:
  - `letter_service.py` → 편지 기능  
  - `user_service.py` → 사용자 기능  
  - `ai_proxy.py` → AI 서비스와 연결하는 다리  
👉 services 는 실제 서비스 로직을 담당합니다.   
👉 api 는 services 의 로직을 불러와 api을 구성합니다.    
👉 backend는 `ai_proxy.py` 을 통해 **AI 내부 상태를 모른 채**, 결과만 받아서 사용자에게 돌려줍니다.  

#### 🔗 backend ↔ ai_service 연결 방식
- backend는 **AI의 내부 상태를 모릅니다.**  
- 대신, AI가 결과를 **딕셔너리(dict)** 형태로 정리해서 전달합니다.  

예시:
```python
def run_agent(session_id: str, user_input: str):
    result = call_ai_service(session_id, user_input)
    return {
        "status": "running",
        "progress": result.get("progress"),
        "checkpoint_id": result.get("checkpoint_id"),
        "answer": result.get("answer")
    }
```


## 🤖 ai_service (AI 두뇌)
- 실제 **AI 로직이 돌아가는 두뇌** 역할을 합니다.  
- backend와 독립적이며, 복잡한 연산은 모두 이곳에서 수행합니다.  

구성:
- `tools/` → AI가 사용하는 도구 (RAG, 웹검색, MCP 등)  
- `tools_setting/` → 도구 세부 설정  
- `core/` → AI 핵심 설정 및 LLM 관리  
- `memory/` → 대화 기록/상태 저장 (캐시, Redis)  
- `graph/` → LangGraph 워크플로우 및 상태 관리  
- `agents/` → AI 에이전트 정의 (예: 작업 수행, 결과 검토 등)  

