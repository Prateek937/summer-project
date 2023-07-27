provider "aws" {
    region = "ap-south-1"
}

variable "name" {
  type = string
}

variable "nodecount" {
  type = number
}

resource "aws_instance" "hadoop" {
  count  = var.nodecount
  ami           = "ami-003b12a9a1ee83922"
  instance_type = "t3.micro"
  vpc_security_group_ids = ["sg-0d50e273cccb9bdce"]
  key_name = "hadoop"
  subnet_id = "subnet-0ed454b2be601fe92"
  tags = {
    Name = var.nodecount > 1 ? "${var.name}-${count.index + 1}" : var.name 
  }
  provisioner "remote-exec" {
    inline = ["echo 'connected!'"]
    connection {
      type     = "ssh"
      user     = "ec2-user"
      private_key = file("./playbooks/hadoop.pem") 
      host     = self.public_ip
  }
  }

}

resource "local_file" "inventory" {
  content  = <<-EOT
[namenode]
${try(aws_instance.hadoop.0.public_ip, "")}

[datanode]
${try(aws_instance.hadoop.1.public_ip, "")}
${try(aws_instance.hadoop.2.public_ip, "")}
${try(aws_instance.hadoop.3.public_ip, "")}
${try(aws_instance.hadoop.4.public_ip, "")}
${try(aws_instance.hadoop.5.public_ip, "")}
${try(aws_instance.hadoop.6.public_ip, "")}
${try(aws_instance.hadoop.7.public_ip, "")}
${try(aws_instance.hadoop.8.public_ip, "")}
${try(aws_instance.hadoop.9.public_ip, "")}
${try(aws_instance.hadoop.10.public_ip, "")}
${try(aws_instance.hadoop.11.public_ip, "")}
${try(aws_instance.hadoop.12.public_ip, "")}
${try(aws_instance.hadoop.13.public_ip, "")}

[all:vars]
ansible_user=ec2-user
  EOT
  filename = "./playbooks/inventory"
}

resource "null_resource" "hadoop_cluster" {
  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=./playbooks/ansible.cfg ansible-playbook -i ./playbooks/inventory --private-key ./playbooks/hadoop.pem ./playbooks/cluster.yml"
  }
  triggers = {always_run:"${timestamp()}"}
  depends_on = [local_file.inventory]
}