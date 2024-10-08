# Automated-Deployment-Pipeline-with-Jenkins-and-Docker

## Overview
This project demonstrates an end-to-end Continuous Integration/Continuous Deployment (CI/CD) pipeline using Jenkins, Docker, Ansible, and Terraform. The pipeline automates the process from code push to deployment, utilizing infrastructure as code (IAC) and containerization principles for consistent and automated deployments.

![Image](pipeline-image.png)


## Pipeline Steps Explanation

### Step 1: Infrastructure Setup with Terraform

Terraform is used to provision two EC2 instances in AWS:
- **Jenkins Agent EC2**: Hosts the Jenkins agent that runs the pipeline.
- **Ansible and Docker Agent EC2**: Used to deploy the application.

Terraform scripts define and manage the infrastructure-as-code, ensuring reproducibility and consistency in environment setups.




### Step 2: Code Push to GitHub

When the developer pushes code to the GitHub repository, a webhook is triggered, notifying Jenkins of the update. This initiates the pipeline process automatically.



### Step 3: Dockerization of the Application

Upon receiving the webhook, Jenkins:
1. **Clones the repository**: Jenkins pulls the latest code from GitHub.
2. **Dockerizes the application**: Jenkins uses a `Dockerfile` to package the application into a Docker image.



### Step 4: Unit Testing

Jenkins runs unit tests to ensure that the new code does not break the application. If the unit tests pass, the deployment process proceeds. If they fail, Jenkins stops the process and notifies the team via email or Slack. After the image is tested, it is pushed to a Docker Hub repository for storage and future deployments.



### Step 5: Deployment with Ansible and Docker

- **Docker Compose Template Update**: Ansible updates the Docker Compose file template, injecting the new Docker image name.
- **Deployment**: 
   - If there are changes in the image or configuration, Ansible runs `docker-compose up` on the Ansible-and-Docker EC2 instance.
   - This deploys the latest version of the application.



### Step 6: Notifications

Throughout the pipeline, Jenkins is configured to send notifications about the pipeline status (successful build, failed tests, deployment status) via email.




---

 ## Prerequisites
Ensure you have the following prerequisites set up before running the pipeline:

1. Infrastructure
    - AWS Account
    - Two EC2 Instances:
        - Jenkins Agent EC2: Where Jenkins will run.
        - Ansible and Docker Agent EC2: For application deployment.
    - Security Groups: Ensure SSH (port 22) and HTTP/HTTPS (port 80/443) are open for server access.
2. Tools Installed
    - Jenkins: Installed on the Jenkins Agent EC2 instance.
    - Terraform: Installed on your local machine or build server.
    - Docker: Installed on both EC2 instances.
    - Ansible: Installed on the Ansible and Docker Agent EC2 instance.
3. GitHub Repository
    - Code Repository: Application code with a Dockerfile and unit tests.
    - Webhook Setup: GitHub webhook to trigger Jenkins builds.
4. Docker Hub Account
Docker Hub Repository: For storing Docker images created during the pipeline.
Jenkins Plugins

### Install the following plugins in Jenkins to enable the full CI/CD pipeline:

- Git Plugin: Allows Jenkins to pull code from GitHub.
- Docker Pipeline Plugin: Provides support for Docker operations in Jenkins Pipeline.
- Ansible Plugin: Runs Ansible playbooks for automated deployments.
- Mailer Plugin: Sends custom email notifications for build and deployment statuses.


## Screenshots
<div text-align="center">
The app before update with removing "Team leader" sentence

![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.02.57.jpeg)

Start building:
![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.00%20(2).jpeg)
![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.01.jpeg)
![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.01%20(1).jpeg)
![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.02.jpeg)
![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.02%20(1).jpeg)
![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.03.jpeg)
![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.04.jpeg)

The App After update:

![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.00%20(1).jpeg)

Email Sending: 

![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.04%20(2).jpeg)

Pipeline Configration:

![App Screenshot](./Screenshots/WhatsApp%20Image%202024-10-08%20at%2023.00.04%20(1).jpeg)


</div>



