variable "instance_type" {
  description = "This describes the instance type"
  type = string
  
}
variable "ec2_Name" {
  description = "name of ec2 "
  type = string
}

variable "ami_id" {
    description = "This describes the ami image which Amazon Linux 2023 AMI"
    type = string
   
}
variable "public_subnet_ids" {
    
    type = list(string)
   
}

variable "ssh_port" {
  description = "SSH Port"
  type = number
  default = 22
  
}
variable "HTTP_port" {
  description = "HTTP Port"
  type = number
  default = 80
}

variable "vpc_id" {
  type = string
}


variable "key_Name" {
  description = "Name of private key use in aws to connect ec2 "
  type = string
}