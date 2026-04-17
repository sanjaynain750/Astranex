import requests
from utils.logger import Logger

log = Logger("CloudHunter")

def check_s3_bucket(bucket_name):
    url = f"http://{bucket_name}.s3.amazonaws.com"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return True
    except:
        pass
    return False

def scan(domain):
    # अगर domain में s3 जैसा कुछ है तो चेक करें
    log.info(f"Checking cloud misconfigurations for {domain}")
    # यहाँ आप और चेक्स जोड़ सकते हैं (Azure Blob, GCP Buckets)
    findings = []
    if check_s3_bucket(domain):
        findings.append(f"Public S3 bucket: {domain}")
        log.warning(f"Public S3 bucket found: {domain}")
    return findings
