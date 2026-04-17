import requests
import concurrent.futures
from utils.logger import Logger

log = Logger("WebFuzz")

# डिफ़ॉल्ट वर्डलिस्ट (आप wordlists/common.txt से भी लोड कर सकते हैं)
DIRS = ["admin", "backup", "config", "data", "db", "debug", "default", "dev",
        "files", "include", "js", "lib", "logs", "login", "old", "phpmyadmin",
        "private", "robots.txt", "secret", "sql", "src", "test", "tmp", "upload",
        "user", "var", "vendor", "web", "wp-admin", "wp-content", "wp-includes"]

def check_path(url, path):
    full_url = f"{url.rstrip('/')}/{path}"
    try:
        r = requests.get(full_url, timeout=5, allow_redirects=False)
        if r.status_code in [200, 301, 302, 403]:
            return (path, r.status_code)
    except:
        pass
    return None

def fuzz(target_url):
    log.info(f"Fuzzing directories on {target_url}")
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(check_path, target_url, d): d for d in DIRS}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found.append(result)
                log.success(f"Found: /{result[0]} [{result[1]}]")
    return found
