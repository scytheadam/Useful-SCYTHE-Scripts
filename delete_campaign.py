import scythe_helpers.auth as helpers


if __name__ == '__main__':
    print("Running...\n")
    # Optional/helper way to get SCYTHE Credentials via argparse ...
    parser = helpers.setup_cred_args()
    # Add this example's arguments
    parser.add_argument(
        '--campaign', required=True,
        help="Name of the Campaign to delete.",
    )
    args = parser.parse_args()

    # Use the optional helper for arguments ...
    SCYTHE_API = helpers.login(
        args.scythe_dest,
        args.scythe_user,
        args.scythe_pass,
    )

    # Delete campaign...
    result = SCYTHE_API["rpc1"].delete_campaign(args.campaign)
    print(result)

    print("\n ...Exiting.\n")
    exit()
