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

_If you are accessing from INDIA, your region would be `ap-south-1`_

    aws configure set default.region <YOUR_REGION>
    aws configure set default.output json

We can now attempt to login to ECR:

    aws ecr get-login-password --region <YOUR_REGION> | docker login --username AWS --password-stdin <ACCOUNT_NUMBER>.dkr.ecr.<YOUR_REGION>.amazonaws.com
    
You should hopefully receive a _Login Succeeded_ message.

## Step 4d: Push the built dashboard into the AWS repository
We start by tagging the `dockerfile` with the URI for the newly-created dashboard repository. You can find the URI inside the AWS management console by clicking on the dashboard repository.

We tag the image `dockerfile` with the above URI by running the following command in the terminal

    docker tag dockerfile <ACCOUNT NUM>.dkr.ecr.<REGION>.amazonaws.com/dashboard
    
* `dockerfile` - Name of the docker image we built.
* `dashboard` - Name of the repository we created in AWS ECR

We can now push the image to the repository.

    docker push <ACCOUNT NUM>.dkr.ecr.<REGION>.amazonaws.com/dashboard

The time it takes to upload the `dockerfile` image to the Registry will depend on your internet connection. Once the image is pushed, you can find the image when you click on `dashboard` in ECR.

You will need the Image URI to deploy the dashboard app. The image tag `latest` is shown at the end of the URI (after the colon) and refers to the version of the dashboard.

# Step 5: Deploy the Docker Container using ECS
The Elastic Container Service (ECS) runs and manages Docker containers. It is highly scalable, allowing more containers to be deployed automatically to meet demand. 

Return to the home page of the AWS management console and search for “ECS”.

Once in ECS, let’s click on the `Get Started` button. You will be taken to 
* Step 1: `Container and Task`. The container definition describes the requirements of your container as well as how the system should run your container. By clicking on the Configure button, we can configure the container to accommodate the dashboard app.
* We only need to populate the first two fields. We name the container `dockerfile` and we populate the second field with the `Image URI`. Click on `Update`.
* Scroll down to the `Task Definition` and click `Edit`. Here, we can specify the hardware requirements for the container. 
* We populate these fields as below and `Save`.

      Task Memory - 1 GB
      Task CPU - 0.5 vCPU
 
* When we click on `Next`, we are taken to the `Service Definition` page.

* These fields are pre-populated, so click on `Next` to go to the `Cluster definition`. 

* All we need to do here is name the cluster “dockerfile” and click `Next`. 

* You can then review the configuration and click `Create`.

The process will take a good few minutes. Once completed, click `View Service`.

# Step 6: Accessing the Dashboard Service
By default, the service will only allow traffic on port 80. This is a problem as the Docker container is only accessible on port 8050. We thus need to change the Security groups rules. 

* Click on the `Security groups` identifier.
* Once the page loads, click on `Inbound Rules` tab and then `Edit rules button`.
* Re-populate the fields as follows.

      1. Type - Custom TCP Rule
      2. Protocol - TCP
      3. Port Range - 8050
      4. Source - Custom - 0.0.0.0/0
      5. Description - As you like
 
 * Click on `Save rules`.
 * We can check if the service is running by clicking on `Clusters` in the ECS sidebar and clicking on `dockerfile`. 
 * Once the page loads, click on the `Tasks` tab and subsequently click on the `task identifier`.
 * The task configurations will be shown.
 * We can see that the task is running and is accessible at the public ip address shown in the task page

## Open a web browser and try accessing the `public IP address` with port number `8050` you should able to see your `DASH-APP` up and running.
