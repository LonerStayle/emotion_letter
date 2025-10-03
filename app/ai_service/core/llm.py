"""
vLLM와 OpenAI API를 이용한 AI 서비스 구현 코드 예시 입니다.
(서빙)
"""

# from vllm import LLM, SamplingParams
# from openai import OpenAI

# class VLLMClient:
#     def __init__(self, model_name: str = "facebook/opt-125m"):
#         """
#         vLLM으로 로컬 모델 서빙
#         """
#         self.llm = LLM(model=model_name)

#     def generate(self, prompt: str, max_tokens: int = 128, temperature: float = 0.7):
#         params = SamplingParams(temperature=temperature, max_tokens=max_tokens)
#         outputs = self.llm.generate([prompt], params)
#         return outputs[0].outputs[0].text



# class OpenAIClient:
#     def __init__(self, model_name: str = "gpt-4o-mini"):
#         self.client = OpenAI()
#         self.model_name = model_name

#     def generate(self, prompt: str, max_tokens: int = 128, temperature: float = 0.7):
#         response = self.client.chat.completions.create(
#             model=self.model_name,
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=max_tokens,
#             temperature=temperature
#         )
#         return response.choices[0].message.content

