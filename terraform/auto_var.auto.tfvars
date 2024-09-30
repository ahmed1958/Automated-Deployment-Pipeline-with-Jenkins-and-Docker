 # vpc 
  vpc_Name = "test-vpc"
  vpc_cidr_block = "10.0.0.0/16"
  public_subnets_cidr = ["10.0.1.0/24"]
  availability_Zones_subnet = ["eu-north-1a"]   # us-east-1a
#ec2
  ec2_Name = "test-ec2"
  ami_id = "ami-090abff6ae1141d7d"   # ami-0e86e20dae9224db8
  key_Name = "private_key"
  instance_type = "t3.micro"   # t2.micro