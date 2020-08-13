from scythe_helpers.auth import login

if __name__ == '__main__':
    print("Running...\n")

    # Login to SCYTHE & get access to XMLRPC objects
    # NOTE: Domain MUST be formatted ...
    # 'https://<DOMAIN/IP>:<PORT>'
    # ... with NOTHING ELSE! (i.e. no '/RPC' etc.)
    SCYTHE_API = login(
        'https://CHANGE_ME_SERVER:8443',
        r'CHANGE_ME_USERNAME',
        'CHANGE_ME_PASSWORD'
    )

    # EXAMPLE: Print Session Key
    print(SCYTHE_API["sessionid"])
    # EXAMPLE: Get, then print all current Campaigns (via /RPC1)
    result = SCYTHE_API["rpc1"].current_campaigns()
    print(result)
    # EXAMPLE: Get the first Campaign in result ...
    example_campaign = result[0]
    # EXAMPLE: Campaign's name, to call /RPC2 and get Direct Download Links
    result = SCYTHE_API["rpc2"].get_direct_download_links(
        example_campaign['name']
        )
    # EXAMPLE: Print all Download Links
    print(result)

    print("\n ...Exiting.\n")
    exit()
