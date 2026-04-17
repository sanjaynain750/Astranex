import re
import os
from utils.logger import Logger

log = Logger("SecretSnitch")

# रेगेक्स पैटर्न्स
PATTERNS = {
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret": r"[0-9a-zA-Z/+]{40}",
    "Google API": r"AIza[0-9A-Za-z\-_]{35}",
    "GitHub Token": r"ghp_[0-9a-zA-Z]{36}",
    "Private Key": r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----",
    "Password in URL": r"(?:user|pass|pwd|password)=([^&]+)",
}

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for name, pattern in PATTERNS.items():
                matches = re.findall(pattern, content)
                for match in matches:
                    findings.append((name, match))
    except:
        pass
    return findings

def scan(target_path):
    log.info(f"Scanning {target_path} for secrets...")
    all_findings = []
    if os.path.isfile(target_path):
        all_findings = scan_file(target_path)
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                filepath = os.path.join(root, file)
                findings = scan_file(filepath)
                if findings:
                    all_findings.extend(findings)
                    log.warning(f"Found secrets in {filepath}")
    return all_findings
