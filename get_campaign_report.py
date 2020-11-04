import scythe_helpers.auth as helpers
from pprint import pprint


if __name__ == '__main__':
    print("Running...\n")
    # Optional/helper way to get SCYTHE Credentials via argparse ...
    parser = helpers.setup_cred_args()
    args = parser.parse_args()

    # Use the optional helper for arguments ...
    SCYTHE_API = helpers.login(
        args.scythe_dest,
        args.scythe_user,
        args.scythe_pass,
    )

    # Get all Campaigns (via /RPC1)
    result = SCYTHE_API["rpc1"].current_campaigns_report()
    for campaign in result:
        print("\n----------%s----------" % campaign['name'])
        pprint(campaign, indent=4)

    print("\n ...Exiting.\n")
    exit()
