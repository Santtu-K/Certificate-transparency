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

#from confusables import unconfuse

certstream_url = 'wss://certstream.calidog.io'

log_suspicious = os.path.dirname(os.path.realpath(__file__))+'/suspicious_domains_'+time.strftime("%Y-%m-%d")+'.log'

suspicious_yaml = os.path.dirname(os.path.realpath(__file__))+'/suspicious.yaml'

external_yaml = os.path.dirname(os.path.realpath(__file__))+'/external.yaml'



#pbar = tqdm.tqdm(desc='certificate_update', unit='cert')


# print("log_suspicious:",log_suspicious)

# print("suspicious_yaml:",suspicious_yaml)

# testi = os.path.realpath(__file__)
# print("testi:",testi)

# testi = os.path.dirname("/nuppi/nappi/tappi")
# print("testi:",testi)



from confusables import unconfuse

domain = "paypal.com.domain.com"
words_in_domain = re.split("\W+", domain)

merkkijono = "testa1lua 0mena 11 𝓗℮𝐥1೦ 𝓗℮𝐥1೦" #𝓗℮𝐥1೦

hamm = unconfuse(merkkijono)
print("hamm:", hamm)


def testi(muuttuja):
    print("tstaus:", muuttuja + tuntematon)

tuntematon = 10

testi(20)

with open(suspicious_yaml, 'r') as f:
        suspicious = yaml.safe_load(f)

print("sus:", type(suspicious))

sk = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "year": 1999,

  "kw": {"perse": "kuusysi", "kassi": 420}
}

print("sk:", sk)
print("ali:", sk["kw"]["kassi"])

score = 0
for word in suspicious['keywords']:
    if word in domain:
        print("word:", word)
        print("poang:", suspicious['keywords'][word])
        score += suspicious['keywords'][word]

print("score1:", score)


for key in [k for (k,s) in suspicious['keywords'].items() if s >= 70]:
    # Removing too generic keywords (ie. mail.domain.com)
    for word in [w for w in words_in_domain if w not in ['email', 'mail', 'cloud']]:
        if distance(str(word), str(key)) == 1:
            score += 70

print("dom:", domain)
print("wid:", words_in_domain)

for word in [w for w in words_in_domain if w not in ['paypal', 'mail', 'cloud']]:
    print("hepulihei:", word)
    if distance(str(word), str(key)) == 1:
        score += 70

alus = 'xn--'

print("xn--", alus)


domain = "paypal.com.domain.com"



print("wrdsindom:", words_in_domain)

res = get_tld(domain, as_object=True, fail_silently=True, fix_protocol=True)
print("res:", res)
domain = '.'.join([res.subdomain, res.domain])
print("domain:",domain)
print("yrit:", 'vipatin'.join(["TOIMI", "KYLA"]))