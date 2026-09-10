import urllib.request, re, csv, io

SUBSCRIBERS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-8bBBW87Rx5YHf_VoCk2xIvQA9qtbSH00fp0LtBS5_1o7dGQZ21L33NXBcATaWdZ9UoaK_bOT4EQo/pub?output=csv"

def get_additional_subscribers():
    url = (SUBSCRIBERS_CSV_URL or "").strip()
    if not url:
        return []
    try:
        emails = set()
        urls_to_check = [url]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        
        # 구글 스프레드시트 게시 링크인 경우 (pub, pubhtml, output=csv 등 모든 형태 지원)
        if "docs.google.com/spreadsheets" in url:
            clean_url = url.split('?')[0]
            if clean_url.endswith('/pub'):
                pubhtml_url = clean_url + "html"
                base_pub = clean_url
            elif clean_url.endswith('/pubhtml'):
                pubhtml_url = clean_url
                base_pub = clean_url.replace('/pubhtml', '/pub')
            else:
                pubhtml_url = url
                base_pub = clean_url

            try:
                req = urllib.request.Request(pubhtml_url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    html_data = response.read().decode('utf-8', errors='ignore')
                gids = set(re.findall(r'gid=(\d+)', html_data))
                if gids:
                    urls_to_check = [f"{base_pub}?gid={gid}&single=true&output=csv" for gid in gids]
            except Exception as e_sheet:
                print(f"  [Warning] Google Sheets pubhtml 탭 탐색 실패 ({e_sheet}), 원본 URL로 직접 시도합니다.")

        for target_url in urls_to_check:
            try:
                req = urllib.request.Request(target_url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    csv_data = response.read().decode('utf-8', errors='ignore')
                
                reader = csv.reader(io.StringIO(csv_data))
                for row in reader:
                    for cell in row:
                        matches = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', cell)
                        for m in matches:
                            clean_email = m.strip().lower()
                            if not clean_email.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                emails.add(clean_email)
            except Exception as e_csv:
                print(f"  [Warning] 시트/CSV 다운로드 실패 ({target_url}): {e_csv}")

        subscriber_list = list(emails)
        if subscriber_list:
            print(f"  [구독자 동기화] 총 {len(urls_to_check)}개 시트 검색 완료. 추가 구독자 {len(subscriber_list)}명 확인.")
        return subscriber_list
    except Exception as e:
        print(f"구독자 목록 가져오기 실패: {e}")
        return []

print("Results for /pub?output=csv:", get_additional_subscribers())

