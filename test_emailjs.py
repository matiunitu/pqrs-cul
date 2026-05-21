import urllib.request
import json
import sys

def test_emailjs():
    url = 'https://api.emailjs.com/api/v1.0/email/send'
    payload = {
        'service_id': 'service_25libn5',
        'template_id': 'template_tu878js',
        'user_id': 'o3tsRNH8slV7K4jTP',
        'template_params': {
            'name': 'Test User',
            'title': 'Test Radicado RAD-12345',
            'email': 'test@example.com'
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            print(f"Status: {response.status}")
            print(f"Response: {body}")
            if response.status == 200:
                print("EmailJS is working correctly!")
            else:
                print("EmailJS is NOT working correctly. Returned non-200 status.")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        print(f"Response: {e.read().decode('utf-8')}")
        print("EmailJS is NOT working correctly.")
    except Exception as e:
        print(f"Error: {e}")
        print("EmailJS is NOT working correctly.")

if __name__ == "__main__":
    test_emailjs()
