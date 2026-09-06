# 📰 Daily News Summarizer

매일 아침, 내가 관심 있는 글로벌 산업의 핵심 트렌드만 쏙쏙 뽑아 전문가 수준의 브리핑으로 정리해주는 완전 자동화 뉴스 요약기입니다.

## ✨ 핵심 기능
- **📌 3단계 입체 브리핑 구조**:
  1. **Section 1 (Executive Summary)**: 당일 뉴스와 오픈소스 트렌드를 관통하여 **Group 2nd Brain** 및 **Codebase 이해/구현 루프/코드 리뷰** 관점의 핵심 혁신, 보안/환각 리스크, 실무 시사점을 도출합니다.
  2. **Section 2 (오늘의 GitHub 트렌드 큐레이션: 시니어 멘토 개발자)**: 20년 차 시니어 개발자의 시선에서 4대 핵심 주제(Second-Brain, Code Review AI, Codebase understanding, Embedded SW implementation)별 스테디셀러와 신흥 루키를 1:1로 엄선하여 실무 페인포인트와 아키텍처 팁(Overview + Senior's Insight)을 큐레이션합니다.
  3. **Section 3 (관심 분야별 심층 뉴스)**: 사내 2nd Brain, 코드 리뷰/에이전틱 루프, 글로벌 빅테크 M&A/자본 동맹, AI 반도체/인프라, **Telecom & Mobility Strategy C-Pilot (통신·모빌리티 전략 분석기: 비-모바일 다각화, Custom SoC, 5G FWA, 위성 NTN, 벤더 다각화 매트릭스 표 및 후속 질문)** 등 맞춤 카테고리 뉴스 분석.
- **✉️ 모던 반응형 HTML 이메일 & 마크다운 테이블 엔진**: 모바일과 데스크톱 메일 클라이언트 모두에서 완벽히 가독성을 보장하는 프리미엄 카드 UI 및 인라인 CSS 테이블 렌더링을 지원합니다.
- **🤖 Dual-LLM 안정성**: Google Gemini를 메인 엔진으로 사용하며, 한도 초과 시 OpenAI(GPT-4o-mini)로 자동 Fallback 됩니다.
- **💡 스마트 트렌드 추천**: 브리핑 하단에 새롭게 추적할 만한 신규 키워드를 추천합니다.
- **📱 스마트폰 원격 업데이트 (IssueOps)**: 스마트폰 GitHub Issue 등록만으로 `config.json`을 AI가 자동 갱신합니다.
- **📝 Obsidian 완벽 호환**: 생성된 리포트는 MyWiki 옵시디언 포맷(`_sources/News/Daily_Summaries/`)으로 자동 아카이빙됩니다.


---

## 🚀 5분 컷! 나만의 뉴스 요약기 세팅 가이드

초보자도 무조건 따라 할 수 있도록 상세하게 설명합니다.

### 1단계: 저장소 준비 (Fork / Use this template)
1. GitHub 계정이 없다면 먼저 회원가입을 진행합니다.
2. 현재 이 저장소의 우측 상단에 있는 **`Use this template`** 버튼을 누르거나 **`Fork`**를 클릭하여 내 계정으로 가져옵니다.

### 2단계: API 키 및 앱 비밀번호 발급

#### ① Google 앱 비밀번호 발급 (이메일 발송용)
본인의 Gmail 계정으로 메일을 보내려면 보안 인증이 필요합니다.
1. 구글 계정 관리에 들어가 **[보안]** 탭을 클릭합니다.
2. **[2단계 인증]**이 꺼져 있다면 켜줍니다.
3. 검색창에 **"앱 비밀번호"**(App passwords)를 검색해서 들어갑니다.
4. 앱 이름을 `NewsSummarizer`로 적고 생성(만들기) 버튼을 누릅니다.
5. 화면에 표시되는 **16자리 비밀번호**를 복사해둡니다. (창을 닫으면 다시 볼 수 없으니 메모장 등에 임시 저장하세요.)

#### ② Gemini API 키 발급 (AI 요약용)
최고 성능의 Gemini AI를 무료로 쓰기 위한 열쇠입니다.
1. [Google AI Studio](https://aistudio.google.com/)에 접속하여 로그인합니다.
2. 좌측 메뉴에서 **`Get API key`**를 클릭합니다.
3. 파란색 **`Create API key`** 버튼을 눌러 새 키를 생성하고 복사해둡니다.

### 3단계: GitHub Secrets 등록 (최종 자동화 세팅)
복사해둔 키값들을 내 GitHub 저장소에 안전하게 등록합니다.
1. 내 저장소 화면에서 상단의 **[Settings]** 탭을 누릅니다.
2. 좌측 메뉴에서 **[Secrets and variables] -> [Actions]**를 클릭합니다.
3. 초록색 **`New repository secret`** 버튼을 눌러 다음 4개의 값을 차례대로 추가합니다:
   - `GEMINI_API_KEY`: 방금 발급받은 Gemini API 키
   - `EMAIL_SENDER`: 본인의 구글 이메일 주소 (예: `myid@gmail.com`)
   - `EMAIL_PASSWORD`: 1단계에서 발급받은 16자리 구글 앱 비밀번호
   - `EMAIL_RECEIVER`: 메일을 받아볼 주소 (본인 주소로 적어도 됩니다.)

🎉 **수고하셨습니다! 모든 세팅이 끝났습니다.** 이제 매일 아침 자동으로 뉴스가 배달됩니다!

---

## 🛠️ 스마트폰으로 주제 추가하기 (IssueOps)

"오늘 메일에 추천된 양자컴퓨터 주제를 내일 브리핑부터 받고 싶은데, PC 켜기가 귀찮다?"
👉 **스마트폰 GitHub 앱에서 Issue 하나만 띄우세요!**

1. 폰에서 내 `NewsSummarizer` 저장소로 들어갑니다.
2. **Issues** 탭에서 글을 하나 작성합니다.
   - 제목 예시: `"양자컴퓨터 주제 추가해줘"`
   - 내용 예시: `"상용화 동향과 주요 기업 소식 위주로"` (생략 가능)
3. Submit 버튼을 누르면 끝입니다. 
4. AI가 알아서 `config.json`을 수정해 주고, 처리가 끝나면 이슈에 완료 댓글을 달고 닫아줍니다. 내일 아침부터 해당 뉴스가 배달됩니다!
