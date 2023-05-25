import os
import subprocess

def check_required_env_variables():
    # Check if the required environment variables are set
    required_variables = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]

    for variable in required_variables:
        if not os.environ.get(variable):
            raise EnvironmentError(f"Environment variable {variable} is not set.")

def login_to_docker():
    # Login to Docker Hub or another container registry
    login_command = f"docker login --username {os.environ['DOCKER_USERNAME']} --password {os.environ['DOCKER_PASSWORD']}"
    subprocess.run(login_command, shell=True, check=True)
    print("successfuly logged")

def build_and_push_image(image_name, dockerfile_path, repository, tag):
    # Check if the required environment variables are set
    check_required_env_variables()

    # Login to Docker Hub or another container registry
    login_to_docker()

    # Build the Docker image
    build_command = f"docker build -t {image_name} -f {dockerfile_path} ."
    subprocess.run(build_command, shell=True, check=True)

    # Push the Docker image to a repository
    push_command = f"docker tag {image_name} {repository}:{tag} && docker push {repository}:{tag}"
    subprocess.run(push_command, shell=True, check=True)

# Example usage
image_name = "cli-aws-kubectl"
dockerfile_path = "docker-images/cli-aws-kubectl/Dockerfile"
repository = "pickittechnology"
tag = "latest"

build_and_push_image(image_name, dockerfile_path, repository, tag)