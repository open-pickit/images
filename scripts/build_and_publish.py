import subprocess

def build_and_push_image(image_name, dockerfile_path, repository, tag):
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