"LLM Wiki"라는 개념 자체가 최근에 재정의됐습니다 — 참고로 말씀드리면

2026년 4월, Andrej Karpathy(전 OpenAI 공동창업자)가 llm-wiki.md라는 짧은 gist를 올리면서 "LLM Wiki" 패턴이 화제가 됐습니다. 일반 RAG가 질문마다 원문 조각을 매번 다시 검색하는 방식이라면, LLM Wiki는 소스를 한 번 컴파일해서 서로 링크된 영구적인 페이지로 만들고 점진적으로 업데이트하는 방식입니다. 그리고 흥미롭게도, 활성화된 오픈소스 프로젝트들이 공통적으로 목표하는 저장 형식이 바로 Obsidian 호환 마크다운([[wikilinks]] + YAML frontmatter)입니다 — 지금 키호님이 만들고 계신 Vault 구조가 이미 이 트렌드와 정확히 맞아떨어집니다. 
Tericsoft + 2

설치 가능한 사이트/도구 — 용도별로 정리
1. 지금 Vault에 바로 설치 (가장 쉬움, 서버 불필요)

Obsidian 플러그인 방식 — 별도 사이트 설치 없이 Community Plugins에서 검색:

Smart Connections — Vault 내 노트 간 의미 기반 연결/검색, 로컬 임베딩 + 외부 LLM 선택 가능
Copilot for Obsidian — Claude API 연결해서 Vault 전체에 대해 채팅형 질의응답

이게 개인 Vault(집 PC)용으로는 제일 빠른 시작점입니다.

2. 독립 실행형 셀프호스팅 (실제 "Wiki Mode" 지원)
사이트	특징
github.com/Tencent/WeKnora	원문서를 RAG 질의응답, 자율 추론 에이전트, 그리고 서로 링크된 마크다운 지식베이스로 자동 정리하는 "Wiki Mode"까지 갖춘 오픈소스. 
GitHub
 로컬/프라이빗 클라우드 배포로 데이터 완전 통제 가능 
GitHub

xwiki.org	프라이버시 우선 엔터프라이즈용, bring-your-own-LLM 지원 
Slite
 — 회사에서 승인된 Qwen/GLM 같은 자체 LLM을 붙일 수 있어 사내 LLM Wiki 후보로 적합
Onyx (전 Danswer)	50개 이상 소스를 연결하는 하이브리드 검색 + agentic RAG, 
Slite
 오픈소스 셀프호스팅
3. 프레임워크 (직접 파이프라인 구축하고 싶을 때)
LlamaIndex, LangChain — RAG 파이프라인 직접 구성
LightRAG / GraphRAG — 지식 그래프 기반, 사실 관계 변화 추적까지 지원하는 더 발전된 형태 
Forwardic
키호님 상황에 대입하면
용도	추천
개인 LLM Wiki (집 PC, 지금 바로)	Obsidian 플러그인(Smart Connections / Copilot) — 이미 있는 Vault 그대로 활용
개인 고도화 (나중, ChromaDB 로드맵과 연결)	WeKnora — Wiki Mode가 정확히 지금 목표(자동 정리되는 지식베이스)와 일치
회사 LLM Wiki (Qwen/GLM 기반, 사내 승인 LLM만)	xWiki (bring-your-own-LLM) 또는 자체 구축(LlamaIndex + 사내 LLM)

주의: 회사용으로 검토하시는 도구는 반드시 완전 로컬/온프레미스 배포가 가능한지 확인이 우선입니다 — SaaS형(Glean, Notion AI 등)은 지난번 세운 "회사 데이터 외부 반출 금지" 원칙과 바로 충돌합니다.

✅ Next Action
 개인용: Obsidian Community Plugins에서 Smart Connections 또는 Copilot for Obsidian 설치 테스트
 회사용: WeKnora/xWiki가 사내 네트워크(Model API 직접 호출 제약)에서 로컬 LLM(Qwen/GLM)과 연동 가능한지 사내 검토
 Study/AI-활용법 폴더에 이번 검색 내용(LLM Wiki 개념, 도구 비교) 노트로 정리해두시면 나중에 도구 선택 시 참고자료로 유용