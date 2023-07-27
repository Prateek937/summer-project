provider "aws" {
    region = "ap-south-1"
}

variable "name" {
  type = string
}

variable "slavecount" {
  type = number
}

resource "aws_instance" "kubernetes" {
  count  = var.slavecount + 1
  ami           = "ami-072ec8f4ea4a6f2cf"
  instance_type = "t2.medium"
  vpc_security_group_ids = ["sg-0d50e273cccb9bdce"]
  key_name = "hadoop"
  subnet_id = "subnet-0ed454b2be601fe92"
  tags = {
    Name = var.slavecount > 1 ? "${var.name}-${count.index + 1}" : var.name 
  }
}

resource "local_file" "inventory" {
  content  = <<-EOT
[master]
${try(aws_instance.kubernetes.0.public_ip, "")}

[workers]
${try(aws_instance.kubernetes.1.public_ip, "")}
${try(aws_instance.kubernetes.2.public_ip, "")}
${try(aws_instance.kubernetes.3.public_ip, "")}
${try(aws_instance.kubernetes.4.public_ip, "")}
${try(aws_instance.kubernetes.5.public_ip, "")}
${try(aws_instance.kubernetes.6.public_ip, "")}
${try(aws_instance.kubernetes.7.public_ip, "")}
${try(aws_instance.kubernetes.8.public_ip, "")}
${try(aws_instance.kubernetes.9.public_ip, "")}
${try(aws_instance.kubernetes.10.public_ip, "")}
${try(aws_instance.kubernetes.11.public_ip, "")}
${try(aws_instance.kubernetes.12.public_ip, "")}
${try(aws_instance.kubernetes.13.public_ip, "")}

[all:vars]
ansible_user=ec2-user
  EOT
  filename = "./playbooks/inventory"
}

resource "null_resource" "kube_cluster" {
  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=./playbooks/ansible.cfg ansible-playbook -i ./playbooks/inventory --private-key ./playbooks/hadoop.pem ./playbooks/kube_cluster.yml"
  }
  triggers = {always_run:"${timestamp()}"}
  depends_on = [local_file.inventory]
}