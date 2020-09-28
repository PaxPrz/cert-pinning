import urllib3
from urllib3 import HTTPSConnectionPool
import certifi
import base64
import M2Crypto
import hashlib

class TestHTTPSConnectionPool(HTTPSConnectionPool):
    def _validate_conn(self, conn):
        super(TestHTTPSConnectionPool, self)._validate_conn(conn)
        pinset = [
            'dbe20600cd8420abc8f3dda6eccfb33b161a2eacb39f464fa212facf9e2731a2'
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
            raise Exception('Invalid public key set!')

# print('certifi :  ', certifi.where())

pool = TestHTTPSConnectionPool(
    'cod-avatar.com',
    9000,
    cert_reqs='CERT_REQUIRED',
    ca_certs='new/cert.pem'
)

rv = pool.urlopen('GET', 'https://cod-avatar.com:9000/')
print(rv.data)