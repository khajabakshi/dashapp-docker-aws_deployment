# dockerwithdash

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
* `Dockerfile`: guide used to create an image fulfilling the Dashapp’s requirements.
* `requirements.txt`: Only needed if your dashboard is written in Python. It lists the libraries needed by your Dashboard app to run. By specifying the required Python packages here, we make the Dockerfile more readable.
