import requests
import os
import subprocess
from pypac import PACSession
from io import StringIO

### Rancher API access variables 

url = "https://console.k8s.tech.orange/v3/clusters/c-m-tjbs2xnn?action=generateKubeconfig"
rancher_api_key = os.getenv("RANCHER_API_KEY") # Bearer token stored in 'RANCKER_API_KEY' env - adjust to your config
session = PACSession(pac_file_url='http://proxy.tepenet/opl.pac') # OPL Proxy PAC - can be ignored if proxy is not required
headers = {
  'Authorization': f'Bearer {rancher_api_key}',
}
response = session.post(url, headers=headers)
# response = requests.post(url, headers=headers) # Used when proxy is not required

### Kubeconfig file variables

kubeconfig_content = response.json()['config']
kubeconfig_path = os.getenv("KUBECONFIG") # Path to kubeconfig stored in the env
intraorange_proxy_url = "    proxy-url: http://proxygroup.itn.intraorange:8080\n" # Include new line, 4 spaces before proxy !!!
parsed_kubeconfig = StringIO(kubeconfig_content)
lines = parsed_kubeconfig.readlines()
lines.insert(5, intraorange_proxy_url) # Include the proxy url in the kubeconfig, it is set in the line 6
kubeconfig_with_proxy = "".join(lines) # Combine lines to string

### Debug

# print (lines)
# print (kubeconfig_with_proxy)

### Save content to kubeconfig file

with open (kubeconfig_path, "w") as f:
    f.write(kubeconfig_with_proxy)

### Verify access with kubectl

verify_access = subprocess.run("kubectl cluster-info", shell=True, capture_output=True, text=True)
print (verify_access)
