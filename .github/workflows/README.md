# 🏷️ GitHub Actions Naming Conventions

본 저장소의 `.github/workflows/` 디렉토리에 위치하는 워크플로우 파일들은 목적과 성격을 쉽게 파악하기 위해 아래와 같은 접두사(Prefix) 규칙을 따릅니다.

## 📂 Prefix Rules (접두사 룰)

### 1. `agent_*` (AI 에이전트 실행)
- **역할**: 실제로 데이터를 수집, 분석, 가공하여 위키(마크다운) 콘텐츠를 생성하거나 외부로 브리핑을 보내는 AI 에이전트 봇 워크플로우입니다.
- **예시**: `agent_news_summarizer.yml`, `agent_youtube_summarizer.yml`

### 2. `ops_*` (운영 자동화 및 IssueOps)
- **역할**: 깃허브 이슈(Issue)나 코멘트 등을 트리거로 삼아, 프로젝트 설정(`config.json`)을 업데이트하거나 에이전트의 작동 방식을 변경하는 운영 스크립트입니다.
- **예시**: `ops_update_topic.yml`

### 3. `sys_*` (시스템 CI/CD)
- **역할**: 저장소의 코드 안정성을 검증(Test, Lint, Build)하거나 배포 파이프라인을 담당하는 전통적인 CI/CD 워크플로우입니다.
- **예시**: `sys_ci.yml`, `sys_pytest.yml`

### 4. `tmpl_*` (재사용 템플릿)
- **역할**: `agent_*` 등의 다른 워크플로우들이 공통으로 가져다 쓰는(Reusable) 부모 워크플로우 템플릿입니다. 단독으로 실행되지 않고 `uses:` 키워드를 통해 호출됩니다.
- **예시**: `tmpl_python_agent.yml`

---

## 🛠 새로운 에이전트 추가 가이드
새로운 파이썬 기반 에이전트를 추가하고 싶다면, 파이썬 환경 설정과 의존성 설치, 커밋 과정을 일일이 작성할 필요가 없습니다.

1. `agent_{새로운에이전트}.yml` 파일을 생성합니다.
2. 아래와 같이 `tmpl_python_agent.yml` 템플릿을 호출합니다.

```yaml
jobs:
  run-new-agent:
    uses: ./.github/workflows/tmpl_python_agent.yml
    with:
      working_directory: '_source/Projects/NewAgentFolder'
      script_command: 'python run.py'
      commit_message: "📝 새로운 봇의 작업 결과물 자동 추가"
      file_pattern: "path/to/save/*.md"
    secrets: inherit
```
