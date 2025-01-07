import subprocess
import os

images_base_dir = 'docker-images'


def set_docker_engine():
    build_command = f"docker buildx create --use --driver=docker-container"
    subprocess.run(build_command, shell=True, check=True)

def read_version_file(file_path):
    try:
        with open(f"{file_path}/VERSION", 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file: {e}")

def build_and_push_image(image_name):
    dockerfile_path = os.path.join(images_base_dir, image_name)
    repository = "pickittechnology"
    tag = read_version_file(dockerfile_path)

    # Build the Docker image
    build_command = f"docker buildx build --cache-from \"type=local,src=./cache\" --cache-to \"type=local,dest=./cache\" -t {repository}/{image_name}:{tag} --push {dockerfile_path}"
    subprocess.run(build_command, shell=True, check=True)

# Example usage
set_docker_engine()

images_dirs = [d for d in os.listdir(images_base_dir) if os.path.isdir(os.path.join(images_base_dir, d))]

for image in images_dirs:
    build_and_push_image(image)
