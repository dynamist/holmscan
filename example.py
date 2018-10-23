from holmscan.auth import HolmSecurityWeb

# Creates a session with the Holm Security Scanning APIs
hsw = HolmSecurityWeb("<username>", "<password>")

# Starts a Web Application Discovery Scan on a pre created asset
# and gets id of running job back
id = hsw.startWebScan(name="Example Job", 
                       schedule_is_active=False, 
                       node_source_overrides=False, 
                       is_was_discovery=True, 
                       assets=[41150], 
                       scheduled=False)

# Gets information about running job using ID 
print hsw.getWebScan(id).text
