import auth

hssc = auth.HolmSecurityScannerClass("<username>", "<password>")

id = hssc.startWebScan(name="Example Job", 
                       schedule_is_active=False, 
                       node_source_overrides=False, 
                       is_was_discovery=True, 
                       assets=[41150], 
                       scheduled=False)

print hssc.getWebScan(id).text
