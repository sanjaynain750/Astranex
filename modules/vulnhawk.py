import requests
from utils.logger import Logger

log = Logger("VulnHawk")

# कुछ सरल चेक्स
PAYLOADS = {
    "sql_injection": ["'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1"],
    "xss": ["<script>alert(1)</script>", "\"><script>alert(1)</script>"],
    "lfi": ["../../../../etc/passwd", "....//....//....//etc/passwd"],
}

def check_sqli(url):
    # बहुत बेसिक चेक
    test_url = f"{url}?id=1"
    try:
        normal = requests.get(test_url, timeout=5)
        for payload in PAYLOADS["sql_injection"]:
            r = requests.get(f"{url}?id={payload}", timeout=5)
            if "error" in r.text.lower() or "mysql" in r.text.lower() or "sql" in r.text.lower():
                return True
    except:
        pass
    return False

def scan(target_url):
    log.info(f"Scanning {target_url} for vulnerabilities")
    vulns = []
    if check_sqli(target_url):
        log.warning("Possible SQL Injection vulnerability found!")
        vulns.append({"type": "SQLi", "url": target_url, "param": "id"})
    # आप XSS, LFI आदि के लिए और चेक जोड़ सकते हैं
    return vulns
