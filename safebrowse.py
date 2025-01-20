from pysafebrowsing import SafeBrowsing

key = "AIzaSyDWBFkXMqoFM_7QTtEyH-6XLg3aI38dxpI"
s = SafeBrowsing(key)



r = s.lookup_urls(['https://telegrnm.cc/'])
print(r)