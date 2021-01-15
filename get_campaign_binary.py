import scythe_helpers.auth as helpers


if __name__ == '__main__':
    print("Running...\n")
    # Optional/helper way to get SCYTHE Credentials via argparse ...
    parser = helpers.setup_cred_args()
    # Add this example's arguments
    parser.add_argument(
        '--campaign', required=True,
        help="The desired Campaign (name).",
    )
    parser.add_argument(
        '--os', required=True,
        help="The desired Campaign's OS ('windows', 'macos', 'linux').",
    )
    args = parser.parse_args()

    # Use the optional helper for arguments ...
    SCYTHE_API = helpers.login(
        args.scythe_dest,
        args.scythe_user,
        args.scythe_pass,
    )

    # Get the payload
    # Arch's availble, ['x86', 'x64']
    arch = "x64"
    result = SCYTHE_API["rpc1"].binary_client(args.campaign, args.os, arch)
    # Define filename
    filename = "%s_scythe_client_%s_%s.scythe.bin" % (args.campaign, args.os, arch)
    # Create the File
    open(
        filename,
        'wb'
    ).write(bytearray(result.data))
    print("Created: '%s'!" % filename)
    # Done!
    print("\n ...Exiting.\n")
    exit()
