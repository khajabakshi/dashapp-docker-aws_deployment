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
