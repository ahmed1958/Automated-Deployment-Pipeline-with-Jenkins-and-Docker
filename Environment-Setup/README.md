# Environment Setup
This environment setup leverages Terraform for provisioning AWS infrastructure and Ansible for configuring Docker and Jenkins on EC2 instances. The setup includes creating two public subnets, one for a Docker agent and another for a Jenkins agent. This section of the repository is focused on setting up the infrastructure required for an automated deployment pipeline.

## Overview
This project automates the deployment of two EC2 instances in AWS, each running a different service:
  - Docker Agent: Installed on one EC2 instance to run Docker.
  - Jenkins Agent: Installed on a separate EC2 instance to run Jenkins.
Terraform is used to provision the necessary AWS infrastructure, including EC2 instances, security groups, and key pairs. Ansible is used to install and configure Docker and Jenkins on the respective EC2 instances.

## Prerequisites
Before running this setup, ensure the following tools are installed:
   - Terraform (version 0.12 or above)
   - Ansible (version 2.9 or above)
   - AWS CLI (for managing AWS resources)
   - SSH Access (for connecting to the EC2 instances)
You should also have an AWS account configured with appropriate permissions to create EC2 instances, security groups, and VPCs.

## Infrastructure Setup
### Terraform Configuration
The infrastructure is defined using Terraform scripts, which include:
  - AWS VPC: A Virtual Private Cloud with two public subnets.
  - EC2 Instances: Two EC2 instances, one for the Docker agent and one for the Jenkins agent.
  - Security Groups: A security group allowing SSH, HTTP, and Jenkins port access.
  - Key Pair: An RSA private key is generated and used for EC2 access.
### Key components of the Terraform configuration:
  - Public EC2 Instances: The instances are created with public IPs and are assigned to the public subnets.
  - Provisioner: A local provisioner is used to dynamically update an inventory file for Ansible after the EC2 instances are created.
### Variables
Key values used in the Terraform configuration:
#### VPC Configuration:
  - VPC Name: test-vpc
  - VPC CIDR Block: 10.0.0.0/16
  - Public Subnets CIDR: ["10.0.1.0/24", "10.0.2.0/24"]
  - Availability Zones: ["us-east-1a", "us-east-1b"]
#### EC2 Configuration:
  - Instance Names: ["docker-agent", "jenkins-agent"]
  - AMI ID: ami-0e86e20dae9224db8
  - Key Name: private_key
  - Instance Type: t2.micro

## Configuration Setup
### Ansible Playbooks
Once the EC2 instances are provisioned, Ansible is used to configure them.

#### Docker Agent Configuration
The docker-agent EC2 instance is configured with Docker. The following tasks are executed:
  - Update the apt cache and install necessary prerequisites.
  - Add the official Docker GPG key and repository.
  - Install Docker and ensure the service is running.
#### Jenkins Agent Configuration
The jenkins-agent EC2 instance is configured with Jenkins. The tasks include:
  - Install Java, a prerequisite for Jenkins.
  - Add the Jenkins GPG key and repository.
  - Install Jenkins and start the service.
  - Configure the firewall to allow traffic on port 8080 (Jenkins' default port).
## Running the Setup
Follow these steps to run the environment setup:

### Step 1: Clone the Repository
```sh
git clone <repository-url>
cd Environment-setup
```
### Step 2: Initialize and Apply Terraform
Ensure that your AWS credentials are set up, and then run the following Terraform commands:
```sh
cd terraform
terraform init
terraform apply
```
This will provision the infrastructure, including EC2 instances, security groups, and key pairs.

### Step 3: Run Ansible Playbooks
After Terraform completes, the dynamic inventory file will be updated with the IP addresses of the EC2 instances. Run the following Ansible playbook to configure the instances:
```sh
ansible-playbook  setup_project.yml
```
