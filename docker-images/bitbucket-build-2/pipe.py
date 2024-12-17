from bitbucket_pipes_toolkit import Pipe
import subprocess

variables = {
    'IMAGE': {'type': 'string', 'required': True},
    'DOCKER_FILE': {'type': 'string', 'required': False, 'default':'Dockerfile'}
}

def execute_bash(command:str):
    subprocess.run(command, shell=True, check=True)

pipe = Pipe(schema=variables)
image = pipe.get_variable('IMAGE')
docker_file = pipe.get_variable('DOCKER_FILE')

pipe.log_info("Executing the pipe...")

pipe.log_info("building image...")
execute_bash(f"docker build -f {docker_file} -t {image} .")

pipe.log_info("saving image...")
execute_bash(f"docker save {image} > {image}.tar")

execute_bash(f"ls")

pipe.success(message=f"Success building {image}")