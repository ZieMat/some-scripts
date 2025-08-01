'''
Script that can be used to simplify the image update process on the local env.
Usage: python ./image_update.py {version}
'''

import subprocess
import argparse

def parse_version():
    # with open("versions.txt", "r") as file:
    #     # Read lines and strip whitespace, filter out empty lines
    #     choices = [line.strip() for line in file.readlines() if line.strip()]
    parser = argparse.ArgumentParser(description='Build Docker image and rollout K8s deployment with this updated image')
    parser.add_argument('version', type=str, choices=choices,
                       help='Version to deploy (playground, test_scripts, or main)')
    return parser.parse_args()

def main():
    args = parse_version()
    version = args.version

    # Kubectl variables
    deployment_file_path = f"k8s/{version}/deployment.yml"
    kubectl_rollout = f"kubectl rollout restart -f {deployment_file_path}"

    # Docker variables
    dockerfile = f".\{version}.Dockerfile"
    docker_tag = f"registry.gitlab.tech.orange/diod/secgov/dt-self-onboarding-portal:{version}"
    docker_build = f"docker build -t {docker_tag} -f {dockerfile} ."
    docker_push = f"docker push {docker_tag}"


    '''
    Execution order:
    1. docker build 
    2. docker push
    3. kubectl rollout
    '''

    commands = [
        # f"{kubectl_delete}",
        docker_build,
        docker_push,
        kubectl_rollout
        # f"{kubectl_apply}"
    ]

    for command in commands:
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True)

        if result.returncode == 0:
            print (f"{command} proceed succesfully")
            print ("Output:", result.stdout)
        else:
            print (f"{command} failed")
            print ("Error", result.stderr)
            
            
            if not command.startswith('kubectl delete'):
                print(f"Command {command} failed")
                break
            else:
                print("Deployment not present in the cluster - Skipping")
                continue
            
    print("Image rebuild and pod redeployed succesfully")     

if __name__ == '__main__':
    main()