from bitbucket_pipes_toolkit import Pipe
import subprocess

variables = {
    'AWS_ACCESS_KEY_ID': {'type': 'string', 'required': True},
    'AWS_SECRET_ACCESS_KEY': {'type': 'string', 'required': True},
    'IMAGE': {'type': 'string', 'required': True},
    'DOCKER_FILE': {'type': 'string', 'required': False, 'default':'Dockerfile'}
}

def execute_bash(command:str):
    subprocess.run(command, shell=True, check=True)

pipe = Pipe(schema=variables)
aws_key = pipe.get_variable('AWS_ACCESS_KEY_ID')
aws_secret = pipe.get_variable('AWS_SECRET_ACCESS_KEY')
image = pipe.get_variable('IMAGE')
docker_file = pipe.get_variable('DOCKER_FILE')

pipe.log_info("Executing the pipe...")

pipe.log_info("log into docker...")
execute_bash(f"aws configure set aws_access_key_id {aws_key}")
execute_bash(f"aws configure set aws_secret_access_key {aws_secret}")
execute_bash(f"eval $(aws ecr get-login --no-include-email --region us-west-2 | sed 's;https://;;g')")

pipe.log_info("building image...")
execute_bash(f"docker build -f {docker_file} -t {image} .")

pipe.log_info("saving image...")
execute_bash(f"docker save {image} > {image}.tar")

execute_bash(f"ls")

pipe.success(message=f"Success building {image}")