import os
import json
import shutil
import subprocess

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(PROJECT_DIR, "config.json")
BACKUP_PATH = os.path.join(PROJECT_DIR, "config.json.bak")
SCRIPT_PATH = os.path.join(PROJECT_DIR, "update_topic.py")

def setup_backup():
    if os.path.exists(CONFIG_PATH):
        shutil.copy2(CONFIG_PATH, BACKUP_PATH)

def restore_backup():
    if os.path.exists(BACKUP_PATH):
        shutil.copy2(BACKUP_PATH, CONFIG_PATH)
        os.remove(BACKUP_PATH)

def run_test(title, body=""):
    print(f"\n--- Testing Issue: '{title}' ---")
    result = subprocess.run(
        ["python", SCRIPT_PATH, "--title", title, "--body", body],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("FAIL: Script exited with error.")
        print(result.stdout)
        print(result.stderr)
        return False
        
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            new_config = json.load(f)
            
        print("SUCCESS: Output valid JSON.")
        print("New Categories Found:")
        for cat in new_config.get("categories", []):
            print(f" - {cat['name']} (queries: {len(cat.get('queries', []))})")
            
        return True
    except Exception as e:
        print(f"FAIL: JSON Parsing error: {e}")
        return False

def main():
    print("Starting IssueOps Verification Loop...")
    setup_backup()
    
    success_count = 0
    tests = [
        ("양자컴퓨터 주제 추가해줘", "최근 양자컴퓨터의 상용화 동향과 주요 기업들의 발표 위주로 포커싱"),
        ("자율주행 자동차 동향 추가", "테슬라, 웨이모 등"),
        ("기존 통신 카테고리 삭제해줘", ""), # 모호/변경 요청 테스트
    ]
    
    try:
        for title, body in tests:
            if run_test(title, body):
                success_count += 1
            # Restore backup after each test to keep environment clean
            restore_backup()
            setup_backup()
            
    finally:
        restore_backup()
        
    print(f"\nCompleted {len(tests)} tests. Success: {success_count}/{len(tests)}")
    if success_count == len(tests):
        print("All tests passed! Verification loop is completely verified.")
        sys.exit(0)
    else:
        print("Some tests failed.")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
