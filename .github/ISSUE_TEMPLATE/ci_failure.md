---
title: "[🚨 CI Failure] 테스트 실패 리포트"
labels: bug, ci-failure
assignees: ''
---

## 🚨 CI/CD 파이프라인에서 오류가 발생했습니다!

워크플로우가 코드 또는 에이전트를 테스트하던 중 실패(Failure)를 반환했습니다.
아래 로그를 확인하고, 원인을 분석해 주세요.

### 📝 실패한 워크플로우 정보
- **Repository:** {{ env.GITHUB_REPOSITORY }}
- **Workflow:** {{ env.GITHUB_WORKFLOW }}
- **Run ID:** [{{ env.GITHUB_RUN_ID }}](https://github.com/{{ env.GITHUB_REPOSITORY }}/actions/runs/{{ env.GITHUB_RUN_ID }})
- **Triggering Actor:** {{ env.GITHUB_ACTOR }}

### 📋 상세 로그 및 확인 방법
위의 [Run ID 링크]를 클릭하시면 깃허브 액션 대시보드로 이동하여 상세한 에러 로그(Traceback)를 확인할 수 있습니다.
API 할당량 초과(Quota Error), 파이썬 문법 오류, 의존성 충돌 등이 주요 원인일 수 있습니다.

> 🤖 **Human-in-the-Loop:** 에러가 해결되면, 문제가 된 코드를 수정 후 재커밋(Push)하여 해당 워크플로우가 정상 통과하는지 꼭 다시 확인해 주세요!
