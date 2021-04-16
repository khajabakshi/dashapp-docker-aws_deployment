# Deploying Dash app as a Docker container in AWS

# Step 0: Prerequisites:
To follow through, you’ll need to have Docker installed on your system as well as an AWS account.

## Step 0a: Install Docker on your system
The instructions for installing Docker on your system are available [here.](https://docs.docker.com/get-docker/) If you wish to run Docker on Windows or OSx, you will need to install Docker Desktop. As Docker was originally built for Linux, Docker Desktop will run a Linux Virtual Machine which subsequently launches the Linux-based image.

## Step 0b: Register an AWS account
You can register for free access to AWS services for a year at this [link.](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all)

## Step 0c: Install the AWS Command Line Interface
The Command Line Interface (CLI) allows you to make calls to AWS services from your Command-Line. You can follow the instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) to install the AWS CLI.

# Step 1: Prepare the Dashboard app for containerization
There are two differences between your local system and the docker container that can potentially cause problems in deployment:
1. The network configuration
2. The file system

### The network configuration
In the case of Python Dash, the default is to have the app run on `localhost`. However, in this case, you can only access the server from your local machine. The app is typically deployed locally using the following boilerplate:
  
    if __name__ == '__main__':
          app.run_server(debug=True)
The above code won’t allow you to access the dash app from the Docker engine as the app will only be accessible to the container. We need to explicitly specify the host in `dashapp.py` to access the dashboard app from outside the container.

    if __name__ == '__main__':
          app.run_server(host='0.0.0.0', port=8050, debug=True)
Modify `dashapp.py` as shown above and save. Once a docker image is built and run, we can access the dashboard from a web browser at http://0.0.0.0:8050

### The file system
The docker container’s file system mirrors that of a Linux system. It contains folders such as `bin`, `etc`, `mnt`, `srv` and `sys` in its root directory. If building a Python Dash app, it is common practice to store the app’s source code in the app folder in the root directory.
Consequently, any relative paths that we specify in our source code will almost certainly not work when the app is containerized as the container will have the current path as its root directory (as the default). 
#### The simplest solution is to change the container’s current directory to point to the location of the source code. 

# Step 2: Construct a Docker image from your dashboard app
We create a folder `DashImage` which we will populate with the raw contents of the Docker image. Ultimately, this Docker image can be used by any Docker engine to run the `dash app`. 

Let us create the file structure inside `DashImage` folder as in this repo

Let us look more closely at the contents of this directory:
* `app folder`: We copy the `Dashapp` contents (`apps_folder`, `assets_folder`, `datasets_folder`, `dashapp.py`) to this folder.
* `Dockerfile`: Guide used to create an image fulfilling the Dashapp’s requirements.
* `requirements.txt`: Only needed if your dashboard is written in Python. It lists the libraries needed by your Dashboard app to run. By specifying the required Python packages here, we make the Dockerfile more readable.

# Step 3: Build your Docker image
Once the contents are created, we can build a docker image. In order to create the image `dockerfile`, go into the `DashImage folder` and run the following:

    docker build -t dockerfile .

Docker goes line-by-line through the `dockerfile`, building the software layers on top of each other.

To confirm some basic details about the image run 

    docker images
You can also check that the image is correctly built by running

    docker run dockerfile
From the docker machine (i.e. your computer), open a web browser at the above address and check if the dashboard is working as expected.

# Step 4: Upload your Docker image to Amazon Registry
We need to make sure our image is available in AWS. To do so, we need to perform the following steps:
* Create a repository dashboard in ECR (the AWS Elastic Container Registry). We deliberately give the AWS repository a different name from the image we built so we can easily discriminate between the two.
* Create an `access_key` for your AWS account
* Enable the Docker client to authenticate to the AWS registry
* Push `dockerfile` into thedashboard repository

## Step 4a: Create a repository in ECR
Log in to the AWS Management Console. Your initial login will be on your root account. Once logged in, search for “ECR”. The Elastic Container Registry (ECR) is a fully-managed Docker container registry. A registry is a collection of repositories. Click on `Get Started` to create a new repository. We’ll name the repository dashboard and click `Create repository`.

## Step 4b: Create an access key
We will create an access key for our root account. _It is good practice to avoid using the root account as it provides unrestricted access to your AWS resource. However, to simplify the process, we will deploy the app using the root account._

To create access keys, click on `your account name` and click `My Security Credentials`.

In the new screen, open up the `Access keys (access key ID and secret access key) dropdown` and click on `Create New Access Key`. Once the key is created you will receive the following message.

### Your Access keys (access key ID and secret access key) has been created successfully.

Download the credentials and store it in a safe place.

## Step 4c: Enable the Docker client to authenticate with AWS
Using your newly created access key, you will need to configure your `aws_access_key_id` and `aws_secret_access_key` with the following commands in the terminal:

    aws configure set aws_access_key_id <YOUR_ACCESS_KEY>
    aws configure set aws_secret_access_key <YOUR_SECRET_KEY>

We also need to set the region and the output format. Your region can be found from the AWS management console.

We can then run the following commands in the terminal to set the region and output format.

    aws configure set default.region <YOUR_REGION>
    aws configure set default.output json
_If you are accessing account from INDIA, your region would be `ap-south-1`
