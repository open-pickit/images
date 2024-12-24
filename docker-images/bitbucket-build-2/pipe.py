from bitbucket_pipes_toolkit import Pipe
import subprocess
import os, json

variables = {
    'AWS_ACCESS_KEY_ID': {'type': 'string', 'required': True},
    'AWS_SECRET_ACCESS_KEY': {'type': 'string', 'required': True},
    'ENV': {'type': 'string', 'required': True},
    'NPMRC_FILE': {'type': 'string', 'required': True}
}

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
    
    return name, version

def get_image_name(env: str, img: str):
    name, version = get_data_from_package_json()

    parts = name.split('-', 1)
    if len(parts) != 2:
        raise ValueError("Input string format is invalid.")
    
    first_word = parts[0]
    rest_of_string = parts[1]
    valid_words = {"pickers", "pickit"}
    if first_word not in valid_words:
        raise ValueError(f"Invalid first word: '{first_word}'. Must be one of {valid_words}.")
    
    if(img == "Dockerfile.init"):
        return f"{first_word}-{env}-{rest_of_string}-init:{version}" 
    else:
        return f"{first_word}-{env}-{rest_of_string}:{version}" 


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

pipe = Pipe(schema=variables)

aws_key = pipe.get_variable('AWS_ACCESS_KEY_ID')
aws_secret = pipe.get_variable('AWS_SECRET_ACCESS_KEY')
npmrc = pipe.get_variable('NPMRC_FILE')

pipe.log_info("Executing the pipe...")

pipe.log_info("log into ecr...")
execute_bash(f"aws configure set aws_access_key_id {aws_key}")
execute_bash(f"aws configure set aws_secret_access_key {aws_secret}")
execute_bash(f"eval $(aws ecr get-login --no-include-email --region us-west-2 | sed 's;https://;;g')")

registry = get_registry()
pipe.log_info(f"registry: {registry}")

pipe.log_info("Creating npmrc...") 
execute_bash(f"echo {npmrc} | base64 -d > .npmrc")

images = find_docker_files()
for img in images:
    image = get_image_name(pipe.get_variable('ENV'))
    pipe.log_info(f"detected image: {image}")

    pipe.log_info("building image...")
    execute_bash(f"docker build -f Dockerfile -t {registry}/{image} .")

    pipe.log_info("publishing...")
    execute_bash(f"docker push {registry}/{image}")

pipe.success(message=f"Success publishing {image}")