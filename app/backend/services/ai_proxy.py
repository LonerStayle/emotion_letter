"""
아래는 예시 입니다. 의존 분리를 위해 backend 패키지는 ai_service 의 랭그래프 상태를 몰라야합니다.

그래서 아래와 같이 dict로 변환해서 리턴을 해서 ai의 결과물을 사용합니다.
"""




# def run_agent(session_id: str, user_input: str):
#     # ai_service 호출
#     result = call_ai_service(session_id, user_input)
    
#     # LangGraph 내부 상태는 모름
#     # 대신 surface metadata만 리턴
#     return {
#         "status": "running",
#         "progress": result.get("progress"),
#         "checkpoint_id": result.get("checkpoint_id"),
#         "answer": result.get("answer")
#     }