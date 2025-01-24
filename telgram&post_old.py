#!/usr/bin/env python
# Copyright (c) 2017 @x0rz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
import re
import math

import certstream
import tqdm
import yaml
import time
import os
from Levenshtein import distance
from termcolor import colored, cprint
from tld import get_tld
import subprocess
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
import os
import time 

import threading


certstream_url = 'wss://certstream.calidog.io'
log_suspicious = os.path.dirname(os.path.realpath(__file__))+'/suspicious_domains_'+time.strftime("%Y-%m-%d")+'.log'
suspicious_yaml = os.path.dirname(os.path.realpath(__file__))+'/suspicious.yaml'
external_yaml = os.path.dirname(os.path.realpath(__file__))+'/external.yaml'
pbar = tqdm.tqdm(desc='certificate_update', unit='cert') #progress bar

def take_screenshot(URL, timeout, output_file):
    # Validate IP address format
    import re
    # ipv4_pattern = r'\b((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b'
    # if not re.match(ipv4_pattern, ip_address):
    #     print("Invalid IP address format.")
    #     return

    # Prepare Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for better compatibility
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size

    # Set up the Chrome WebDriver
    service = Service("./chromedriver")  # Replace "chromedriver" with the path to your ChromeDriver if necessary
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Construct the URL
        url = f"https://{URL}"
        print(f"Accessing {url}...")
        
        #Set timeout
        driver.set_page_load_timeout(timeout)
        # Open the website
        driver.get(url)

        # Take a screenshot
        screenshot_path = os.path.abspath(output_file)
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved as: {screenshot_path}")
    
    except Exception as e:
        print(f"An error occurred: time to move on")
    
    finally:
        driver.quit()

def find_ip_addresses(input_string):
    # Regular expression for IPv4 addresses
    ipv4_pattern = r'((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])'

    # Regular expression for simplified IPv6 addresses
    ipv6_pattern = r'\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b'

    # Combine both patterns
    ip_pattern = f'({ipv4_pattern})|({ipv6_pattern})'

    # Find all matches
    matches = re.findall(ip_pattern, input_string)

    # Extract IPv4 and IPv6 addresses from matches
    ip_addresses = [match[0] if match[0] else match[1] for match in matches]

    return ip_addresses

def entropy(string):
    """Calculates the Shannon entropy of a string"""
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return entropy

def score_domain(domain):
    """Score `domain`.

    The highest score, the most probable `domain` is a phishing site.

    Args:
        domain (str): the domain to check.

    Returns:
        int: the score of `domain`.
    """
    score = 0

    if "telegraph" in domain:
        return 0

    if len(domain) >= 20:
        return 0
    # for t in suspicious['tlds']: # ends in weird tld
    #     if domain.endswith(t):
    #         score += 20

    # # Remove initial '*.' for wildcard certificates bug
    # if domain.startswith('*.'):
    #     domain = domain[2:]

    # # Removing TLD to catch inner TLD in subdomain (ie. paypal.com.domain.com --> paypal.com.domain)
    # try:
    #     res = get_tld(domain, as_object=True, fail_silently=True, fix_protocol=True)
    #     domain = '.'.join([res.subdomain, res.domain])
    # except Exception:
    #     pass

    # # Higer entropy is kind of suspicious
    # score += int(round(entropy(domain)*10))

    # # Remove lookalike characters using list from http://www.unicode.org/reports/tr39 (e.g 1 --> l)
    # domain = unconfuse(domain)

    words_in_domain = re.split("\W+", domain) # ("\W+" = .)
    words_in_domain_dash = re.split("-", domain)
    

    # # ie. detect fake .com (ie. *.com-account-management.info)
    # if words_in_domain[0] in ['com', 'net', 'org']:
    #     score += 10

    # Testing keywords
    for word in suspicious['keywords']:
        if word in domain:
            score += suspicious['keywords'][word]
        if domain.find(word) != -1:
            score += suspicious['keywords'][word]
    
    # Testing Levenshtein distance for strong keywords (>= 70 points) (ie. paypol)
    for key in [k for (k,s) in suspicious['keywords'].items() if s >= 70 and len(k) > 7]:
        # Removing too generic keywords (ie. mail.domain.com)
        for word in [w for w in words_in_domain if w not in ['email', 'mail', 'cloud']]:
            if distance(str(word), str(key)) == 1:
                score += 100
        for word in [w for w in words_in_domain_dash if w not in ['email', 'mail', 'cloud']]:
            if distance(str(word), str(key)) == 1:
                score += 100

    # # Lots of '-' (ie. www.paypal-datacenter.com-acccount-alert.com)
    # if 'xn--' not in domain and domain.count('-') >= 4:
    #     score += domain.count('-') * 3

    # # Deeply nested subdomains (ie. www.paypal.com.security.accountupdate.gq)
    # if domain.count('.') >= 3:
    #     score += domain.count('.') * 3

    

    return score


