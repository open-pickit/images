import subprocess


def build_and_push_image(image_name, dockerfile_path, repository, tag):
    # Set Docker engine
    build_command = f"docker buildx create --use --driver=docker-container"
    subprocess.run(build_command, shell=True, check=True)

    # Build the Docker image
    build_command = f"docker buildx build --cache-from \"type=local,src=./cache\" --cache-to \"type=local,dest=./cache\" -t {repository}/{image_name}:{tag} -f {dockerfile_path} --push ."
    subprocess.run(build_command, shell=True, check=True)


# Example usage
image_name = "cli-aws-kubectl"
dockerfile_path = "docker-images/cli-aws-kubectl/Dockerfile"
repository = "pickittechnology"
tag = "latest"

build_and_push_image(image_name, dockerfile_path, repository, tag)
