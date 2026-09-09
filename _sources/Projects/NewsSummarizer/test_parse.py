import urllib.request, re, csv, io

SUBSCRIBERS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-8bBBW87Rx5YHf_VoCk2xIvQA9qtbSH00fp0LtBS5_1o7dGQZ21L33NXBcATaWdZ9UoaK_bOT4EQo/pubhtml"

def get_additional_subscribers():
    if not SUBSCRIBERS_CSV_URL:
        return []
    try:
        emails = set()
        urls_to_check = [SUBSCRIBERS_CSV_URL]
        
        if "pubhtml" in SUBSCRIBERS_CSV_URL:
            req = urllib.request.Request(SUBSCRIBERS_CSV_URL)
            with urllib.request.urlopen(req, timeout=10) as response:
                html_data = response.read().decode('utf-8')
            gids = set(re.findall(r'gid=(\d+)', html_data))
            if gids:
                urls_to_check = []
                base_url = SUBSCRIBERS_CSV_URL.split('?')[0].replace("pubhtml", "pub")
                for gid in gids:
                    urls_to_check.append(f"{base_url}?gid={gid}&single=true&output=csv")

        for url in urls_to_check:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                csv_data = response.read().decode('utf-8')
            
            reader = csv.reader(io.StringIO(csv_data))
            for row in reader:
                for cell in row:
                    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', cell)
                    if match:
                        emails.add(match.group(0).strip())
                        
        return list(emails)
    except Exception as e:
        print(f"Failed: {e}")
        return []

print("Emails:", get_additional_subscribers())
