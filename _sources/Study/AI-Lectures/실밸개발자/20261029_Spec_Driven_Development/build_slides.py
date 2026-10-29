#!/usr/bin/env python3
"""
Slide & Report Builder for Spec-Driven Development Lecture
Generates:
1. slides/ (01_intro.html ~ 10_domain_takeaways.html, index.html)
2. lecture_report.html (Interactive Single Dashboard Report)
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SLIDES_DIR = os.path.join(BASE_DIR, "slides")
os.makedirs(SLIDES_DIR, exist_ok=True)

COMMON_CSS = """
:root {
  --bg: #0a0f1a;
  --card-bg: rgba(18, 26, 43, 0.7);
  --card-border: rgba(139, 148, 158, 0.16);
  --accent-primary: #7c3aed;
  --accent-cyan: #38bdf8;
  --accent-gradient: linear-gradient(135deg, #7c3aed 0%, #38bdf8 100%);
  --text-main: #f0f6fc;
  --text-muted: #8b949e;
  --font-sans: 'Pretendard', 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', Consolas, Monaco, monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background-color: var(--bg);
  color: var(--text-main);
  font-family: var(--font-sans);
  line-height: 1.6;
  overflow-x: hidden;
}

.gradient-text {
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  padding: 24px;
  backdrop-filter: blur(12px);
  margin-bottom: 20px;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(124, 58, 237, 0.15);
  color: #a78bfa;
  border: 1px solid rgba(124, 58, 237, 0.3);
  margin-right: 8px;
}

.badge-cyan {
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.code-box {
  background: #060911;
  border: 1px solid rgba(139, 148, 158, 0.2);
  border-radius: 8px;
  padding: 16px;
  font-family: var(--font-mono);
  font-size: 0.88rem;
  color: #e6edf3;
  overflow-x: auto;
  position: relative;
  margin: 14px 0;
}

.copy-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(139, 148, 158, 0.15);
  border: 1px solid rgba(139, 148, 158, 0.3);
  color: #c9d1d9;
  border-radius: 6px;
  padding: 4px 10px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}
.copy-btn:hover {
  background: var(--accent-primary);
  color: #fff;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 0.9rem;
}
th, td {
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid var(--card-border);
}
th {
  background: rgba(124, 58, 237, 0.1);
  color: #c4b5fd;
  font-weight: 600;
}
tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}
"""

SLIDES_DATA = [
    {
        "id": "01_intro",
        "title": "AI 시대의 새로운 패러다임: Spec-Driven Development",
        "subtitle": "실밸개발자 (메타 시니어 엔지니어) 초청 세미나 핵심 요약",
        "content": """
        <div class="card">
          <div style="margin-bottom: 16px;">
            <span class="badge">패스트캠퍼스 무료 공개</span>
            <span class="badge badge-cyan">하네스 프레임워크 실전</span>
            <span class="badge">러닝타임 61분 전수 분석</span>
          </div>
          <h2 style="font-size: 1.8rem; margin-bottom: 16px;">"스펙만 썼는데 AI가 앱을 30분 만에 다 만들었습니다"</h2>
          <p style="color: var(--text-muted); font-size: 1.05rem; margin-bottom: 24px;">
            전통적인 TDD의 한계를 극복하고, 자연어 스펙을 선행 작성하여 에이전트가 <strong>계획 ➡️ 구현 ➡️ 자율 교정</strong>까지 완주하도록 지휘하는 AI-Native 엔지니어링 패러다임.
          </p>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
            <div style="background: rgba(124, 58, 237, 0.08); padding: 16px; border-radius: 8px; border-left: 3px solid var(--accent-primary);">
              <h4 style="color: #c4b5fd; margin-bottom: 6px;">🎯 핵심 주제</h4>
              <p style="font-size: 0.9rem; color: #d1d5db;">TDD가 실패하는 모호한 영역에서 SDD로 자율 소프트웨어 개발 루프 구축</p>
            </div>
            <div style="background: rgba(56, 189, 248, 0.08); padding: 16px; border-radius: 8px; border-left: 3px solid var(--accent-cyan);">
              <h4 style="color: #7dd3fc; margin-bottom: 6px;">⚙️ 오픈소스 하네스</h4>
              <p style="font-size: 0.9rem; color: #d1d5db;"><code>jha0313/harness_framework</code> (Claude Code + Python Orchestrator)</p>
            </div>
            <div style="background: rgba(16, 185, 129, 0.08); padding: 16px; border-radius: 8px; border-left: 3px solid #10b981;">
              <h4 style="color: #6ee7b7; margin-bottom: 6px;">🛡️ 메인 컨텍스트 방어</h4>
              <p style="font-size: 0.9rem; color: #d1d5db;"><code>claude -p</code> 헤드리스 독립 서브세션으로 컨텍스트 블로트 100% 원천 차폐</p>
            </div>
          </div>
        </div>
        """
    },
    {
        "id": "02_tdd_vs_sdd",
        "title": "TDD의 한계 vs SDD (Spec-Driven Development)",
        "subtitle": "언제 TDD를 쓰고, 언제 SDD로 전환해야 하는가?",
        "content": """
        <div class="card">
          <h3 style="color: #38bdf8; margin-bottom: 14px;">⚖️ 패러다임 비교 매트릭스</h3>
          <table>
            <thead>
              <tr>
                <th>구분</th>
                <th>TDD (Test-Driven Development)</th>
                <th>SDD (Spec-Driven Development)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>작동 전제</strong></td>
                <td>"어떻게 동작해야 하는가"가 이미 명확한 작업</td>
                <td><strong>"무엇을 만들어야 하는가"부터 모호한 신규 작업</strong></td>
              </tr>
              <tr>
                <td><strong>최적 적용처</strong></td>
                <td>단일 함수, 버그 수정, 레거시 인터페이스 리팩토링</td>
                <td>신규 SaaS, 모듈 아키텍처 기획, 복잡한 통신 프로토콜 설계</td>
              </tr>
              <tr>
                <td><strong>핵심 병목</strong></td>
                <td>테스트 케이스 선행 작성 및 코드 구현</td>
                <td><strong>자연어 스펙 정의(Design) 및 에이전트 출력 검토(Review)</strong></td>
              </tr>
              <tr>
                <td><strong>AI와의 관계</strong></td>
                <td>AI가 테스트 먼저 안 짜고 코드부터 짜서 탈선</td>
                <td>AI에게 스펙 기반 Step 분할과 자율 교정 루프 위임</td>
              </tr>
            </tbody>
          </table>
          <div style="margin-top: 18px; padding: 14px; background: rgba(239, 68, 68, 0.08); border-radius: 8px; border-left: 3px solid #ef4444;">
            <strong style="color: #fca5a5;">⚠️ TDD의 치명적 약점:</strong>
            <p style="font-size: 0.88rem; color: #e5e7eb; margin-top: 4px;">새로운 도메인이나 미지의 프로덕트를 시작할 때, 테스트를 먼저 쓰려고 하면 무엇을 검증할지 몰라 개발이 완전히 멈추게 됨. 합의된 스펙(Spec)이 선행되어야 함.</p>
          </div>
        </div>
        """
    },
    {
        "id": "03_five_mindsets",
        "title": "SDD가 작동하기 위한 5가지 사고방식 전환",
        "subtitle": "도구를 쥐어줘도 생각이 바뀌지 않으면 과거 방식으로 회귀한다",
        "content": """
        <div class="card">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 18px; border-radius: 10px;">
              <span class="badge">01</span><strong style="font-size: 1.05rem; color: #c4b5fd;">Spec First, Code Second</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 8px;">코드를 건드리기 전에 명확한 자연어 스펙을 작성하라. 모호한 프롬프트는 무한 수정 핑퐁의 주범이다.</p>
            </div>
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 18px; border-radius: 10px;">
              <span class="badge badge-cyan">02</span><strong style="font-size: 1.05rem; color: #7dd3fc;">Reviewer, Not Author</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 8px;">인간은 더 이상 코더가 아니다. 코딩은 AI에 넘기고, 인간은 아키텍처·엣지케이스·도메인 맥락의 판사가 된다.</p>
            </div>
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 18px; border-radius: 10px;">
              <span class="badge">03</span><strong style="font-size: 1.05rem; color: #c4b5fd;">Externalize Mental Context</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 8px;">머릿속 암묵지(패턴, 컨벤션, 의도)를 꺼내 문서화(CLAUDE.md, ADR)하라. 외부화되지 않은 지식은 AI가 알 수 없다.</p>
            </div>
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 18px; border-radius: 10px;">
              <span class="badge badge-cyan">04</span><strong style="font-size: 1.05rem; color: #7dd3fc;">Attention on Front-end (Design)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 8px;">엔지니어 100명 몫을 AI가 코딩하므로 코딩은 더 이상 병목이 아니다. 인간의 시간은 스펙 설계에 80% 쏟아야 한다.</p>
            </div>
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 18px; border-radius: 10px; grid-column: span 2;">
              <span class="badge" style="background: #10b98122; color: #6ee7b7; border-color: #10b98144;">05</span><strong style="font-size: 1.05rem; color: #6ee7b7;">Closed Learning Loop (복리 성장)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 8px;">AI의 실패는 환경 개선의 기회다. 실패 원인을 CLAUDE.md 가드레일이나 스킬로 승격시켜 시스템을 업그레이드하라. <strong>50번째 세션은 첫 번째 세션보다 압도적으로 생산적이어야 한다.</strong></p>
            </div>
          </div>
        </div>
        """
    },
    {
        "id": "04_five_step_loop",
        "title": "SDD 5단계 라이프사이클 루프",
        "subtitle": "설계 ➡️ 계획 ➡️ 구현 ➡️ 교정 ➡️ 회고의 협업 매트릭스",
        "content": """
        <div class="card">
          <div style="display: flex; flex-direction: column; gap: 12px;">
            <div style="display: flex; align-items: center; background: rgba(124, 58, 237, 0.1); padding: 14px; border-radius: 8px;">
              <div style="width: 120px; font-weight: bold; color: #c4b5fd;">1. 설계 (Design)</div>
              <div style="width: 140px;"><span class="badge">인간 주도 / AI 보조</span></div>
              <div style="flex: 1; font-size: 0.88rem; color: #e5e7eb;">무엇을 왜 만드는지, 아키텍처, 기술 결정(ADR), 도메인 조직 제약을 문서화</div>
            </div>
            <div style="display: flex; align-items: center; background: rgba(56, 189, 248, 0.1); padding: 14px; border-radius: 8px;">
              <div style="width: 120px; font-weight: bold; color: #38bdf8;">2. 계획 (Plan)</div>
              <div style="width: 140px;"><span class="badge badge-cyan">AI 주도 / 인간 승인</span></div>
              <div style="flex: 1; font-size: 0.88rem; color: #e5e7eb;">스펙 문서를 바탕으로 AI가 작업을 작은 단위의 Step으로 분할하고 계획 수립</div>
            </div>
            <div style="display: flex; align-items: center; background: rgba(16, 185, 129, 0.1); padding: 14px; border-radius: 8px;">
              <div style="width: 120px; font-weight: bold; color: #6ee7b7;">3. 구현 (Execute)</div>
              <div style="width: 140px;"><span class="badge" style="background:#10b98122; color:#6ee7b7;">AI 전권 자율</span></div>
              <div style="flex: 1; font-size: 0.88rem; color: #e5e7eb;">각 Step별 독립 헤드리스 세션에서 컴파일 및 AC 테스트 통과 시까지 자율 코딩</div>
            </div>
            <div style="display: flex; align-items: center; background: rgba(245, 158, 11, 0.1); padding: 14px; border-radius: 8px;">
              <div style="width: 120px; font-weight: bold; color: #fcd34d;">4. 교정 (Correct)</div>
              <div style="width: 140px;"><span class="badge" style="background:#f59e0b22; color:#fcd34d;">인간 주도 피드백</span></div>
              <div style="flex: 1; font-size: 0.88rem; color: #e5e7eb;">결과물 검토, 에러 처리 매트릭스 확인 및 아키텍처 준수 여부 심사</div>
            </div>
            <div style="display: flex; align-items: center; background: rgba(236, 72, 153, 0.1); padding: 14px; border-radius: 8px;">
              <div style="width: 120px; font-weight: bold; color: #f472b6;">5. 회고 (Reflect)</div>
              <div style="width: 140px;"><span class="badge" style="background:#ec489922; color:#f472b6;">인간 주도 자산화</span></div>
              <div style="flex: 1; font-size: 0.88rem; color: #e5e7eb;">AI 반성문에서 도출된 교훈을 CLAUDE.md 규칙 및 하네스 프레임워크로 영구 반영</div>
            </div>
          </div>
        </div>
        """
    },
    {
        "id": "05_good_spec_5elements",
        "title": "좋은 스펙의 5가지 핵심 요소",
        "subtitle": "스펙은 길 필요가 없다. 이 5가지만 명확하면 직행한다",
        "content": """
        <div class="card">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px;">
            <div style="padding: 16px; background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); border-radius: 8px;">
              <strong style="color: #c4b5fd;">1. Inputs & Outputs (입출력)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">명확한 입력 데이터 구조와 관측 가능한 기대 출력 정의 (예: 프롬프트+이미지 ➡️ 16:9 썸네일 2개)</p>
            </div>
            <div style="padding: 16px; background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); border-radius: 8px;">
              <strong style="color: #38bdf8;">2. Success Criteria (성공 기준)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">정량적으로 측정 가능한 성공 척도 (예: 응답시간 < 2초, 빌드 에러 0개, 테스트 커버리지)</p>
            </div>
            <div style="padding: 16px; background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); border-radius: 8px;">
              <strong style="color: #6ee7b7;">3. Constraints (제약 조건)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">보안, 라이브러리 제한, 외부 API 호출 전용 라우트 강제 등 절대 넘지 말아야 할 기술적 경계</p>
            </div>
            <div style="padding: 16px; background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); border-radius: 8px;">
              <strong style="color: #fcd34d;">4. Scope & Out-of-Scope (범위)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">이번 MVP에서 <strong>"절대 하지 않을 것"</strong>을 명시. AI 특유의 과도한 오버엔지니어링 원천 차단</p>
            </div>
            <div style="padding: 16px; background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); border-radius: 8px; grid-column: span 2;">
              <strong style="color: #f87171;">5. Edge Cases (예외 및 에러 핸들링)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">API Rate Limit, 네트워크 단절, 잘못된 사용자 입력 시의 조건부 재시도 및 UI 폴백 매트릭스</p>
            </div>
          </div>
        </div>
        """
    },
    {
        "id": "06_spec_checklist_hierarchy",
        "title": "계층형 스펙(Hierarchical Specs) & AI 슬롭 방지",
        "subtitle": "프로젝트가 커질 때의 스펙 관리와 시니어 엔지니어의 품격",
        "content": """
        <div class="card">
          <h3 style="color: #38bdf8; margin-bottom: 12px;">🏗️ 프로젝트 확장 시: 계층형 스펙 분할</h3>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 16px;">
            단일 대형 스펙 파일은 컨텍스트 압축 과정에서 유실됨. <strong>마스터 스펙</strong> 아래 <strong>컴포넌트 스펙</strong>을 계층형으로 분리하여 단일 세션 크기로 관리.
          </p>
          <div style="background: rgba(18, 26, 43, 0.9); padding: 16px; border-radius: 8px; font-family: var(--font-mono); font-size: 0.85rem; color: #a78bfa; margin-bottom: 20px;">
            Master Spec (전체 비전 & 아키텍처 규칙)<br>
            ├── Phase 0: MVP Spec (기본 골격 및 핵심 API)<br>
            ├── Phase 1: Authentication & User Spec<br>
            └── Phase 2: Analytics & Batch Job Spec
          </div>
          <h3 style="color: #f87171; margin-bottom: 12px;">🚫 docs/UI_GUIDE.md — AI 슬롭(AI Slop) 7대 안티패턴 금지</h3>
          <table>
            <thead>
              <tr>
                <th>금지 항목</th>
                <th>금지 사유</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>backdrop-filter: blur()</code></td>
                <td>글래스모피즘은 AI 템플릿의 가장 흔하고 뻔한 징후</td>
              </tr>
              <tr>
                <td><code>gradient-text</code> (배경 그라데이션)</td>
                <td>AI가 찍어낸 SaaS 랜딩 페이지의 전형적 특징</td>
              </tr>
              <tr>
                <td>"Powered by AI" 배지</td>
                <td>기능이 아니라 무가치한 장식. 사용자에게 무의미함</td>
              </tr>
              <tr>
                <td>보라/인디고 브랜드 색상 클리셰</td>
                <td>"AI = 보라색"이라는 식상한 템플릿 색상</td>
              </tr>
            </tbody>
          </table>
        </div>
        """
    },
    {
        "id": "07_harness_framework_architecture",
        "title": "Harness Framework 구조 및 4대 핵심 문서",
        "subtitle": "jha0313/harness_framework 리포지토리 완전 해부",
        "content": """
        <div class="card">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px;">
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 16px; border-radius: 8px;">
              <strong style="color: #c4b5fd;">1. PRD.md</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">제품 요구사항 정의서. 목표, 타겟 사용자 페르소나, 핵심 기능, MVP 제외 사항.</p>
            </div>
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 16px; border-radius: 8px;">
              <strong style="color: #38bdf8;">2. ARCHITECTURE.md</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">디렉토리 구조, 디자인 패턴, 컴포넌트 간 데이터 흐름, 서버/클라이언트 상태 관리.</p>
            </div>
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 16px; border-radius: 8px;">
              <strong style="color: #fcd34d;">3. ADR.md (Architecture Decision Records)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">선택, 선택 이유, 포기한 트레이드오프 기록. 에이전트의 임의 구조 파괴 원천 방지.</p>
            </div>
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 16px; border-radius: 8px;">
              <strong style="color: #6ee7b7;">4. CLAUDE.md</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">기술 스택, 절대 지켜야 할 CRITICAL 규칙, 빌드/테스트 명령어, 커밋 컨벤션.</p>
            </div>
          </div>
          <div style="margin-top: 16px; background: rgba(124, 58, 237, 0.08); padding: 14px; border-radius: 8px; border-left: 3px solid var(--accent-primary);">
            <strong style="color: #c4b5fd;">💡 ADR이 가장 중요한 이유:</strong>
            <p style="font-size: 0.88rem; color: #d1d5db; margin-top: 4px;">모든 기술 선택에는 이유와 포기한 것(트레이드오프)이 있다. 이 의도를 문서화하지 않으면 다음 에이전트 세션이 임의로 아키텍처를 뒤엎는다.</p>
          </div>
        </div>
        """
    },
    {
        "id": "08_claude_p_headless_session",
        "title": "claude -p 헤드리스 모드 & 컨텍스트 격리",
        "subtitle": "메인 세션의 컨텍스트 윈도우 오염(Context Bloat)을 극복하는 열쇠",
        "content": """
        <div class="card">
          <h3 style="color: #f87171; margin-bottom: 12px;">⚠️ 메인 컨텍스트가 커지는 걸 두려워해야 하는 이유</h3>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 16px;">
            단일 대화 세션에서 Step 1부터 7까지 계속 구현을 시키면 컨텍스트가 120k~150k로 누적되며 성능이 급격히 붕괴함. Step 6~7에 작성된 코드는 사실상 버려야 할 수준이 됨.
          </p>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); padding: 16px; border-radius: 8px;">
              <strong style="color: #fca5a5;">❌ 대화형 세션 단일 실행 (Bad)</strong>
              <ul style="font-size: 0.85rem; color: #d1d5db; margin-top: 8px; padding-left: 18px;">
                <li>Step이 진행될수록 이전 로그와 코드가 누적됨</li>
                <li>150k 토큰 초과 시 환각 및 규칙 망각 발생</li>
                <li>비용 폭증 및 응답 속도 극심한 저하</li>
              </ul>
            </div>
            <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); padding: 16px; border-radius: 8px;">
              <strong style="color: #6ee7b7;">✅ claude -p 헤드리스 서브프로세스 (Good)</strong>
              <ul style="font-size: 0.85rem; color: #d1d5db; margin-top: 8px; padding-left: 18px;">
                <li>Step마다 깨끗한 1회용 독립 세션 기동</li>
                <li>이전 Step의 1줄 <code>summary</code>와 핵심 문서만 주입</li>
                <li>메인 컨텍스트는 0k 유지, 성능 100% 보존</li>
              </ul>
            </div>
          </div>
          <div class="code-box">
            <span style="color: #8b949e;"># execute.py 내부 독립 세션 실행 커맨드</span><br>
            claude -p --dangerously-skip-permissions --output-format json &quot;{preamble + step_prompt}&quot;
          </div>
        </div>
        """
    },
    {
        "id": "09_execute_py_orchestrator",
        "title": "scripts/execute.py 오케스트레이터 분석",
        "subtitle": "Preamble 가드레일, 3회 자가교정, 2단계 원자적 커밋",
        "content": """
        <div class="card">
          <h3 style="color: #38bdf8; margin-bottom: 14px;">⚙️ execute.py 4대 핵심 메커니즘</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); padding: 16px; border-radius: 8px;">
              <strong style="color: #c4b5fd;">1. 가드레일 & 컨텍스트 주입</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">매 세션마다 CLAUDE.md + docs/*.md + 이전 완료 Step들의 1줄 요약(summary)을 Preamble로 자동 합성</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); padding: 16px; border-radius: 8px;">
              <strong style="color: #38bdf8;">2. 3회 자가교정 루프 (Self-Correction)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">AC 실패 시 최대 3회 재시도. 이전 실패 에러 메시지(prev_error)를 다음 프롬프트에 자동 주입하여 스스로 수정</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); padding: 16px; border-radius: 8px;">
              <strong style="color: #6ee7b7;">3. 원자적 2단계 커밋 (Atomic Commits)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">코드 변경(feat: step N)과 관리 메타데이터(chore: step N output)를 분리하여 Git 히스토리 청결성 유지</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); padding: 16px; border-radius: 8px;">
              <strong style="color: #fcd34d;">4. 명확한 상태 전이 및 차단 감지</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">pending ➡️ completed, error, blocked. API 키나 수동 작업 필요 시 blocked 상태로 즉시 사용자 개입 요청</p>
            </div>
          </div>
          <div class="code-box">
            <span style="color: #8b949e;"># 실행 명령어</span><br>
            python3 scripts/execute.py 0-mvp --push
          </div>
        </div>
        """
    },
    {
        "id": "10_domain_takeaways",
        "title": "그룹장 실무 적용: 임베디드 SW & PHY 계층 SDD",
        "subtitle": "모바일 통신 프로토콜 / PHY Layer C/C++ 하네스 프레임워크 설계",
        "content": """
        <div class="card">
          <h3 style="color: #38bdf8; margin-bottom: 14px;">📡 모바일 SW 통신 프로토콜 그룹 맞춤 실무 적용</h3>
          <div style="display: flex; flex-direction: column; gap: 14px;">
            <div style="background: rgba(124, 58, 237, 0.08); padding: 16px; border-radius: 8px; border-left: 3px solid var(--accent-primary);">
              <h4 style="color: #c4b5fd;">1. HW 레지스터 맵 기반 C/C++ 임베디드 하네스 구축</h4>
              <p style="font-size: 0.88rem; color: #d1d5db; margin-top: 4px;">
                신규 모뎀/RFIC 레지스터 맵 CSV를 <code>docs/PRD.md</code>(비트필드, 오프셋)로 정의 ➡️ <code>execute.py</code>가 C 구조체 헤더 생성 ➡️ 읽기/쓰기 인라인 함수 ➡️ QEMU/호스트 단위 시뮬레이션 AC 검증까지 자동화.
              </p>
            </div>
            <div style="background: rgba(56, 189, 248, 0.08); padding: 16px; border-radius: 8px; border-left: 3px solid var(--accent-cyan);">
              <h4 style="color: #7dd3fc;">2. 3GPP 프로토콜 스택의 계층형 스펙(Hierarchical Spec) 분할</h4>
              <p style="font-size: 0.88rem; color: #d1d5db; margin-top: 4px;">
                수만 줄의 통신 규격을 통째로 주입하지 않고, Master Spec(전체 아키텍처) 아래 L1 PHY(디코딩), L2 MAC(HARQ), L3 RRC(상태 머신)로 모듈을 분할하여 컨텍스트 압축 없는 정밀 구현.
              </p>
            </div>
            <div style="background: rgba(16, 185, 129, 0.08); padding: 16px; border-radius: 8px; border-left: 3px solid #10b981;">
              <h4 style="color: #6ee7b7;">3. JIRA / 필드 이슈 분석 자동 회고 루프</h4>
              <p style="font-size: 0.88rem; color: #d1d5db; margin-top: 4px;">
                필드 Drop call 또는 CRC 에러 로그를 분석한 뒤, 일회성 패치로 끝내지 않고 <code>docs/ADR.md</code> 및 <code>CLAUDE.md</code>에 동기화 타이밍 제약 규칙을 영구 반영하여 복리 개선.
              </p>
            </div>
          </div>
        </div>
        """
    }
]

# Generate individual slide files
for i, slide in enumerate(SLIDES_DATA):
    prev_id = SLIDES_DATA[i - 1]["id"] if i > 0 else None
    next_id = SLIDES_DATA[i + 1]["id"] if i < len(SLIDES_DATA) - 1 else None
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{slide['title']} | SDD Slide {i+1}</title>
  <style>
    {COMMON_CSS}
    .slide-container {{
      max-width: 960px;
      margin: 40px auto;
      padding: 0 20px;
      min-height: calc(100vh - 120px);
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .slide-header {{
      margin-bottom: 24px;
    }}
    .slide-nav {{
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 16px;
      background: rgba(18, 26, 43, 0.9);
      padding: 10px 24px;
      border-radius: 9999px;
      border: 1px solid var(--card-border);
      backdrop-filter: blur(12px);
      z-index: 100;
    }}
    .nav-btn {{
      background: none;
      border: none;
      color: var(--text-main);
      font-size: 1.1rem;
      cursor: pointer;
      text-decoration: none;
      padding: 4px 8px;
      border-radius: 6px;
      transition: background 0.2s;
    }}
    .nav-btn:hover {{ background: rgba(255,255,255,0.1); }}
    .nav-indicator {{ font-size: 0.85rem; color: var(--text-muted); font-family: var(--font-mono); }}
  </style>
</head>
<body>
  <div class="slide-container">
    <div class="slide-header">
      <div style="font-size: 0.85rem; font-weight: 600; color: #a78bfa; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">
        Slide {i+1} of {len(SLIDES_DATA)}
      </div>
      <h1 style="font-size: 2.2rem; margin-bottom: 8px;">{slide['title']}</h1>
      <p style="color: var(--text-muted); font-size: 1.1rem;">{slide['subtitle']}</p>
    </div>
    {slide['content']}
  </div>

  <div class="slide-nav">
    {"<a href='" + prev_id + ".html' class='nav-btn'>&larr; 이전</a>" if prev_id else "<span style='opacity:0.3;' class='nav-btn'>&larr; 이전</span>"}
    <span class="nav-indicator">{i+1} / {len(SLIDES_DATA)}</span>
    {"<a href='" + next_id + ".html' class='nav-btn'>다음 &rarr;</a>" if next_id else "<span style='opacity:0.3;' class='nav-btn'>다음 &rarr;</span>"}
    <a href="../lecture_report.html" class="nav-btn" style="border-left: 1px solid var(--card-border); padding-left: 12px; margin-left: 6px; font-size: 0.85rem; color: #38bdf8;">전체 리포트 보기</a>
  </div>

  <script>
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowLeft' && '{prev_id}' !== 'None') {{
        window.location.href = '{prev_id}.html';
      }} else if (e.key === 'ArrowRight' && '{next_id}' !== 'None') {{
        window.location.href = '{next_id}.html';
      }}
    }});
  </script>
</body>
</html>"""
    
    with open(os.path.join(SLIDES_DIR, f"{slide['id']}.html"), "w", encoding="utf-8") as f:
        f.write(html)