def callback(message, context):
    """Callback handler for certstream events."""
    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        for domain in all_domains:
            pbar.update(1)
            score = score_domain(domain.lower())

            # If issued from a free CA = more suspicious
            if "Let's Encrypt" == message['data']['leaf_cert']['issuer']['O']:
                score += 10

            if score >= 100:
                tqdm.tqdm.write(
                    "[!] Suspicious: "
                    "{} (score={})".format(colored(domain, 'red', attrs=['underline', 'bold']), score))
            elif score >= 90:
                tqdm.tqdm.write(
                    "[!] Suspicious: "
                    "{} (score={})".format(colored(domain, 'red', attrs=['underline']), score))
            elif score >= 80:
                tqdm.tqdm.write(
                    "[!] Likely    : "
                    "{} (score={})".format(colored(domain, 'yellow', attrs=['underline']), score))
            elif score >= 65:
                tqdm.tqdm.write(
                    "[+] Potential : "
                    "{} (score={})".format(colored(domain, attrs=['underline']), score))

            if score >= 75:
                # subprocess.run(["echo", "\"{}\"".format(domain.lower()), "|" , "/zdns/zdns", "A"])
                res = subprocess.run(["./zdns/zdns", "A", "\"{}\"".format(domain.lower()), "--verbosity=1"], capture_output=True)
                zdns_output = str(res)

                #print("printti:",zdns_output)
                URL_fake = zdns_output.find("NXDOMAIN") # Not found
                URL_real = zdns_output.find("NOERROR") # Found
                if URL_fake != -1:
                    print("Did not find website/IP @ behind URL:", domain.lower())
                if URL_real != -1:
                    print("Found website/IP @ behind URL:", (domain).lower())

                    ip_addresses = find_ip_addresses(zdns_output)
                    
                    timeout = 7
                    if ip_addresses:
                        print("Found IP addresses:")
                        take_screenshot(domain, timeout=timeout, output_file=("./ssOverNight/nopath/"+domain+".png").lower())
                        
                        common_paths = ["login", "app", "en"]

                        for path in common_paths:
                            take_screenshot(domain+"/"+path, timeout=timeout, output_file=("./ssOverNight/"+path+"/"+domain+".png").lower())
                with open(log_suspicious, 'a') as f:
                    f.write("{}\n".format(domain))


if __name__ == '__main__':
    with open(suspicious_yaml, 'r') as f:
        suspicious = yaml.safe_load(f)

    with open(external_yaml, 'r') as f:
        external = yaml.safe_load(f)

    if external['override_suspicious.yaml'] is True:
        suspicious = external
    else:
        if external['keywords'] is not None:
            suspicious['keywords'].update(external['keywords'])

        if external['tlds'] is not None:
            suspicious['tlds'].update(external['tlds'])

    
    certstream.listen_for_events(callback, url=certstream_url)
