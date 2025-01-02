from bitbucket_pipes_toolkit import Pipe
import subprocess
import os, json

variables = {
    'AWS_ACCESS_KEY_ID': {'type': 'string', 'required': True},
    'AWS_SECRET_ACCESS_KEY': {'type': 'string', 'required': True},
    'ENV': {'type': 'string', 'required': True},
}

def execute_bash(command:str):
    subprocess.run(command, shell=True, check=True)

def get_registry():
    result = subprocess.run("aws sts get-caller-identity --query 'Account' --output text", shell=True, capture_output=True, text=True)
    return f"{result.stdout.strip()}.dkr.ecr.us-west-2.amazonaws.com"

def find_docker_files():
    # List to store found files
    docker_files = []
    
    # Walk through the root directory
    for root, _, files in os.walk("."):
        for file in files:
            if file in ["Dockerfile", "Dockerfile.init"] and root == ".":
                docker_files.append(file)
    
    # Iterate over the list and print filenames
    pipe.log_info("Docker Files found:")
    for file in docker_files:
        pipe.log_info(file)
    
    return docker_files

def get_data_from_package_json():
    package_json_path = os.path.join(os.getcwd(), "package.json")
    
    if not os.path.exists(package_json_path):
        raise FileNotFoundError("package.json file not found at root directory.")
    
    with open(package_json_path, "r") as file:
        package_data = json.load(file)
    
    name = package_data.get("name")
    version = package_data.get("version")

    if name is None:
        raise KeyError("The 'name' key is missing in package.json.")
    if version is None:
        raise KeyError("The 'version' key is missing in package.json.")
    
    print(f"detected name: {name}")
    print(f"detected version: {version}")

    parts = name.split('-', 1)
    if len(parts) != 2:
        raise ValueError("Input string format is invalid.")
    
    first_word = parts[0]
    rest_of_string = parts[1]
    valid_words = {"pickers", "pickit"}
    if first_word not in valid_words:
        raise ValueError(f"Invalid first word: '{first_word}'. Must be one of {valid_words}.")
    
    return first_word, rest_of_string, version

def get_image_name(env: str, img: str, latest: bool = False):
    namespace, project_name, version = get_data_from_package_json()

    if(latest):
        version = 'latest'

    if(img == "Dockerfile.init"):
        return f"{namespace}-{env}-{project_name}-init:{version}" 
    else:
        return f"{namespace}-{env}-{project_name}:{version}" 

pipe = Pipe(schema=variables)
aws_key = pipe.get_variable('AWS_ACCESS_KEY_ID')
aws_secret = pipe.get_variable('AWS_SECRET_ACCESS_KEY')

pipe.log_info("Executing the pipe...")

pipe.log_info("log into ecr...")
execute_bash(f"aws configure set aws_access_key_id {aws_key}")
execute_bash(f"aws configure set aws_secret_access_key {aws_secret}")
execute_bash(f"eval $(aws ecr get-login --no-include-email --region us-west-2 | sed 's;https://;;g')")
execute_bash("aws eks update-kubeconfig --name eks-cluster --region us-west-2")
registry = get_registry()

images = find_docker_files()
for img in images:
    image = get_image_name(pipe.get_variable('ENV'), img)
    new_image = get_image_name(pipe.get_variable('ENV'), img, True)
    pipe.log_info(f"detected image: {image}")
    pipe.log_info(f"new image: {new_image}")

    pipe.log_info("tagging images...")
    execute_bash(f"docker buildx imagetools create {registry}/{image} --tag {registry}/{new_image}")

pipe.log_info("deploying...")
namespace, project_name, version = get_data_from_package_json()

if(namespace == 'pickers'):
    pipe.log_warning('rename \'ms\' namespace to \'pickers\'')
    namespace = 'ms'
pipe.log_info(f"namespace: {namespace}")

deploy_name = f"{namespace}-{project_name}"
pipe.log_info(f"deploy_name: {deploy_name}")

execute_bash(f"kubectl rollout restart deployment {deploy_name} -n {namespace}")
execute_bash(f"kubectl rollout status deploy/{deploy_name} -n {namespace}")

pipe.success(message=f"Success deploying {deploy_name}.{namespace}")