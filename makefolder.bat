@echo off
chcp 65001 >nul
cd /d "C:\Users\kihok\내 드라이브\MyWiki"

echo ===== 기본 폴더 생성 =====
mkdir "00_Inbox" 2>nul
mkdir "90_MOC" 2>nul
mkdir "99_Templates" 2>nul

echo ===== News 생성 =====
mkdir "News\Tech-AI" 2>nul
mkdir "News\Communication" 2>nul
mkdir "News\Energy-Power" 2>nul
mkdir "News\Radar" 2>nul
mkdir "News\Non-mobile-Biz" 2>nul
mkdir "News\Finance" 2>nul

echo ===== Study 생성 =====
mkdir "Study\AI-Lectures" 2>nul
mkdir "Study\AI-Prompt" 2>nul
mkdir "Study\AI-활용법" 2>nul

echo ===== Books 생성 =====
mkdir "Books\Novels" 2>nul
mkdir "Books\Tech" 2>nul
mkdir "Books\Future-Insight" 2>nul
mkdir "Books\FinTech" 2>nul

echo ===== Projects 생성 =====
mkdir "Projects\Milestone-Generator" 2>nul
mkdir "Projects\Doc-Automation" 2>nul
mkdir "Projects\Data-Processing-Tools" 2>nul
mkdir "Projects\_Templates" 2>nul

echo ===== Work-Ideas 생성 =====
mkdir "Work-Ideas\Pre-Silicon-Verification" 2>nul
mkdir "Work-Ideas\Feature-Development" 2>nul
mkdir "Work-Ideas\Code-Review-Automation" 2>nul
mkdir "Work-Ideas\Simulator-TDD" 2>nul
mkdir "Work-Ideas\E2E-AI-Verification-Loop" 2>nul
mkdir "Work-Ideas\Data-Handling-Optimization" 2>nul

echo.
echo ===== 전체 구조 생성 완료 =====
pause