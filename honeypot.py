#import necessary packages 
import logging
import paramiko
import socket
import threading

# Set up logging system
logging.basicConfig(filename="honeypot.log", level=logging.INFO)
logHelper = logging.getLogger(__name__)


class HoneyPot(paramiko.ServerInterface):
    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED  # Corrected typo: 'SUCCEEDED'

    def get_allowed_auths(self, username): #allowed authentification methods
        return "password publickey"

    def check_auth_password(self, username, password): #password authentication
        logHelper.info(f"Login attempt: {username}/{password}")
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key): #public key authentication attempts
        logHelper.info(f"Key login attempt: {username}/{key.get_base64()}")
        return paramiko.AUTH_FAILED

"""
creates instance of honeypot server for the specified port and listens for inbound connections


"""
def start_honeypot(port):
    host = paramiko.RSAKey.generate(2048)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("0.0.0.0", port))
        server.listen(5)
        print(f"SSH honeypot on port {port}")
        while True:
            client, addr = server.accept()
            trans = paramiko.Transport(client)
            trans.add_server_key(host)
            server_instance = HoneyPot()
            trans.start_server(server=server_instance)
    except OSError as e:
        logHelper.error(f"Error binding SSH honeypot to port {port}: {e}")


def HTTPhoneypot():
    start_honeypot(80)  # Use port 80 for HTTP connections


def FTPHoneypot():
    start_honeypot(21)  # Use port 21 for FTP connections


if __name__ == "__main__":
    # Start honeypots on different threads
    threading.Thread(target=HTTPhoneypot).start()
    threading.Thread(target=FTPHoneypot).start()
    threading.Thread(target=start_honeypot, args=(22,)).start()  # Explicitly pass port to SSH honeypot