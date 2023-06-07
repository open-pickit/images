from bitbucket_pipes_toolkit import Pipe
import subprocess

variables = {
    'AWS_ACCESS_KEY_ID': {'type': 'string', 'required': True},
    'AWS_SECRET_ACCESS_KEY': {'type': 'string', 'required': True},
    'IMAGE': {'type': 'string', 'required': True},
    'DOCKER_FILE': {'type': 'string', 'required': False, 'default':'Dockerfile'},
    'IMAGE_INIT': {'type': 'string', 'required': False, 'default':''},
    'DOCKER_FILE_INIT': {'type': 'string', 'required': False, 'default':''}
}

def execute_bash(command:str):
    build_command = command
    subprocess.run(build_command, shell=True, check=True)

pipe = Pipe(schema=variables)
aws_key = pipe.get_variable('AWS_ACCESS_KEY_ID')
aws_secret = pipe.get_variable('AWS_SECRET_ACCESS_KEY')
image = pipe.get_variable('IMAGE')
docker_file = pipe.get_variable('DOCKER_FILE')
image_init = pipe.get_variable('IMAGE_INIT')
docker_file_init = pipe.get_variable('DOCKER_FILE_INIT')

pipe.log_info("Executing the pipe...")

execute_bash(f"aws configure set aws_access_key_id {aws_key}")
execute_bash(f"aws configure set aws_secret_access_key {aws_secret}")
execute_bash(f"eval $(aws ecr get-login --no-include-email --region us-west-2 | sed 's;https://;;g')")
execute_bash(f"docker build -f {docker_file} -t {image} .")
execute_bash(f"docker push {image}")

if(image_init != '' and docker_file_init != ''):
    execute_bash(f"docker build -f {docker_file_init} -t {image_init} .")
    execute_bash(f"docker push {image_init}")

pipe.success(message="Success publishing image")