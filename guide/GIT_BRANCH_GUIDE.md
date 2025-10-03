# 🌿 깃 브랜치 사용 가이드

이 문서는 우리 프로젝트에서 **브랜치를 어떻게 나누고 쓰는지** 설명합니다.  
복잡한 용어는 최소화했으니 그대로 따라 하면 됩니다.

---

## 📂 브랜치 역할

- **main**
  - 최종 배포용 브랜치입니다.
  - 실제 개발이 모이는 중심 브랜치입니다.
  - 모든 작업 브랜치(feat/fix/refactor)는 여기서 만들어집니다.
  - 작업을 끝내면 이 브랜치에 합칩니다.

- **feat/**  
  - 새로운 기능을 만들 때 사용합니다.  
  - 예: `feat/letter-service`
  - `feat/*`의 *는 파일명이 아니라 기능 단위로 적어주세요.

- **fix/**  
  - 버그를 고칠 때 사용합니다.  
  - 예: `fix/login-bug`
  - `fix/*`의 *는 파일명이 아니라 기능 단위로 적어주세요.

- **refactor/**  
  - 기능은 그대로 두고 코드 구조만 정리할 때 사용합니다.  
  - 예: `refactor/ai-proxy`
  - `refactor/*`의 *는 파일명이 아니라 기능 단위로 적어주세요.

---

## 🛠️ 작업 순서

### 1. 최초 작업 시작하기
```bash
git checkout main        # develop 브랜치로 이동
git pull origin main     # 최신 코드로 업데이트
git checkout -b feat/기능명   # 새 브랜치 생성
```

### 2. 코드 작성 후 저장하기
```
git add .   
git commit
- "feat: 편지 전송 기능 추가" 작성
```

### 3. 작업 끝내고 main 에 합치고 기존 브랜치 삭제
```
git checkout develop
git pull origin develop
git merge feat/기능이름
git push origin develop
git branch -d feat/기능이름   # 사용 끝난 브랜치 삭제
```
---
## ✅ 브랜치 머지 순서

작업이 겹치지 않게 다음 순서를 지켜주세요:

1. 'fix/*' -> 버그 수정 먼저 합치기
2. 'feat/*' -> 새로운 기능 합치기
3. 'refactor/*' -> 마지막에 코드 정리하기


---
## 📋 커밋 메시지 규칙
- 버그 수정:   
```feat: 편지 전송 기능 추가```

- 새로운 기능:   
```fix: 로그인 오류 수정```

- 코드 정리::   
```refactor: AI 프록시 코드 리팩토링```