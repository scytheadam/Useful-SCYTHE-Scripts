import json
import scythe_helpers.auth as helpers


if __name__ == '__main__':
    print("Running...\n")
    # Optional/helper way to get SCYTHE Credentials via argparse ...
    parser = helpers.setup_cred_args()
    # Add this example's arguments
    parser.add_argument(
        '--target', required=True,
        help="The destination (server or relay) IP/Domain.",
    )
    parser.add_argument(
        '--name', required=True,
        help="New Campaign's name.",
    )
    parser.add_argument(
        '--threat', required=False,
        help="Option to build Campaign from a pre-exisiting Threat.",
    )
    args = parser.parse_args()

    # Use the optional helper for arguments ...
    SCYTHE_API = helpers.login(
        args.scythe_dest,
        args.scythe_user,
        args.scythe_pass,
    )

    # Pre-define some empty variables for either Threat or Automation
    threat_name = ""
    campaign_steps = ""
    # If based on a Threat, check to make sure it exists!
    if args.threat:
        print("Looking for (Windows) Threat: '%s'" % args.threat)
        # Use a shortcut API call to confirm Threat exists & get OS
        result = SCYTHE_API["rpc2"].get_threat_operating_system(args.threat)
        # For this example, if it's not a Windows Threat, bail ...
        if result == "":
            print("Error: Threat not found.\n ...Exiting.\n")
            exit()
        elif result != "windows":
            print("Error: Threat not Windows ('%s').\n ...Exiting.\n" % result)
            exit()
        # If all okay, set the Threat Name
        threat_name = args.threat
        print("Found!")
    else:
        # If no threat, let's add some Automation
        campaign_steps = {
            "0":
            {
                "type": "initialization",
                "module": "https",
                "conf":
                {
                    "--cp": "%s:443" % args.target,
                    "--secure": True,
                    "--multipart": 10240
                }
            },
            "1":
                {
                    "type": "message",
                    "module": "loader",
                    "request": "--load run"
                },
            "2":
            {
                "type": "message",
                "module": "run",
                "request": "whoami",
                "rtags":
                [
                    "scythe",
                    "att&ck",
                    "att&ck-tactic:TA0007",
                    "att&ck-technique:T1033"
                ]
            }
        }
        # Lastly, need to format to JSON
        campaign_steps = json.dumps(campaign_steps)
    # ... end Else

    # Setup a object campaign object ...
    campaign = {
        'threatName': threat_name,
        'campaignName': args.name,
        'operatingSystem': "windows",
        'campaignBoundary': "", 'startDate': "", 'endDate': "",
        'delivery': "physical", 'emailFrom': "", 'emailRecipients': "",
        'emailSubject': "", 'emailBody': "", 'drivebyBody': "",
        'modules': [
            {
                "conf":
                    {
                        "--cp": "%s:443" % args.target,
                        "--secure": True,
                        "--multipart": 10240
                    },
                "name": "https"
            },
            {
                "conf": {},
                "name": "controller"
            },
            {
                "conf": {},
                "name": "loader"
            }
        ],
        'steps': campaign_steps,
        'emailAttachment': "",
        'avoidance_options':
        {
            "modify_pdb": "manually_set.pdb",
            "modify_timestamp": "2025-08-25T16:39:54"
        }
    }

    print("\nAttempting to create Campaign '%s' ... " % args.name)
    # Now create the campaign ...
    result = SCYTHE_API["rpc2"].start_campaign(
        campaign['threatName'],
        campaign['campaignName'],
        campaign['operatingSystem'],
        campaign['campaignBoundary'],
        campaign['startDate'], campaign['endDate'],
        campaign['delivery'], campaign['emailFrom'],
        campaign['emailRecipients'], campaign['emailSubject'],
        campaign['emailBody'], campaign['drivebyBody'],
        json.dumps(campaign['modules']),
        campaign['steps'],
        campaign['emailAttachment'],
        json.dumps(campaign['avoidance_options'])
    )
    print(result)

    # Using Campaign's name, get Direct Download Links ...
    result = SCYTHE_API["rpc2"].get_direct_download_links(args.name)
    # Output accordingly ...
    print("\nDirect Download Links for '%s' ... " % args.name)
    print("\n64-bit EXE:\t%s" % result['active']['false'])
    print("64-bit DLL:\t%s" % result['passive']['false'])
    print("64-bit Reflective Loader + DLL:\t%s" % result['output']['false'])
    print("\n32-bit EXE:\t%s" % result['active']['true'])
    print("32-bit DLL:\t%s" % result['passive']['true'])
    print("32-bit Reflective Loader + DLL:\t%s" % result['output']['true'])

    print("\n ...Exiting.\n")
    exit()
