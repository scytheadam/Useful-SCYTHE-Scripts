import scythe_helpers.auth as helpers
import requests


def download_payload(download_url, cookies, filename):
    # Get the file
    result = requests.get(
        download_url,
        cookies=cookies,
        verify=False,
        stream=True
    )
    if result.status_code != 200:
        print(
            "\nERROR: Failed to download '%s' from '%s'!\n" % (
                filename,
                download_url
            )
        )
        return False
    # Create the  File
    open(
        filename,
        'wb'
    ).write(result.content)
    print("Created: '%s'!" % filename)
    return True


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
        '--entrypoint', default="PlatformClientMain",
        help="The Entrypoint Function name for the DLL payload.",
    )
    args = parser.parse_args()

    # Use the optional helper for arguments ...
    SCYTHE_API = helpers.login(
        args.scythe_dest,
        args.scythe_user,
        args.scythe_pass,
    )

    # Setup Cookies
    cookies = dict(sessionid=SCYTHE_API['sessionid'])

    # Setup Download URL for 64 bit EXE
    download_url = (
        "%s/download_client?"
        "campaignName=%s"
        "&architectureType=x64"
        ) % (
        args.scythe_dest,
        args.campaign
    )
    print(download_url)
    filename = "%s_scythe_client64.exe" % args.campaign
    # Download file...
    download_payload(download_url, cookies, filename)\

    # Setup Download URL for 64 bit DLL
    download_url = (
        "%s/download_client?"
        "campaignName=%s"
        "&architectureType=x64&dll=1"
        "&entryPoint=%s"
        ) % (
        args.scythe_dest,
        args.campaign,
        args.entrypoint
    )
    print(download_url)
    filename = "%s_scythe_client64.dll" % args.campaign
    # Download file...
    download_payload(download_url, cookies, filename)

    print("\n ...Exiting.\n")
    exit()
