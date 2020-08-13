import argparse
import json
import os
from scythe_helpers.auth import login


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--jsondir', required=True,
        help='''
            A directory which contains SCYTHE JSON files to import.
        ''',
    )
    args = parser.parse_args()

    print("Running...\n")

    if not os.path.exists(args.jsondir):
        print("Path '%s' not found!" % args.jsondir)
        print("\n ...Exiting.\n")
        exit()

    # Login to SCYTHE & get access to XMLRPC objects
    # NOTE: Domain MUST be formatted ...
    # 'https://<DOMAIN/IP>:<PORT>'
    # ... with NOTHING ELSE! (i.e. no '/RPC' etc.)
    SCYTHE_API = login(
        'https://CHANGE_ME_SERVER:8443',
        r'CHANGE_ME_USERNAME',
        'CHANGE_ME_PASSWORD'
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
            if result is True:
                print("Success!")
            else:
                print("Failed.")

    print("\n ...Exiting.\n")
    exit()
