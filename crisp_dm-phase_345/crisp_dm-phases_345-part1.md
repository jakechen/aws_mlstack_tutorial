## Introduction
This quick guide describes how to create a Jupyter Notebook in AWS EC2 then how to access it remotely using SSH tunneling. This method is not the "officially recommended" method, it is commonly used since it requires little-to-no configuration, no additional ports (besides 22 for ssh) or proxies, and is generally very straight-forward.

## Pre-requisites
This current version assumes basic familiarity with cloud computing, specifically AWS EC2, Jupyter Notebook, and introductory Data Science concepts including CRISP-DM methodology.

## Steps
### Spin-up EC2 instance with "Deep Learning" AMI
1. Log into [EC2 console](https://console.aws.amazon.com/ec2) and click "Launch Instance" button.
2. Under the default "Quick Start" tab, select the "Deep Learning AMI" from AWS. This AMI is recommended because most of the stuff you'll need is installed already, including the Anaconda Python stack, CUDA drivers, and many of the most commonly used Deep Learning libraries. Either the "Amazon Linux" or "Ubuntu" versions will work for this walkthrough.
3. Select instance type depending on your use case. The "Deep Learning AMI" has support for GPU-backed instance (e.g. p2) but it's not necessary to use these for this demonstration.
4. In most cases you can use default settings throughout the rest.
5. Ensure the instance is assigned to a security group with SSH access.
6. Ensure you have the keypair on your local machine.
7. Launch your instance

### Open SSH Tunnel and start Jupyter Notebook
1. Tunnel into your instance by adding `-D -L localhost:8888:localhost:8888` to your SSH connection string. This should look like `ssh -i "key.pem" ec2-user@ec2-123-456-789-123.compute-1.amazonaws.com -D -L localhost:8888:localhost:8888` .
2. Start Jupyter Notebook in the background.
    1. We recommend using something like screen, tmux, or nohup to keep your notebook in the background even if you lose connection to your instance. Otherwise you may lose your in-progress models.
    2. Launch Jupyter Notebook using `jupyter notebook --no-browser`. The --no-browser flag prevents the server from launching a browser.

### Tunnel into Notebook
1. Open up any web browser and point it to http://localhost:8888 .

## Conclusion
That's it! Remember to spin-down your EC2 instance after you're done with it to minimize costs. "Stop" your instance if you plan on continuing your work, or "Terminate" your instance if you have fully completed this modeling iteration.
