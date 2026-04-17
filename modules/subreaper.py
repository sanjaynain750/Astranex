import requests
import concurrent.futures
from utils.logger import Logger

log = Logger("SubReaper")

# बिल्ट-इन वर्डलिस्ट (छोटी पर प्रभावी)
SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
    "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test",
    "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3",
    "mail2", "new", "mysql", "old", "lists", "support", "mobile", "mx", "static",
    "docs", "beta", "shop", "sql", "secure", "demo", "cp", "calendar", "wiki",
    "web", "media", "email", "images", "img", "download", "dns", "api", "cdn",
    "staging", "portal", "video", "sip", "dns2", "dns1", "host", "rss", "vps",
]

def check_subdomain(domain, sub):
    url = f"http://{sub}.{domain}"
    try:
        r = requests.get(url, timeout=3, allow_redirects=False)
        if r.status_code < 400:
            return sub
    except:
        pass
    return None

def find(domain):
    log.info(f"Enumerating subdomains for {domain}")
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_subdomain, domain, sub): sub for sub in SUBDOMAINS}
        for future in concurrent.futures.as_completed(futures):
            sub = futures[future]
            result = future.result()
            if result:
                found.append(result)
                log.success(f"Found: {sub}.{domain}")
    return found
