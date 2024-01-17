# parse yaml file
import requests
import yaml
import time
from urllib.parse import urlparse

def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def send_requests(endpoints):
        availability = {}
        for endpoint in endpoints:
            try:
                if 'url' in endpoint:
                    url = endpoint['url']
                    domain = urlparse(url).netloc
                    method = endpoint.get('method', 'GET')
                    headers = endpoint.get('headers', {})
                    body = endpoint.get('body', None)
                    name = endpoint.get('name')

                    print(f"Sending {method} request to {url}")

                    start_time = time.time()

                    if method == 'GET':
                        response = requests.get(url, headers=headers, json=body)
                    elif method == 'POST':
                        response = requests.post(url, headers=headers, json=body)

                    end_time = time.time()

                    latency = (end_time - start_time) * 1000  # Convert to milliseconds

                    if 200 <= response.status_code < 300 and latency < 500:
                        availability[domain] = availability.get(domain, {'up': 0, 'total': 0})
                        availability[domain]['up'] += 1
                    else:
                        availability[domain] = availability.get(domain, {'up': 0, 'total': 0})

                    availability[domain]['total']+=1
            except Exception as e:
                print(f"Error occurred: {str(e)}")
        return availability
        

if __name__ == "__main__":
    file_path = 'prompt.yaml'  # Replace with the path to your YAML file
    endpoints = read_yaml_file(file_path)
    if endpoints:
        while 1:
         try:
            availability = send_requests(endpoints)
            for domain, status in availability.items():
                availability_percentage = 100 * (status['up'] / status['total']) if status['total'] > 0 else 0
                print(f"\n{domain} has {int(availability_percentage)}% availability percentage")
            time.sleep(15)
            print('\nNew cycle:')
         except KeyboardInterrupt:
            print('\nProgram terminated\n')
            break
    else:
        print("No endpoints.")
# send requests every 15 seconds
# log the result
# end the program and print the availaibility percentage 