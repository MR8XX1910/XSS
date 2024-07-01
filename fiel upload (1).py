import requests
from bs4 import BeautifulSoup
from googlesearch import search
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style

# تهيئة مكتبة colorama
init(autoreset=True)

# دالة للتحقق من الثغرة
def check_vulnerability(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and 'upload' in response.text.lower():
            return url, True
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
    return url, False

# دالة للبحث عن المواقع في دولة معينة
def search_sites(query, num_results):
    return search(query, num_results=num_results, lang='en')

# المدخلات من المستخدم
country = input("أدخل اسم الدولة: ")
site_limit = int(input("أدخل عدد المواقع المراد فحصها: "))

# إعداد استعلام البحث
query = f'site:.{country} "file upload"'

# البحث عن المواقع
websites = search_sites(query, site_limit)

# تخزين النتائج
results = []

# تفقد كل موقع في القائمة باستخدام البرمجة المتوازية
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_url = {executor.submit(check_vulnerability, site): site for site in websites}
    for future in future_to_url:
        url, is_vulnerable = future.result()
        results.append((url, is_vulnerable))

# طباعة النتائج مرتبة
for url, is_vulnerable in sorted(results, key=lambda x: x[1], reverse=True):
    if is_vulnerable:
        print(f"{Fore.GREEN}{url} مصاب بثغرة upload file")
    else:
        print(f"{Fore.RED}{url} غير مصاب بثغرة upload file")