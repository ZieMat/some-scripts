import argparse
from python_on_whales import docker 

def arguments():
    parser = argparse.ArgumentParser(description="Update the Docker image and restart K8S deployment")
    parser.add_argument("--image", "-i", help="Dockerfile path", default=".")
    args = parser.parse_args()
    return args

def main():
    args = arguments()
    dockerfile = args.image
    # with open (dockerfile, "r") as f:
    #     content = f.read()
        
    # print(content)
    image = docker.build(context_path=dockerfile, tags="test")
    # output = docker.run("hello-world")
    print(image)

if __name__ == "__main__":
    main()