import certstream

def print_callback (message, context) :
# Callback handler for certificate update events """ 
    if message["message_type"] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']
# Here we print all the domains. 
        for domain in all_domains:
            print (domain)
certstream.listen_for_events(print_callback, url="wss://certstream.calidog.io")