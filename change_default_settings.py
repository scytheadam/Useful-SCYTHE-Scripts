import scythe_helpers.auth as helpers


if __name__ == '__main__':
    print("Running...\n")
    # Optional/helper way to get SCYTHE Credentials via argparse ...
    parser = helpers.setup_cred_args()
    # Add this example's arguments
    parser.add_argument(
        '--target', required=True,
        help="Update your Download Links & HTTPS settings to this IP/Domain.",
    )
    args = parser.parse_args()

    # Use the optional helper for arguments ...
    SCYTHE_API = helpers.login(
        args.scythe_dest,
        args.scythe_user,
        args.scythe_pass,
    )

    # First, change the Download Link setting ...
    print("\nChanging Driveby Website to:\n'%s'" % args.target)
    result = SCYTHE_API["rpc1"].update_setting(
        "drivebysite",
        args.target
    )
    print(result)

    # Then, change the HTTPS setting ...
    new_https = "--cp %s:443 --secure true --multipart 10240" % args.target
    print("\nChanging HTTPS default to: \n'%s'" % new_https)
    result = SCYTHE_API["rpc1"].update_setting(
        "https_default_params",
        new_https
    )
    print(result)

    print("\n ...Exiting.\n")
    exit()
