"""
Generate self-signed SSL certificates for Flask HTTPS development
Run this script once to create the certificates
"""

import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import ipaddress

def generate_self_signed_cert():
    """Generate self-signed SSL certificate for localhost"""
    
    # Create certificates directory if it doesn't exist
    cert_dir = "security/ssl"
    os.makedirs(cert_dir, exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Various details about who we are. For a self-signed certificate the
    # subject and issuer are always the same.
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Development"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Local"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"API Logic Server"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    
    # Certificate valid for 365 days
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # Certificate valid for 1 year
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        # Add Subject Alternative Names for localhost variations
        x509.SubjectAlternativeName([
            x509.DNSName(u"localhost"),
            x509.DNSName(u"127.0.0.1"),
            x509.DNSName(u"0.0.0.0"),
            x509.IPAddress(ipaddress.IPv4Address(u"127.0.0.1")),
            x509.IPAddress(ipaddress.IPv4Address(u"0.0.0.0")),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Write private key to file
    key_path = os.path.join(cert_dir, "server.key")
    with open(key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Write certificate to file
    cert_path = os.path.join(cert_dir, "server.crt")
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print(f"✅ SSL certificates generated successfully!")
    print(f"📁 Certificate: {cert_path}")
    print(f"🔑 Private Key: {key_path}")
    print(f"⚠️  Note: This is a self-signed certificate for development only")
    print(f"🌐 Valid for: localhost, 127.0.0.1, 0.0.0.0")
    
    return cert_path, key_path

if __name__ == "__main__":
    try:
        generate_self_signed_cert()
    except ImportError as e:
        print("❌ Missing required package. Install with:")
        print("pip install cryptography")
    except Exception as e:
        print(f"❌ Error generating certificates: {e}")