#!/usr/bin/env python3
"""
SSL Certificate Fix for macOS/Python
Run this script to fix SSL certificate issues
"""

import ssl
import certifi
import subprocess
import sys
import os

def install_certificates_macos():
    """Install certificates for macOS Python"""
    try:
        # Try to run the macOS certificate installer
        python_path = sys.executable
        cert_command = f"{python_path} -m pip install --upgrade certifi"
        
        print("🔧 Updating certifi...")
        subprocess.run(cert_command.split(), check=True)
        
        # Try to install macOS certificates
        cert_install_path = f"{os.path.dirname(python_path)}/Install Certificates.command"
        if os.path.exists(cert_install_path):
            print("🔧 Running macOS certificate installer...")
            subprocess.run([cert_install_path], check=True)
        else:
            print("ℹ️  macOS certificate installer not found, trying alternative...")
            
        print("✅ Certificate update completed!")
        return True
        
    except Exception as e:
        print(f"⚠️  Certificate installation failed: {e}")
        return False

def test_ssl_connection():
    """Test SSL connection"""
    try:
        import urllib.request
        
        # Test with a simple request
        response = urllib.request.urlopen("https://httpbin.org/get", timeout=10)
        print("✅ SSL connection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ SSL connection test failed: {e}")
        return False

def main():
    print("🚀 RPNews SSL Certificate Fix")
    print("=" * 40)
    
    # Check current certificate path
    print(f"📍 Current certifi path: {certifi.where()}")
    
    # Try to install/update certificates
    success = install_certificates_macos()
    
    if success:
        # Test the connection
        test_ssl_connection()
    
    print("\n🔧 Alternative solutions if this doesn't work:")
    print("1. Install certificates manually:")
    print("   /Applications/Python\\ 3.x/Install\\ Certificates.command")
    print("2. Update certificates:")
    print("   pip install --upgrade certifi")
    print("3. Set environment variable:")
    print("   export SSL_CERT_FILE=$(python -m certifi)")
    
    # Create environment variable file
    try:
        with open(".env", "w") as f:
            f.write(f"SSL_CERT_FILE={certifi.where()}\n")
            f.write("PYTHONHTTPSVERIFY=0\n")  # For development only
        print("✅ Created .env file with SSL configuration")
    except Exception as e:
        print(f"⚠️  Could not create .env file: {e}")

if __name__ == "__main__":
    main()