# Index slide (hub)
index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>Spec-Driven Development 슬라이드 허브</title>
  <style>
    {COMMON_CSS}
    .container {{ max-width: 900px; margin: 60px auto; padding: 0 20px; }}
    .slide-item {{
      display: flex;
      align-items: center;
      padding: 16px 20px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      margin-bottom: 12px;
      text-decoration: none;
      color: var(--text-main);
      transition: all 0.2s;
    }}
    .slide-item:hover {{
      transform: translateX(6px);
      border-color: var(--accent-primary);
      background: rgba(124, 58, 237, 0.08);
    }}
    .slide-num {{
      font-family: var(--font-mono);
      font-weight: bold;
      color: #38bdf8;
      width: 40px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div style="margin-bottom: 30px;">
      <span class="badge">Slide Navigation Deck</span>
      <h1 style="font-size: 2.4rem; margin: 10px 0;">Spec-Driven Development 슬라이드 목차</h1>
      <p style="color: var(--text-muted);">실밸개발자 패스트캠퍼스 강의 10대 핵심 슬라이드 세트</p>
    </div>
    <div>
      {"".join([f'''<a href="{s['id']}.html" class="slide-item">
        <span class="slide-num">{idx+1:02d}</span>
        <div style="flex: 1;">
          <strong style="font-size: 1.05rem;">{s['title']}</strong>
          <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">{s['subtitle']}</div>
        </div>
        <span style="color: #a78bfa;">열기 &rarr;</span>
      </a>''' for idx, s in enumerate(SLIDES_DATA)])}
    </div>
    <div style="margin-top: 30px; text-align: center;">
      <a href="../lecture_report.html" style="color: #38bdf8; text-decoration: none; font-size: 0.95rem;">&larr; 단일 인터랙티브 종합 리포트 보기</a>
    </div>
  </div>
</body>
</html>"""

with open(os.path.join(SLIDES_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

# Generate Single Dashboard Report
report_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 시대 새로운 패러다임: Spec-Driven Development 심층 리포트</title>
  <style>
    {COMMON_CSS}
    .layout {{
      display: grid;
      grid-template-columns: 280px 1fr;
      max-width: 1400px;
      margin: 0 auto;
      gap: 30px;
      padding: 30px 20px;
    }}
    .sidebar {{
      position: sticky;
      top: 30px;
      height: fit-content;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      backdrop-filter: blur(12px);
    }}
    .toc-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: #a78bfa;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 14px;
    }}
    .toc-link {{
      display: block;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.88rem;
      padding: 6px 10px;
      border-radius: 6px;
      transition: all 0.2s;
      margin-bottom: 4px;
    }}
    .toc-link:hover, .toc-link.active {{
      background: rgba(124, 58, 237, 0.15);
      color: #f0f6fc;
      border-left: 2px solid var(--accent-primary);
    }}
    .content-area {{
      min-width: 0;
    }}
    .section-header {{
      padding-bottom: 12px;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 24px;
      margin-top: 40px;
    }}
    .section-header:first-of-type {{ margin-top: 0; }}
  </style>
</head>
<body>
  <div class="layout">
    <!-- Sidebar TOC -->
    <aside class="sidebar">
      <div class="toc-title">Table of Contents</div>
      <a href="#overview" class="toc-link">1. Executive Summary</a>
      <a href="#mindset" class="toc-link">2. 5대 사고방식 전환</a>
      <a href="#loop" class="toc-link">3. SDD 5단계 라이프사이클</a>
      <a href="#architecture" class="toc-link">4. 하네스 프레임워크 해부</a>
      <a href="#context" class="toc-link">5. claude -p & 컨텍스트 격리</a>
      <a href="#prompts" class="toc-link">6. 무결점 프롬프트 추출본</a>
      <a href="#domain" class="toc-link">7. 그룹장 맞춤 실무 적용</a>
      <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--card-border);">
        <a href="slides/index.html" style="display: block; text-align: center; background: rgba(56, 189, 248, 0.15); color: #38bdf8; text-decoration: none; padding: 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(56, 189, 248, 0.3);">
          🖥️ 슬라이드 덱 프레젠테이션 &rarr;
        </a>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="content-area">
      <!-- Section 1 -->
      <section id="overview">
        <div class="section-header">
          <span class="badge">Deep Curation Report</span>
          <span class="badge badge-cyan">jha0313/harness_framework</span>
          <h1 style="font-size: 2.2rem; margin: 10px 0;">AI 시대의 새로운 패러다임: Spec-Driven Development</h1>
          <p style="color: var(--text-muted);">실밸개발자 (메타 시니어 엔지니어 하재상) 강의 전수 요약 & 엔지니어링 분석</p>
        </div>

        <div class="card">
          <h3 style="color: #c4b5fd; margin-bottom: 12px;">🌟 Executive Summary: 스펙이 구현을 주도하는 시대</h3>
          <p style="margin-bottom: 16px;">
            AI 시대에 코딩의 단가와 소요 시간은 사실상 0으로 수렴하고 있습니다. 과거에는 100명의 개발자를 채용하여 코딩과 테스트 병목을 해소하려 했지만, 이제는 <strong>설계(Design)와 검토(Review)가 유일한 엔지니어링 병목</strong>입니다.
          </p>
          <p style="margin-bottom: 16px;">
            <strong>TDD(Test-Driven Development)</strong>는 무엇을 만들지가 명확한 함수나 버그 수정에는 유용하지만, 새로운 도메인이나 아키텍처를 맨 처음 정의할 때는 테스트를 먼저 작성하기 어렵습니다. <strong>SDD(Spec-Driven Development)</strong>는 인간이 자연어 스펙을 정밀하게 다듬고, AI가 계획 수립, 격리된 서브세션 코딩, 자가 교정까지 완결 짓도록 지휘하는 AI-Native 개발 방법론입니다.
          </p>
        </div>
      </section>

      <!-- Section 2 -->
      <section id="mindset">
        <div class="section-header">
          <h2 style="font-size: 1.6rem; color: #38bdf8;">🧠 SDD를 위한 5대 사고방식 전환 (Mindset Shift)</h2>
        </div>
        <div class="card">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px;">
            <div style="background: rgba(255,255,255,0.02); padding: 14px; border-radius: 8px; border: 1px solid var(--card-border);">
              <strong style="color: #c4b5fd;">1. Spec First, Code Second</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">코드 전에 자연어 스펙 작성. 명확한 스펙은 단번에 프로덕션 코드로 직행함.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); padding: 14px; border-radius: 8px; border: 1px solid var(--card-border);">
              <strong style="color: #38bdf8;">2. Reviewer, Not Author</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">인간은 타이핑하는 코더가 아닌 아키텍처와 엣지케이스를 판정하는 리뷰어.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); padding: 14px; border-radius: 8px; border: 1px solid var(--card-border);">
              <strong style="color: #6ee7b7;">3. Externalize Mental Context</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">머릿속 암묵지를 CLAUDE.md 및 ADR로 외부화. 적히지 않은 지식은 AI가 모름.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); padding: 14px; border-radius: 8px; border: 1px solid var(--card-border);">
              <strong style="color: #fcd34d;">4. Attention on Design Bottleneck</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">주의력의 80%를 스펙 설계에 투입. 설계가 가장 높은 레버리지 구간.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); padding: 14px; border-radius: 8px; border: 1px solid var(--card-border); grid-column: span 2;">
              <strong style="color: #f472b6;">5. Closed Learning Loop (복리 성장)</strong>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">AI 실패를 규칙으로 환류하여 시스템을 개선. 50번째 세션은 첫 번째 세션보다 압도적으로 생산적이어야 함.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 3 -->
      <section id="loop">
        <div class="section-header">
          <h2 style="font-size: 1.6rem; color: #38bdf8;">🔄 SDD 5단계 라이프사이클 루프</h2>
        </div>
        <div class="card">
          <table>
            <thead>
              <tr>
                <th>단계</th>
                <th>주체</th>
                <th>핵심 활동</th>
                <th>산출물</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. 설계 (Design)</strong></td>
                <td><span class="badge">인간 주도</span></td>
                <td>목표, 아키텍처, 결정 이유(ADR), 제약 사항 정의</td>
                <td><code>PRD.md</code>, <code>ARCHITECTURE.md</code>, <code>ADR.md</code></td>
              </tr>
              <tr>
                <td><strong>2. 계획 (Plan)</strong></td>
                <td><span class="badge badge-cyan">AI 주도 / 인간 승인</span></td>
                <td>스펙을 자기완결적 Step 단위로 분할</td>
                <td><code>phases/index.json</code>, <code>step{{N}}.md</code></td>
              </tr>
              <tr>
                <td><strong>3. 구현 (Execute)</strong></td>
                <td><span class="badge" style="background:#10b98122; color:#6ee7b7;">AI 자율</span></td>
                <td>독립 헤드리스 세션에서 컴파일 및 AC 테스트 자율 통과</td>
                <td>프로덕션 코드, 단위 테스트</td>
              </tr>
              <tr>
                <td><strong>4. 교정 (Correct)</strong></td>
                <td><span class="badge" style="background:#f59e0b22; color:#fcd34d;">인간 주도</span></td>
                <td>유저 저니, 에러 매트릭스 검토 및 피드백 주입</td>
                <td>재계획 및 보강된 스펙</td>
              </tr>
              <tr>
                <td><strong>5. 회고 (Reflect)</strong></td>
                <td><span class="badge" style="background:#ec489922; color:#f472b6;">인간 주도</span></td>
                <td>반성문에서 도출된 교훈을 규칙으로 영구 승격</td>
                <td><code>CLAUDE.md</code> 가드레일 업데이트</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Section 4 -->
      <section id="architecture">
        <div class="section-header">
          <h2 style="font-size: 1.6rem; color: #38bdf8;">🛠️ 하네스 프레임워크 아키텍처 심층 해부</h2>
        </div>
        <div class="card">
          <h3 style="color: #c4b5fd; margin-bottom: 12px;">jha0313/harness_framework 핵심 규칙</h3>
          <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 16px;">
            하네스는 복잡할수록 좋은 것이 아닙니다. 30~40개의 복잡한 스킬보다, <strong>명확한 문서 4종 + 1개의 가벼운 파이썬 오케스트레이터</strong>가 가장 강력합니다.
          </p>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 18px;">
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 14px; border-radius: 8px;">
              <strong style="color: #38bdf8;">.claude/commands/harness.md (7대 원칙)</strong>
              <ul style="font-size: 0.82rem; color: #d1d5db; margin-top: 6px; padding-left: 18px;">
                <li>Scope 최소화 (한 step에 하나의 모듈만)</li>
                <li>자기완결성 (외부 대화 참조 금지)</li>
                <li>사전 준비 강제 (읽을 파일 경로 명시)</li>
                <li>시그니처 수준 지시 (구현체는 위임)</li>
                <li>실행 가능한 AC (<code>npm test</code> 등)</li>
                <li>구체적 주의사항 (&quot;X 하지 마라. 이유: Y&quot;)</li>
                <li>Kebab-case 네이밍</li>
              </ul>
            </div>
            <div style="background: rgba(18, 26, 43, 0.8); border: 1px solid var(--card-border); padding: 14px; border-radius: 8px;">
              <strong style="color: #f87171;">docs/UI_GUIDE.md (AI 슬롭 금지)</strong>
              <ul style="font-size: 0.82rem; color: #d1d5db; margin-top: 6px; padding-left: 18px;">
                <li><code>backdrop-filter: blur()</code> 금지</li>
                <li><code>gradient-text</code> (그라데이션 텍스트) 금지</li>
                <li>&quot;Powered by AI&quot; 배지 장식 금지</li>
                <li>box-shadow 네온 글로우 금지</li>
                <li>보라/인디고 브랜드 색상 클리셰 금지</li>
                <li>모든 카드에 균일한 rounded-2xl 금지</li>
                <li>배경 gradient orb 원형 블러 금지</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 5 -->
      <section id="context">
        <div class="section-header">
          <h2 style="font-size: 1.6rem; color: #38bdf8;">🛡️ claude -p 헤드리스 모드 & 컨텍스트 오염 차폐</h2>
        </div>
        <div class="card">
          <h3 style="color: #f87171; margin-bottom: 12px;">메인 컨텍스트가 커지면 발생하는 재앙</h3>
          <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 14px;">
            단일 대화 세션에서 5개 이상의 Step을 연속 구현하면 컨텍스트 윈도우가 150k를 초과하여 모델 지능이 30% 수준으로 폭락합니다. 하네스 프레임워크의 <code>execute.py</code>는 각 Step을 <strong>독립된 1회용 서브프로세스</strong>로 분리 실행하여 이를 해결합니다.
          </p>
          <div class="code-box">
            <button class="copy-btn" onclick="copyCode(this)">Copy</button>
            <pre><code># scripts/execute.py의 핵심 격리 로직
def _invoke_claude(self, step: dict, preamble: str) -> dict:
    step_num, step_name = step["step"], step["name"]
    step_file = self._phase_dir / f"step{{step_num}}.md"
    prompt = preamble + step_file.read_text()
    
    # claude -p 헤드리스 모드로 1회성 서브세션 실행 (메인 세션 오염 없음)
    result = subprocess.run(
        ["claude", "-p", "--dangerously-skip-permissions", "--output-format", "json", prompt],
        cwd=self._root, capture_output=True, text=True, timeout=1800,
    )
    return output</code></pre>
          </div>
        </div>
      </section>

      <!-- Section 6 -->
      <section id="prompts">
        <div class="section-header">
          <h2 style="font-size: 1.6rem; color: #38bdf8;">📝 100% 무결점 프롬프트 추출본 (One-Click Copy)</h2>
        </div>
        <div class="card">
          <h4 style="color: #c4b5fd; margin-bottom: 6px;">[Prompt 1] 썸네일 생성기 의도 제시 및 스펙 수립 요청</h4>
          <div class="code-box">
            <button class="copy-btn" onclick="copyCode(this)">Copy</button>
            <pre><code>오늘 나는 유튜브 썸네일을 GPT-Image-2 API를 사용해서 만드는 서비스를 만들어 볼 거야.
이 서비스는 사용자의 브리프(프롬프트)와 선택적인 이미지를 입력받아서 유튜브 16:9 썸네일 이미지를 생성하는 웹 애플리케이션이야.
- 인풋: 프롬프트(필수), 참조 이미지(선택)
- 아웃풋: 16:9 썸네일 이미지 (후보 2개 동시 생성)
- 타겟 사용자: 유튜브 크리에이터
- 목적: 썸네일 제작 시간을 단축하고 고품질 썸네일을 쉽게 제작하여 시청자 유입률 증대
현재 저장소의 구조를 파악하고, docs/ 하위 문서(PRD, ARCHITECTURE, ADR, CLAUDE.md)를 바탕으로 스펙과 구현 계획(Plan)을 수립해 줘.</code></pre>
          </div>

          <h4 style="color: #38bdf8; margin-top: 20px; margin-bottom: 6px;">[Prompt 2] 스펙 고도화 (티키타카 - 유저 저니 & 에러 매트릭스 보강)</h4>
          <div class="code-box">
            <button class="copy-btn" onclick="copyCode(this)">Copy</button>
            <pre><code>플랜이 아주 빈약해. 특히 유저 플로우(User Journey)와 에러 핸들링 매트릭스를 잘 설계해 줘야 돼.
사용자가 어떻게 진입해서 어떤 폼을 작성하고, 검증 실패 시 어떻게 처리되며, API 호출 실패나 에러가 발생했을 때 조건부 재시도 및 UI 피드백을 어떻게 줄 것인지 다이어그램과 표로 아주 디테일하게 보강해 줘.
그리고 MVP 목적에 맞게 오버엔지니어링은 하지 말고, 최소한의 변화로 최대의 아웃풋을 내도록 계획을 다시 짜 줘.</code></pre>
          </div>

          <h4 style="color: #6ee7b7; margin-top: 20px; margin-bottom: 6px;">[Prompt 3] `/harness` 슬래시 커맨드 실행</h4>
          <div class="code-box">
            <button class="copy-btn" onclick="copyCode(this)">Copy</button>
            <pre><code>/harness
docs/ 하위 문서(PRD, ARCHITECTURE, ADR, CLAUDE.md) 작성을 완료하고, 각 Step이 독립된 세션에서 실행될 수 있도록 Scope 최소화, 자기완결성, AC 실행 커맨드를 포함한 phases/0-mvp/index.json 및 step0.md ~ step4.md 파일들을 생성해 줘.</code></pre>
          </div>
        </div>
      </section>

      <!-- Section 7 -->
      <section id="domain">
        <div class="section-header">
          <h2 style="font-size: 1.6rem; color: #38bdf8;">🏢 그룹장 도메인 최적화: 임베디드 SW & 통신 프로토콜 적용</h2>
        </div>
        <div class="card">
          <div style="background: rgba(124, 58, 237, 0.08); padding: 18px; border-radius: 8px; border-left: 3px solid var(--accent-primary); margin-bottom: 16px;">
            <strong style="color: #c4b5fd; font-size: 1.05rem;">1. HW 레지스터 맵 기반 C/C++ 임베디드 하네스</strong>
            <p style="font-size: 0.88rem; color: #d1d5db; margin-top: 6px;">
              신규 Baseband / RFIC 레지스터 맵 명세서(오프셋, 비트필드, 권한)를 <code>docs/PRD.md</code>에 정의하고, <code>execute.py</code>를 통해 C 구조체 헤더 정의 ➡️ 비트 조작 인라인 함수 ➡️ QEMU/호스트 단위 시뮬레이션 AC(Acceptance Criteria) 검증까지 자동화.
            </p>
          </div>
          <div style="background: rgba(56, 189, 248, 0.08); padding: 18px; border-radius: 8px; border-left: 3px solid var(--accent-cyan); margin-bottom: 16px;">
            <strong style="color: #7dd3fc; font-size: 1.05rem;">2. 계층형 스펙(Hierarchical Specs)을 통한 3GPP 프로토콜 분할 정복</strong>
            <p style="font-size: 0.88rem; color: #d1d5db; margin-top: 6px;">
              대규모 3GPP 릴리즈 규격을 단일 프롬프트에 넣지 않고, Master Spec 아래 L1 PHY(디코딩), L2 MAC(HARQ 제어), L3 RRC(상태 머신)로 모듈화하여 각 계층별 독립 <code>step.md</code>로 무환각 구현.
            </p>
          </div>
          <div style="background: rgba(16, 185, 129, 0.08); padding: 18px; border-radius: 8px; border-left: 3px solid #10b981;">
            <strong style="color: #6ee7b7; font-size: 1.05rem;">3. JIRA / 필드 이슈 분석 자동 회고 루프</strong>
            <p style="font-size: 0.88rem; color: #d1d5db; margin-top: 6px;">
              통신 필드 Drop call 또는 타이밍 이슈 분석 결과를 <code>docs/ADR.md</code> 및 <code>CLAUDE.md</code>의 CRITICAL 규칙으로 영구 승격하여, 다음 개발 시 동일한 버그가 원천 방지되도록 시스템 자산화.
            </p>
          </div>
        </div>
      </section>
    </main>
  </div>

  <script>
    function copyCode(btn) {{
      const pre = btn.parentElement.querySelector('pre');
      navigator.clipboard.writeText(pre.innerText).then(() => {{
        const oldText = btn.innerText;
        btn.innerText = 'Copied!';
        btn.style.background = '#10b981';
        setTimeout(() => {{
          btn.innerText = oldText;
          btn.style.background = '';
        }}, 2000);
      }});
    }}
  </script>
</body>
</html>"""

with open(os.path.join(BASE_DIR, "lecture_report.html"), "w", encoding="utf-8") as f:
    f.write(report_html)

print("Slide set and lecture report generated successfully!")
