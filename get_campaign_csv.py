import scythe_helpers.auth as helpers
import csv
import requests


if __name__ == '__main__':
    print("Running...\n")
    # Optional/helper way to get SCYTHE Credentials via argparse ...
    parser = helpers.setup_cred_args()
    # Add this example's argument
    parser.add_argument(
        '--campaign', required=True,
        help="The desired Campaign's (name) CSV.",
    )
    args = parser.parse_args()

    # Use the optional helper for arguments ...
    SCYTHE_API = helpers.login(
        args.scythe_dest,
        args.scythe_user,
        args.scythe_pass,
    )

    # Setup Download URL
    download_url = "%s/download_report?campaignName=%s&format=csv" % (
        args.scythe_dest,
        args.campaign
    )
    cookies = dict(sessionid=SCYTHE_API['sessionid'])
    result = requests.get(
        download_url,
        cookies=cookies,
        verify=False,
        stream=True
    )
    # Decode the CSV File
    decoded_content = result.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    # Convert to list...
    my_list = list(cr)
    # Make sure there's events...
    if len(my_list) < 2:
        print("ERROR: Campaign '%s' is empty." % args.campaign)
    else:
        # (Example) Print each row
        for row in my_list:
            print(row)

    print("\n ...Exiting.\n")
    exit()
