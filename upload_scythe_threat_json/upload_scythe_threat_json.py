import argparse
import json
import os
import ssl
import xmlrpc.client


# The Global SCYTHE RPC Locations we will set/call
SCYTHE_API = {}


# Helper Class to setup the connections to SCYTHE
class SecureCookieTransport(xmlrpc.client.SafeTransport):
    def __init__(self, sess_id):
        xmlrpc.client.SafeTransport.__init__(
            self, context=ssl._create_unverified_context()
        )
        self.sess_id = sess_id[0]
        self._connection = (None, None)
        self._use_datetime = 0

    def send_content(self, connection, request_body):
        connection.putheader("Content-Type", "text/xml")
        connection.putheader("Cookie", "sessionid=%s" % self.sess_id)
        connection.putheader("Content-Length", str(len(request_body)))
        connection.endheaders(request_body)


# Helper Function to Login to SCYTHE, Setup XMLRPC Listeners
def login(target_url=None, username=None, password=None):
    try:
        # Setup connection, ignoring SSL cert issues
        svr = xmlrpc.client.ServerProxy(
            "%s/RPC1" % target_url,
            context=ssl._create_unverified_context()
        )
        # Get Session ID
        sess_id = svr.login(username, password)
        # Assign the Global Variables
        SCYTHE_API["rpc1"] = \
            xmlrpc.client.ServerProxy(
                "%s/RPC1" % target_url,
                transport=SecureCookieTransport(sess_id)
            )
        SCYTHE_API["rpc2"] = \
            xmlrpc.client.ServerProxy(
                "%s/RPC2" % target_url,
                transport=SecureCookieTransport(sess_id)
            )
        return sess_id
    except Exception as e:
        return e


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
    session = login(
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
            data = json.load(json_file)
            result = SCYTHE_API["rpc2"].read_in_threat_from_json(
                data['threat']
            )
            if result is True:
                print("Success!")
            else:
                print("Failed.")

    print("\n ...Exiting.\n")
    exit()
