import subprocess
import os
from utils.logger import Logger

log = Logger("TrivyLite")

def scan(target):
    log.info(f"Scanning {target} for vulnerabilities")
    if not os.path.exists(target):
        log.error("Path does not exist")
        return
    # यह trivy कमांड को कॉल करेगा अगर इंस्टॉल है, वरना बेसिक चेक
    try:
        cmd = ["trivy", "filesystem", "--severity", "HIGH,CRITICAL", "--no-progress", target]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        return result.stdout
    except FileNotFoundError:
        log.error("Trivy is not installed. Install it with: apt install trivy")
