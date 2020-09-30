import urllib3
from urllib3 import HTTPSConnectionPool
import certifi
import base64
import M2Crypto
import hashlib
import sys
from urllib3 import ProxyManager, make_headers
import ssl

class TryingFromProxyError(Exception):
    def __str__(self):
        return 'The sha256 for SSL certificate did not matched with our system'

class TestHTTPSConnectionPool(HTTPSConnectionPool):
    def _validate_conn(self, conn):
        super(TestHTTPSConnectionPool, self)._validate_conn(conn)
        pinset = [
            'dbe20600cd8420abc8f3dda6eccfb33b161a2eacb39f464fa212facf9e2731a2', # correct ones
            # 'dbe20600cd8420abc8f3dda6eccfb33b161a2eacb39f464fa212facf9e2731a1', # incorrect ones
            # 'a8f2381ad85c44b13803eb9ebe361910b4ef1252da889bc50953d4b7b49adc4d', # burp-proxy
        ]
        if not conn.is_verified:
            print("Connection is not verified")
            return False

        der = conn.sock.getpeercert(binary_form=True)
        x509 = M2Crypto.X509.load_cert_string(der, M2Crypto.X509.FORMAT_DER)
        mem = M2Crypto.BIO.MemoryBuffer()
        public_key = x509.get_pubkey().get_rsa().save_pub_key_bio(mem)
        pk_der = mem.getvalue().decode().split('\n')[1:-2]
        pk_base64 = ''.join(pk_der)
        pk_raw = base64.b64decode(pk_base64)
        pk_sha256 = hashlib.sha256(pk_raw).hexdigest()

        # print('sha: ', pk_sha256)

        if pk_sha256 in pinset:
            pass
        else:
            print("SHASUM: ", pk_sha256)
            raise TryingFromProxyError

# print('certifi :  ', certifi.where())

port = 9000
if len(sys.argv) == 2:
    port = int(sys.argv[-1])
    print(port)
# ca_certs = '/etc/ssl/certs/ca-certificates.crt'
ca_certs = 'new/new-cacert.pem'

pool = TestHTTPSConnectionPool(
    'cod-avatar.com',
    port,
    cert_reqs='CERT_REQUIRED',
    ca_certs=ca_certs
)

print("\nTrying to get from server directly")
rv = pool.urlopen('GET', '/')
print('-------RESPONSE-START---------')
print(rv.data)
print('--------RESPONSE-END---------')

# import time; time.sleep(1)
_ = input('\n\nPress Enter to go through proxy')

pool_with_proxy = TestHTTPSConnectionPool(
    'cod-avatar.com',
    port=port,
    cert_reqs='CERT_REQUIRED',
    ca_certs=ca_certs,
    _proxy=ProxyManager('https://127.0.0.1:8080').proxy,
    
)

# import ipdb;ipdb.set_trace()
print("\nTrying to get from proxy")
r = pool_with_proxy.urlopen('GET', '/')
print(r.data)
