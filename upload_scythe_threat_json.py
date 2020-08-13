import argparse
import json
import os
import scythe_helpers.auth as helpers


if __name__ == '__main__':
    print("Running...\n")

    parser = argparse.ArgumentParser()
    # Optional/helper way to get SCYTHE Credentials via argparse ...
    parser = helpers.setup_cred_args(parser)
    # Add this example's arguments
    parser.add_argument(
        '--jsondir', required=True,
        help='''
            A directory which contains SCYTHE JSON files to import.
        ''',
    )
    args = parser.parse_args()

    # Check for the target local json dir
    if not os.path.exists(args.jsondir):
        print("Path '%s' not found!" % args.jsondir)
        print("\n ...Exiting.\n")
        exit()

    # Use the optional helper for arguments ...
    SCYTHE_API = helpers.login(
        args.scythe_dest,
        args.scythe_user,
        args.scythe_pass,
    )

    # Loop all JSON files in target Dir
    for file_name in [
        file for file in os.listdir(args.jsondir) if file.endswith('.json')
            ]:
        with open(args.jsondir + file_name) as json_file:
            print("\nUploading '%s'..." % file_name)
            try:
                data = json.load(json_file)
                result = SCYTHE_API["rpc2"].read_in_threat_from_json(
                    data['threat']
                )
            except KeyError as e:
                print("KeyError on %s. Probably not a SCYTHE Threat JSON." % e)
            except TypeError as e:
                print("TypeError on %s. Probably a login failure." % e)
                break
            if result is True:
                print("Success!")
            else:
                print("Failed.")

    print("\n ...Exiting.\n")
    exit()
