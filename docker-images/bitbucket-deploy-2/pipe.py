from bitbucket_pipes_toolkit import Pipe
import subprocess

variables = {
    'AWS_ACCESS_KEY_ID': {'type': 'string', 'required': True},
    'AWS_SECRET_ACCESS_KEY': {'type': 'string', 'required': True},
    'IMAGE': {'type': 'string', 'required': True},
    'DEPLOY_NAME': {'type': 'string', 'required': True},
    'NAMESPACE': {'type': 'string', 'required': True},
}

def execute_bash(command:str):
    subprocess.run(command, shell=True, check=True)

pipe = Pipe(schema=variables)
aws_key = pipe.get_variable('AWS_ACCESS_KEY_ID')
aws_secret = pipe.get_variable('AWS_SECRET_ACCESS_KEY')
image = pipe.get_variable('IMAGE')
deploy_name = pipe.get_variable('DEPLOY_NAME')
namespace = pipe.get_variable('NAMESPACE')

pipe.log_info("Executing the pipe...")

pipe.log_info("log into ecr...")
execute_bash(f"aws configure set aws_access_key_id {aws_key}")
execute_bash(f"aws configure set aws_secret_access_key {aws_secret}")
execute_bash("aws eks update-kubeconfig --name eks-cluster --region us-west-2")

pipe.log_info("loading images...")
execute_bash(f"docker load < ms.tar")

pipe.log_info("tagging images...")
execute_bash(f"docker tag ms:latest {image}")

pipe.log_info("uploading images...")
execute_bash(f"docker push {image}")

pipe.log_info("deploying...")
execute_bash(f"kubectl rollout restart deployment {deploy_name} -n {namespace}")
execute_bash(f"kubectl rollout status deploy/{deploy_name} -n {namespace}")

pipe.success(message=f"Success deploying {deploy_name}")