import pulumi
from pulumi_aws import ec2

# const stackConfig = new pulumi.Config();

# const bucketName = stackConfig.require("bhavya");

# // Create an S3 bucket
# const bucket = new aws.s3.Bucket("myBucket", {
#     bucket: bucketName,
# });

# export const bucketNameOutput = bucket.id;

# Create a security group for your EC2 instance
web_security_group = ec2.SecurityGroup("mypulumi",
    ingress=[{
        "protocol": "tcp",
        "fromPort": 22,  # SSH port
        "toPort": 22,
        "cidrBlocks": ["0.0.0.0/0"],
        "protocol": "tcp",
        "fromPort": 80,  # HTTP port
        "toPort": 80,
        "cidrBlocks": ["0.0.0.0/0"],
    }]
)

# Read the content of your custom index.html file
with open("index.html", "r") as index_file:
    custom_html_content = index_file.read()

# Create an EC2 instance with a new AWS Key Pair and user data script
web_instance = ec2.Instance("web-instance",
    instance_type="t2.micro",
    security_groups=[web_security_group.name],
    ami="ami-0fc5d935ebf8bc3bc",
    key_name="ssh",  # Specify the name of the key pair
    user_data=pulumi.Output.all(custom_html_content).apply(lambda content: f"""#!/bin/bash
sudo apt-get update
sudo apt-get install nginx
sudo chmod 777 /var/www/html/index.nginx-debian.html
echo '{content}' > /var/www/html/index.nginx-debian.html
sudo /etc/init.d/nginx start
"""),
)

# Output the public IP address of the EC2 instance
pulumi.export("ec2_public_ip", web_instance.public_ip)
