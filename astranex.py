#!/usr/bin/env python3
"""
AstraNex - AI-Powered Penetration Testing Suite
एक ही कमांड में सब कुछ।
"""

import sys
import argparse
from modules import (
    shadow_port, subreaper, webfuzz, vulnhawk,
    secretsnitch, trivy_lite, waf_bypass, sploiter, cloud_hunter
)
from utils.banner import show_banner
from utils.logger import Logger
from utils.ai_helper import ask_ai

log = Logger("AstraNex")

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="AstraNex - All-in-One AI Pentest Suite")
    parser.add_argument("target", help="Target IP, domain or URL")
    parser.add_argument("-m", "--module", help="Specific module to run (1-9 or name)")
    parser.add_argument("--ai", action="store_true", help="Use AI to guide the testing")
    parser.add_argument("--local", action="store_true", help="Use local Ollama instead of API")

    args = parser.parse_args()

    if args.module:
        run_module(args.module, args.target)
    else:
        run_full_scan(args.target, args.ai, args.local)

def run_module(module_id, target):
    modules_map = {
        "1": ("Port Scanner", shadow_port.scan),
        "2": ("Subdomain Finder", subreaper.find),
        "3": ("Web Fuzzer", webfuzz.fuzz),
        "4": ("Vulnerability Scanner", vulnhawk.scan),
        "5": ("Secret Scanner", secretsnitch.scan),
        "6": ("Container/FS Scanner", trivy_lite.scan),
        "7": ("WAF Detector/Bypass", waf_bypass.test),
        "8": ("Auto Exploiter", sploiter.exploit),
        "9": ("Cloud Misconfig Scanner", cloud_hunter.scan),
    }
    # नाम से भी चलाने की सुविधा
    name_map = {v[0].lower().replace(" ", "_"): v[1] for k,v in modules_map.items()}
    if module_id in modules_map:
        func = modules_map[module_id][1]
    elif module_id in name_map:
        func = name_map[module_id]
    else:
        log.error(f"Unknown module: {module_id}")
        sys.exit(1)

    log.info(f"Running module: {module_id}")
    func(target)

def run_full_scan(target, use_ai, local_ai):
    log.info(f"Starting full scan on {target}")
    results = {}

    # स्टेप 1: पोर्ट स्कैन
    results["ports"] = shadow_port.scan(target)

    # अगर वेब पोर्ट खुले हैं तो आगे बढ़ें
    if "80" in results["ports"] or "443" in results["ports"]:
        url = f"http://{target}" if "80" in results["ports"] else f"https://{target}"
        results["subdomains"] = subreaper.find(target)
        results["waf"] = waf_bypass.test(url)
        results["vulns"] = vulnhawk.scan(url)

        if use_ai:
            # AI से पूछें कि आगे क्या करना है
            prompt = f"Target {url} पर ports: {results['ports']}, subdomains: {results['subdomains']}, vulns: {results['vulns']}। अब कौन सा टूल चलाऊं?"
            suggestion = ask_ai(prompt, local=local_ai)
            log.info(f"AI Suggestion: {suggestion}")

    # फाइनल रिपोर्ट
    print("\n[+] Scan Complete. Results saved in logs/")

if __name__ == "__main__":
    main()
