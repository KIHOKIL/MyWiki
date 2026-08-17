#!/usr/bin/env python3
"""
generate_index.py — Obsidian _sources 폴더 인덱스 자동 생성/갱신 스크립트

사용 방법:
    python3 scripts/generate_index.py                  # _sources 전체 하위 폴더 일괄 처리
    python3 scripts/generate_index.py "특정폴더명"    # 특정 하위 폴더 하나만 처리
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from datetime import datetime
from pathlib import Path

# Windows 터미널의 cp949 인코딩으로 인한 유니코드 오류 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-16"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# 1. 설정 파일 탐색 — .env (CWD 상향 탐색) 또는 ~/.obsidian-wiki/config
# ---------------------------------------------------------------------------

def _parse_env_file(path: Path) -> dict[str, str]:
    """단순 KEY=VALUE 파일을 파싱. 주석(#)과 빈 줄은 무시."""
    result: dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                result[key.strip()] = value.strip()
    except (OSError, UnicodeDecodeError):
        pass
    return result


def resolve_vault_path() -> Path:
    """
    OBSIDIAN_VAULT_PATH 탐색 순서:
      1. CWD부터 부모로 올라가며 OBSIDIAN_VAULT_PATH 를 포함한 .env 탐색
      2. ~/.obsidian-wiki/config 탐색
    """
    # 1) .env 파일 상향 탐색
    cwd = Path.cwd()
    candidate = cwd
    while True:
        env_file = candidate / ".env"
        if env_file.is_file():
            env = _parse_env_file(env_file)
            vault_raw = env.get("OBSIDIAN_VAULT_PATH", "")
            if vault_raw:
                vault = Path(vault_raw).expanduser()
                if vault.is_dir():
                    return vault
        parent = candidate.parent
        if parent == candidate:  # 루트 도달
            break
        candidate = parent

    # 2) 글로벌 설정 탐색
    global_config = Path.home() / ".obsidian-wiki" / "config"
    if global_config.is_file():
        cfg = _parse_env_file(global_config)
        vault_raw = cfg.get("OBSIDIAN_VAULT_PATH", "")
        if vault_raw:
            vault = Path(vault_raw).expanduser()
            if vault.is_dir():
                return vault

    print(
        "오류: OBSIDIAN_VAULT_PATH 를 찾을 수 없습니다.\n"
        "  • 현재 폴더(또는 상위 폴더)의 .env 파일에 OBSIDIAN_VAULT_PATH=<경로> 를 설정하거나\n"
        "  • ~/.obsidian-wiki/config 파일을 생성하세요.",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# 2. 헬퍼 — 기존 _index.md 파싱 및 파일 첫 제목 추출
# ---------------------------------------------------------------------------

# [[파일명.md]] — 설명 패턴 (공백 변형 허용)
_DESC_PATTERN = re.compile(r"\[\[([^\]]+\.md)\]\]\s*[—\-]+\s*(.+)")


def _load_existing_descriptions(index_path: Path) -> dict[str, str]:
    """기존 _index.md 에서 [[파일명.md]] — 설명 딕셔너리를 파싱."""
    descriptions: dict[str, str] = {}
    if not index_path.is_file():
        return descriptions
    try:
        content = index_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return descriptions
    for match in _DESC_PATTERN.finditer(content):
        filename = match.group(1).strip()
        desc = match.group(2).strip()
        descriptions[filename] = desc
    return descriptions


def _extract_first_heading(md_path: Path) -> str:
    """마크다운 파일에서 첫 번째 H1(#) 또는 H2(##) 제목을 반환."""
    try:
        for line in md_path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^#{1,2}\s+(.+)", line)
            if m:
                return m.group(1).strip()
    except (OSError, UnicodeDecodeError):
        pass
    return "원본 문서 자료"


# ---------------------------------------------------------------------------
# 3. 하위 폴더 _index.md 생성/갱신
# ---------------------------------------------------------------------------

def generate_folder_index(folder: Path) -> None:
    """폴더 내 .md 파일을 수집하여 _index.md 를 생성/덮어쓰기."""
    folder_name = folder.name

    # 파일명이 _ 로 시작하지 않는 .md 파일만 수집 (오름차순, 하위 폴더 포함)
    md_files = sorted(
        [f for f in folder.rglob("*.md") if f.is_file() and not f.name.startswith("_")],
        key=lambda p: p.name,
    )

    index_path = folder / "_index.md"

    # 기존 설명 보존
    existing_desc = _load_existing_descriptions(index_path)

    # 각 파일의 설명 결정
    entries: list[tuple[str, str]] = []
    for md_file in md_files:
        filename = md_file.name
        if filename in existing_desc:
            desc = existing_desc[filename]
        else:
            desc = _extract_first_heading(md_file)
        entries.append((filename, desc))

    # 파일 목록 섹션 생성
    if entries:
        list_lines = "\n".join(f"- [[{name}]] — {desc}" for name, desc in entries)
    else:
        list_lines = "*아직 소스 파일이 없습니다.*"

    timestamp = datetime.now().strftime("%Y-%m-%d")
    content = (
        f"# {folder_name} 소스 인덱스\n\n"
        f"이 폴더는 {folder_name} 관련 원본 문서들을 모아놓은 디렉토리입니다.\n\n"
        f"## 소스 파일 목록\n"
        f"{list_lines}\n\n"
        f"## 관련 위키 페이지\n"
        f"*아직 인제스트되지 않았습니다. wiki-ingest를 실행하여 지식을 wiki로 변환하세요.*\n\n"
        f"---\n"
        f"*마지막 갱신: {timestamp}*\n"
    )

    index_path.write_text(content, encoding="utf-8")
    print(f"  [OK] {folder_name}/_index.md 생성/갱신 완료 ({len(entries)}개 파일)")


# ---------------------------------------------------------------------------
# 4. 마스터 인덱스 (_source/_index.md) 갱신
# ---------------------------------------------------------------------------

MASTER_HEADER = "# _source 마스터 인덱스"
FOLDER_SECTION = "## 주제별 폴더 목록"


def _build_master_index_initial(sources_dir: Path) -> str:
    """마스터 인덱스가 없을 때 초기 내용을 생성."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    return (
        f"{MASTER_HEADER}\n\n"
        f"`_sources/` 폴더의 모든 원본 소스 문서를 주제별로 정리한 마스터 인덱스입니다.\n\n"
        f"{FOLDER_SECTION}\n\n"
        f"---\n"
        f"*마지막 갱신: {timestamp}*\n"
    )


def register_folder_in_master(sources_dir: Path, folder_name: str) -> None:
    """
    마스터 인덱스(_sources/_index.md)에 하위 폴더 링크가 없으면 삽입.
    """
    master_path = sources_dir / "_index.md"

    # 마스터 인덱스가 없으면 초기 생성
    if not master_path.is_file():
        master_path.write_text(_build_master_index_initial(sources_dir), encoding="utf-8")
        print(f"  [NEW] _sources/_index.md 초기 생성 완료")

    content = master_path.read_text(encoding="utf-8")

    # 이미 링크가 있으면 스킵
    link_marker = f"[[{folder_name}/_index.md"
    if link_marker in content:
        print(f"  [SKIP] {folder_name} — 이미 마스터 인덱스에 등록되어 있습니다.")
        return

    # '## 주제별 폴더 목록' 섹션 다음에 삽입
    new_entry = f"- [[{folder_name}/_index.md|{folder_name}]] — {folder_name} 관련 매뉴얼 및 문서 자료"
    section_header = FOLDER_SECTION

    if section_header in content:
        # 헤더 바로 아래 빈 줄 이후에 삽입
        lines = content.splitlines(keepends=True)
        insert_idx = None
        for i, line in enumerate(lines):
            if line.strip() == section_header:
                # 헤더 다음 줄부터 시작하는 기존 항목들 아래에 추가
                # (헤더 + 빈 줄 건너뛰고 첫 번째 비목록 줄 앞에 삽입)
                j = i + 1
                while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith("-")):
                    j += 1
                insert_idx = j
                break

        if insert_idx is not None:
            # --- 구분선이 있다면 그 앞에 삽입
            while insert_idx > 0 and lines[insert_idx - 1].strip() in ("", "---"):
                insert_idx -= 1
            lines.insert(insert_idx, new_entry + "\n")
            content = "".join(lines)
        else:
            content += f"\n{new_entry}\n"
    else:
        # 섹션 헤더 자체가 없으면 파일 끝에 섹션째 추가
        content += f"\n{section_header}\n\n{new_entry}\n"

    # 타임스탬프 갱신
    timestamp = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(r"\*마지막 갱신: [\d\-]+\*", f"*마지막 갱신: {timestamp}*", content)

    master_path.write_text(content, encoding="utf-8")
    print(f"  [OK] _sources/_index.md 에 [{folder_name}] 등록 완료")


# ---------------------------------------------------------------------------
# 5. 메인 진입점
# ---------------------------------------------------------------------------

def process_folder(sources_dir: Path, folder_name: str) -> None:
    """하위 폴더 인덱스 생성 + 마스터 인덱스 등록."""
    folder = sources_dir / folder_name
    if not folder.is_dir():
        print(f"오류: '{folder}' 폴더를 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)
    print(f"\n[DIR] 처리 중: {folder_name}/")
    generate_folder_index(folder)
    register_folder_in_master(sources_dir, folder_name)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Obsidian _sources 폴더의 _index.md 파일을 자동 생성/갱신합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "사용 예:\n"
            "  python3 scripts/generate_index.py              # 전체 처리\n"
            '  python3 scripts/generate_index.py "AI논문"    # 특정 폴더만 처리'
        ),
    )
    parser.add_argument(
        "folder",
        nargs="?",
        help="처리할 _sources 하위 폴더명 (생략 시 전체 처리)",
    )
    args = parser.parse_args()

    # Vault 경로 결정
    vault_path = resolve_vault_path()
    sources_dir = vault_path / "_sources"

    if not sources_dir.is_dir():
        print(f"오류: '_sources' 폴더가 없습니다: {sources_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"[Vault]   {vault_path}")
    print(f"[Sources] {sources_dir}")

    if args.folder:
        # 단일 폴더 처리
        process_folder(sources_dir, args.folder)
    else:
        # _sources 하위의 모든 일반 디렉토리 처리
        subfolders = sorted(
            [d for d in sources_dir.iterdir() if d.is_dir() and not d.name.startswith("_")],
            key=lambda p: p.name,
        )

        if not subfolders:
            print("\n[WARN] _sources/ 하위에 처리할 폴더가 없습니다.")
            print("   폴더를 생성하고 소스 파일을 넣은 뒤 다시 실행하세요.")
            return

        print(f"\n총 {len(subfolders)}개 폴더 처리 시작...")
        for folder in subfolders:
            process_folder(sources_dir, folder.name)

    print("\n[DONE] _sources/_index.md 와 각 하위 폴더의 _index.md 가 갱신되었습니다.")


if __name__ == "__main__":
    main()
