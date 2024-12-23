import subprocess
import os

images_base_dir = 'docker-images'


def set_docker_engine():
    build_command = f"docker buildx create --use --driver=docker-container"
    subprocess.run(build_command, shell=True, check=True)


def build_and_push_image(image_name, tag):
    dockerfile_path = os.path.join(images_base_dir, image_name)
    repository = "pickittechnology"

    # Build the Docker image
    build_command = f"docker buildx build --cache-from \"type=local,src=./cache\" --cache-to \"type=local,dest=./cache\" -t {repository}/{image_name}:{tag} --push {dockerfile_path}"
    subprocess.run(build_command, shell=True, check=True)


# Example usage
tag = "latest"

set_docker_engine()

images_dirs = [d for d in os.listdir(images_base_dir) if os.path.isdir(os.path.join(images_base_dir, d))]

for image in images_dirs:
    
    if (image == 'bitbucket-build-2'):
        tag = '2.0.1'
    else:
        tag = 'latest'
    
    build_and_push_image(image, tag)
