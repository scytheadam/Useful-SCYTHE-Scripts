import argparse
import ssl
import xmlrpc.client


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
        # Create a return API object
        SCYTHE_API = {}
        # Setup connection, ignoring SSL cert issues
        svr = xmlrpc.client.ServerProxy(
            "%s/RPC1" % target_url,
            context=ssl._create_unverified_context()
        )
        # Get Session ID
        sess_id = svr.login(username, password)
        # Assign the Global Variables
        SCYTHE_API["sessionid"] = sess_id[0]
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
        return SCYTHE_API
    except Exception as e:
        return e


# Helper Function to setup SCYTHE login details
def setup_cred_args(parser=None):
    # Create a parser object if there is none ...
    if parser is None:
        parser = argparse.ArgumentParser()
    # Add the required SCYTHE arguments ...
    parser.add_argument(
        '--scythe-dest', required=True,
        help='''
            The URL/Domain/IP and Port of SCYTHE Server.
            Destination MUST be formatted:
            "https://<DOMAIN/IP>:<PORT>"
            with NOTHING ELSE! (i.e. no '/RPC' etc.)
        ''',
    )
    parser.add_argument(
        '--scythe-user', required=False,
        default=r"BUILTIN\scythe",
        help=r'''
            SCYTHE user to login as. Default: "BUILTIN\scythe"
        ''',
    )
    parser.add_argument(
        '--scythe-pass', required=True,
        help='''
            SCYTHE user password.
        ''',
    )

    return parser
