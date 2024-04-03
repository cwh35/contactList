# Unveiling the Magic of Web App Deployments

## Introduction
The first big project I completed as a CS major in college was a Flask application. At the time, I had no idea how the complicated magic of deployment works. Years later, I perform that magic as a DevOps engineer, and I figured I'd pull away the curtain for those who are still in school or working on personal projects of their own that they would like to cast out into the world. Specifically, this started as me writing up some instructions for a friend, but I figure it might be useful to someone else out there, too.

In this post, I will walk through the process of deploying a Flask application, detailing specific steps and instructions I use myself. [Here](https://github.com/katrinajaneczko/contactList) is the example repository that I am using to deploy. First, I'll walk through containerizing the backend and frontend separately using Docker and AWS EC2. Then, we will deploy it altogether. Next, I'll show you how to automate this process when you make changes to your GitHub repository, using GitHub Actions. And this is how I hope you'll amaze yourself with the magic of CI/CD, and be inspired to incorporate these ideas into your future projects.

While there are many other ways to go about this, I try to balance simplicity/ease with free/low cost, and to me this seems like the way to go if it's your first introduction to site deployment. However, keep in mind that the more you learn, the more solutions/options you'll realize exist, and you may decide to use different tools and services to suit your needs.

## Containerization

### What Is It?
One thing I was quick to understand as a new software engineer is that containerization is a crucial aspect of software deployment. Containers offer a lightweight, portable, and self-sufficient solution to package applications along with all their dependencies. This is cool because it enables consistent deployments across different environments. So basically, whether it's in Python or C or React, it does not matter what app you are deploying or what environment and requirements it needs--as long as we can containerize it, we can deploy it however we want. 

### Introducing Docker
Docker is a leading containerization platform that allows you to develop, ship, and run applications inside containers. This is what we will be using to containerize our app. This all starts with adding a `Dockerfile` to your repository. This Dockerfile is basically a blueprint that specifies how to build the container image. It specifies the base image to start from, any additional dependencies or configurations needed, and the commands to run within the container when it's launched. You're basically telling Docker instructions: "Hey, I'm running some Python code, so give me a Python runtime parent image. Now copy over all the code from my repository into the image, and make sure to install any requirements I'll need to run that code. Then run it." Easy-peasy. And don't worry too much about how to write a Dockerfile; you can find examples online easily and just copy them and modify them to suit your specific needs. 
 
### Install Docker
Before we begin, you'll need to have [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or [Rancher Desktop](https://rancherdesktop.io/) installed on your local machine, which will allow us to interface with Docker containers. Please double check you are installing the correct version for your operating system and architecture! Fair warning that I am using a Mac with an M2 chip, so while I'll be providing specific commands that should theoretically work across different OSs, you may need to do some extra Googling if it something work on your Windows computer (sorry!). 

## Running Your App Locally (Backend)
Yes I know I said we were going to deploy this thing, but I also said I'd go into extruciating detail in hopes that you'll actually understand what's going on. So bear with me here.

### Dockerizing Backend
Once you have Docker Desktop installed, you can open it up to start the Docker daemon. Then go ahead and navigate
to the directory in which your app resides. In the case of our example repository, and since I said earlier that we will start with the backend, it is `/contactList/backend`. Take a peek at the Dockerfile just to see what that looks like. Be curious.

#### Commands
You can run the following commands from the directory:
Build: `docker build -t backend .`
Run: `docker run --name backend -p 8081:8081 -d backend`
See: Visit http://localhost:8081/contacts
Stop: `docker stop backend`

## Pushing to DockerHub (Backend)
Nice, you have your app running locally with Docker. But that's no that impressive... yet. Do you remember why Docker was so cool? Because it allows us to containerize our app and deploy it anywhere. So, our next step will be to push it to a repository so that we can deploy it to a cloud service. 

DockerHub is a cloud-based registry service that allows you to store and manage your container images. You could also choose
to use other services like AWS ECR, Google Container Registry, or Azure Container Registry. If you want to use DockerHub (which is what I'll walk you through), you will need to create an account [here](https://hub.docker.com/), and take note of your username and password.

#### Commands 
Once you have your account set up, you can push your image to DockerHub by following these steps:
Tag image: `docker tag backend <dockerhub_username>/backend:latest`
Log in to DockerHub: `docker login`
Push image: `docker push <dockerhub_username>/backend:latest`

## Running on AWS EC2
Amazon Elastic Compute Cloud (EC2) is a web service offered AWS that provides resizable compute capacity in the cloud. With EC2, users can easily launch virtual servers, AKA instances. It's basically like renting a computer in the cloud, inside which you will run your app. But how will that allow my mom who lives over in New Hampshire to be able to look at my awesome web app? Well, when deploying a web app on EC2, each instance is assigned a unique IP address that can be used to access the app over the internet. You'll be able to give this address to your mom, so she can copy/paste this into her browser and see what you have hosted there. Although this is outside the scope of this post, it's worth mentioning that you can also attach a domain name to make accessing your web app even more convenient... but we'll go into that another time.

### Make an AWS Account
Firstly, you'll need an AWS account. Sign up for an [AWS Free Tier](https://aws.amazon.com/free) account. You can follow instructions on the site to set up budgets (to not allow charges over $0.01, for example), as well as a ton of interesting tutorials for learning about services they offer. But don't get too distracted--we're on a mission to deploy this web app, remember?

### Launch an EC2 Instance
Anyway, now let's launch the virtual server. You can follow [AWS's quickstart instructions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-instance-wizard.html#liw-quickly-launch-instance) to do so. Remember to always choose "Free Tier Eligible" or else you'll be charged money for however long you have it running. Careful with this cause one time I accidentally incurred a $42 charge when messing around with deploying a Discord bot and... well never mind, just don't make the same mistake. 

Here is how I configured mine:

Name: I called it `test-server`.

Amazon Machine Image (AMI): I chose `Amazon Linux 2023 AMI`. This is Free Tier Eligible.

Architecture: `64-bit (Arm)`. But remember I have an M2 chip Mac (ARM64 architecture), and since I'm building the image locally, I'll want it to run on ARM64 in the virtual server, too. But if you used a Windows computer to build the Docker image, you should choose `64-bit (x86)` here instead.

Key pair (login): Create new key pair. For the key pair name, I called it `test-server-key`, and I chose `ED25519` for the type and `.pem` for the file format. You will need the .pem private SSH key later, so just make sure you save this locally somewhere you'll rememember. 

Network Settings: You'll need to configure Security Groups to open required ports. Click on “Edit” next to the “Network Settings” submenu and fill in the following details: 
* Auto-assign public IP: `Disable`
* Firewall (security groups): `Create security group`
* Security group name: `testserver-sg`
Next, you'll add rules to open required ports and allow connections from anywhere (again, so your mom is allowed to view your app. She really really wants to see it, so make sure you do this right). Under "Inbound Security Group Rules", add 4 rules:
* SSH – TCP - Port 22 - Anywhere
* HTTP – TCP - Port 80 - Anywhere
* HTTPS – TCP - Port 443 - Anywhere
* Custom – TCP - Port 8081 - Anywhere

Configure Storage: I didn't touch this for now.

Advanced details: Also didn't touch this.

Number of instances: `1`.

#### Static IP Assignment
Go ahead and launch that bad boy and take a look at the Instance summary. You should see `Public IPv4 DNS` has a blank value. Oh no! How is your mom going to see your site? Don't panic, we still have to allocate a static IP, for which AWS has the AWS Elastic IP address feature, which you can [read aout here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html?icmpid=docs_ec2_console#using-instance-addressing-eips-allocating). 

Why are we doing this? Well, if we had left the auto-assign public IP option enabled, AWS would assign a public IP address to the EC2 instance for us, but it would automatically change every time you stop and start the instance. When you use EC2 to host a website, you want to use a static IP so your website will always be available at the same address.

For my fellow penny pinchers, keep in mind that if you use an Elastic IP address, you won't not be charged separately, but if you reserve an IP address and do not use it, then you will be charged. Also, if you terminate your EC2 instance, the assigned Elastic IP will not be deleted automatically. You would need to go back to Elastic IP dashboard and manually release the IP address.

Follow the directions [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html#using-instance-addressing-eips-allocating) to allocate an Elastic IP address, and [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html#using-instance-addressing-eips-associating) to associate it with your instance.

Great, now you can see a value for Public IPv4 DNS that looks something like `ec2-11-111-111-111.compute-1.amazonaws.com`, and the Elastic IP address that you set. You'll need those later. It'll be what you text your mom so she can visit your website once you've finished deploying it.

### Connect to & Configure the EC2 Instance
Now you need to actually put your code on the instance. You have a couple options here. One is that from your terminal, you can run `ssh -i test-server-key.pem ec2-user@<public-IP>`. Or, you can opt for what I did, which is doing it through the AWS console. From the Instance summary page, I clicked on the "Connect" button to get instruction. I chose "EC2 Instance Connect" and "Connect using EC2 Instance Connect". 

Once in, we need to install Docker on the virtual server. Follow [these instructions](https://www.cyberciti.biz/faq/how-to-install-docker-on-amazon-linux-2/); they're better than if I tried to explain it myself. 

#### Commands
Now we can pull and run the Docker image from DockerHub.
Pull: `docker pull <dockerhub_username>/backend:latest`
Run: `docker run -d --name backend -p 80:8081 <dockerhub_username>/backend`
Test: `curl localhost:80/contacts` (should output info)

Okay I lied a little bit. You are not going to be able to see your app just yet. You need ONE more thing: the help of Nginx.

When you run a Docker container, it creates its own isolated environment with its own network stack. Each container typically gets its own IP address within this isolated network.

However, by default, Docker containers are not directly accessible from outside the host machine. This means that even though your Flask application might be running inside a Docker container and listening on a certain port, external clients (such as users' web browsers) cannot directly communicate with the Flask app using the container's IP address.





