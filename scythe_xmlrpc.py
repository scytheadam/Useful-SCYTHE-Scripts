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
        self.sess_id = sess_id
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
    print("Running...\n")

    # Login to SCYTHE & get access to XMLRPC objects
    # NOTE: Domain MUST be formatted ...
    # 'https://<DOMAIN/IP>:<PORT>'
    # ... with NOTHING ELSE! (i.e. no '/RPC' etc.)
    session = login(
        'https://CHANGE_ME_SERVER:8443',
        r'CHANGE_ME_USERNAME',
        'CHANGE_ME_PASSWORD'
    )

    # EXAMPLE: Print Session Key
    print(session)
    # EXAMPLE: Get, then print all current Campaigns (via /RPC1)
    result = SCYTHE_API["rpc1"].current_campaigns()
    print(result)
    # EXAMPLE: Get the first Campaign in result ...
    example_campaign = result[0]
    # EXAMPLE: Campaign's name, to call /RPC2 and get Direct Download Links
    result = SCYTHE_API["rpc2"].get_direct_download_links(
        example_campaign['name']
        )
    # EXAMPLE: Print all Download Links
    print(result)

    print("\n ...Exiting.\n")
    exit()
