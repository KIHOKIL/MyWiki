---
name: generate-index
description: >
  Generate and update _index.md files for all subfolders inside the _sources/ directory of the
  Obsidian vault. Creates a per-folder index listing all markdown source files with their
  descriptions, and updates the master _sources/_index.md with links to each folder.
  Use when the user says "/generate-index", "generate index", "update source index",
  "rebuild _sources index", "index my sources", "sync sources index", or wants to organize
  the _sources/ directory. Optionally accepts a folder name to process only that subfolder:
  "/generate-index AI논문" or "generate index for Python레퍼런스".
---

# Generate Index — _sources 폴더 인덱스 자동 생성/갱신

이 Skill은 `$OBSIDIAN_VAULT_PATH/_sources/` 하위 폴더들의 `_index.md` 파일을
자동으로 생성·갱신하고, 마스터 인덱스(`_sources/_index.md`)를 최신 상태로 유지합니다.

## 실행 전 준비

1. **설정 해석** — Config Resolution Protocol (`llm-wiki/SKILL.md` 참조):
   - 인라인 `@name` 오버라이드 → CWD부터 상위로 `.env` 탐색 (`OBSIDIAN_VAULT_PATH` 포함 여부) →
     `~/.obsidian-wiki/config` → 없으면 setup 안내
   - `OBSIDIAN_VAULT_PATH` 를 확정한다. 로그·에코·기타 값 출력 금지.

2. **스크립트 존재 확인** — `$OBSIDIAN_VAULT_PATH/scripts/generate_index.py` 파일이 있는지 확인.
   - 없으면 아래 **Step 0** 을 먼저 실행한 뒤 진행.

3. **대상 파악** — 명령에 폴더명 인수가 포함되어 있으면 해당 폴더만 처리.
   예: `/generate-index AI논문` → `"AI논문"` 만 처리.
   인수가 없으면 `_sources/` 전체 하위 폴더 일괄 처리.

---

## Step 0 (필요한 경우만): 스크립트 미존재 시 생성 안내

`scripts/generate_index.py` 가 없다면 사용자에게 알리고, 이 Vault 저장소 내에
`scripts/` 폴더를 생성한 뒤 `generate_index.py` 스크립트를 직접 작성한다.

스크립트 동작 스펙:
- `.env` (CWD 상향 탐색) 또는 `~/.obsidian-wiki/config` 에서 `OBSIDIAN_VAULT_PATH` 읽기
- `$OBSIDIAN_VAULT_PATH/_sources/<폴더>/_index.md` 생성/갱신
- `$OBSIDIAN_VAULT_PATH/_sources/_index.md` (마스터 인덱스) 갱신
- 선택적 단일 폴더 인수 지원: `python scripts/generate_index.py "폴더명"`

---

## Step 1: 실행

### 전체 처리 (인수 없음)

```bash
python "$OBSIDIAN_VAULT_PATH/scripts/generate_index.py"
```

### 특정 폴더만 처리

```bash
python "$OBSIDIAN_VAULT_PATH/scripts/generate_index.py" "폴더명"
```

- Windows 환경에서는 경로에 한글·공백이 포함될 수 있으므로 반드시 따옴표로 감싼다.
- Python 인터프리터가 `python3` 인 경우 `python3` 로 치환한다.
- 환경에 따라 `$env:PYTHONIOENCODING="utf-8"` 을 앞에 붙여 인코딩 오류를 방지한다.

---

## Step 2: 결과 확인 및 보고

실행 후 다음 항목을 확인하고 사용자에게 요약 보고한다:

1. 처리된 폴더 수 및 폴더 이름 목록
2. 각 폴더 내 인덱스에 등록된 파일 수
3. 마스터 인덱스(`_sources/_index.md`)에 새로 등록된 폴더 링크
4. 이미 등록되어 있어 스킵된 항목 (있는 경우)

보고 형식 예시:
```
generate-index 완료

처리한 폴더: 2개
  - AI논문/        → _index.md 갱신 (2개 파일)
  - Python레퍼런스/ → _index.md 갱신 (3개 파일)

_sources/_index.md 에 새로 등록:
  - [[AI논문/_index.md|AI논문]]
  - [[Python레퍼런스/_index.md|Python레퍼런스]]
```

---

## Step 3: 사후 처리

- `log.md` 에 실행 기록을 추가한다:
  ```
  - [TIMESTAMP] generate-index  folders=<처리된_폴더_목록>  files=<총_파일_수>
  ```
- `hot.md` 의 "Recent Activity" 섹션을 업데이트한다.

---

## 사용 예시

| 사용자 입력 | 동작 |
|---|---|
| `/generate-index` | `_sources/` 하위 모든 폴더 처리 |
| `/generate-index AI논문` | `_sources/AI논문/` 하나만 처리 |
| `generate index` | 전체 폴더 처리 |
| `source index 업데이트` | 전체 폴더 처리 |
| `Python레퍼런스 인덱스 만들어줘` | `_sources/Python레퍼런스/` 하나만 처리 |

---

## 관련 Skill

- `wiki-ingest` — 인덱스에 등록된 소스 파일을 위키 페이지로 변환·통합
- `wiki-status` — 현재 Vault 상태 및 인덱스 현황 확인
- `wiki-update` — 현재 프로젝트 지식을 Vault에 동기화
