import scythe_helpers.auth as helpers


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

    # Get all modules (via /RPC1)
    result = SCYTHE_API["rpc1"].get_modules()
    for module in result:
        print("%s | %s" % (module['id'], module['name']))

    print("\n ...Exiting.\n")
    exit()
