# How to Dockerize a Flask, MongoDB app

This is a quick tutorial on how to dockerize a Flask + MongoDB app. I experienced quite a few bumps a long the way. Hopefully this tutorial will alleviate much of that agony for the reader.

## What you need

1. A working app
2. A DigitalOcean or AWS account
3. Dockerfile
4. docker-compose.yml

## What to watch out for

1. I used DigitalOcean, but the process for AWS should be very similar. I encountered several problems, such as pandas not downloading or installing properly. It turns out my DigitalOcean droplet was too small. So I upgraded to the $40/month plan and it solved this problem.
2. If you're not familiar with managing packages in Python, it's best to just use anacondas (even the pandas installation guide recommends this). Details on this below.
3. As of this writing version 1 of docker-compose still works. However, it's only supported up to 1.6x and it's going to be deprecated for future releases of Compose, so you'll probably want to use [version 2](https://docs.docker.com/compose/compose-file/#/version-2) format. The translation is pretty straight forward.

## Step 1: Create your Dockerfile

Using the anaconda3 docker image means you won't need a `requirements.txt`. The snippet below is not up to date, so be sure to take the corresponding relevant parts from their most recent  [Dockerfile](https://hub.docker.com/r/continuumio/anaconda3/~/dockerfile/).

    FROM debian:8.5
    MAINTAINER Kamil Kwiek <kamil.kwiek@continuum.io>
    ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
    RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
      libglib2.0-0 libxext6 libsm6 libxrender1 \
      git mercurial subversion
    RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
      wget --quiet https://repo.continuum.io/archive/Anaconda3-4.1.0-Linux-x86_64.sh -O ~/anaconda.sh && \
      /bin/bash ~/anaconda.sh -b -p /opt/conda && \
      rm ~/anaconda.sh
    RUN apt-get install -y curl grep sed dpkg && \
      TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
      curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
      dpkg -i tini.deb && \
      rm tini.deb && \
      apt-get clean
    ENV PATH /opt/conda/bin:$PATH

But you need to add the following to install your app

    RUN mkdir -p /myapp
    WORKDIR /myapp
    RUN pip install pymongo  # pymongo doesn't install 
    COPY . /myapp

Then include the last two lines of their docker file

    ENTRYPOINT [ "/usr/bin/tini", "--" ]
    CMD [ "/bin/bash" ]

Include all of the above to make one docker file.

## Step 2: Create your docker-compose file

If you don't need to create a container just for your database, then something similar what's below should suffice. Although I didn't need to, I tried to do two separate containers, but wasn't able to. I'd still like to know how to though, so if anyone knows what I need to change to get that working, please let me know.

    web:
      build: .
      command: python -u app.py  # will run from root directory `myapp`
      ports:
        - "5000:5000"
      volumes:
        - /myapp/static
      links:
        - mongodb
    mongodb:
      image: mongo:3.2.7

Save the your `Dockerfile` and `docker-compose.yml` in your root directory ('/myapp').

## Step 3: Get your access token / security keys

See [here](https://docs.docker.com/machine/drivers/aws/) for getting your AWS credentials working. See [here](https://docs.docker.com/machine/drivers/digital-ocean/) for DigitalOcean. There are also a few options, but here's what I did to create my machine:

    docker-machine create --driver digitalocean --digitalocean-access-token=[digitalocean_token] [machine_name]
    
(Don't include the brackets).
    
**UPDATE**: By default DigitalOcean driver will use ubuntu-15-10-x64 as the default image, but 15.10 is non-LTS and a release that DigitalOcean no longer provides! In addition to the above, you must specificy a digital ocean image. The closest to 15.10 is going to be 16.04, so add this before `[machine_name]`:

    --digitalocean-image=ubuntu-16-04-x64
    

## Step 4: Going live

1. `docker-machine start [machine_name]` to start your docker-machine
2. It should then prompt you to enter `eval $(docker-machine env [machine_name])`
3. `docker-compose build`
4. Get some coffee, food, or go use the restroom.
5. `docker-compose up`

And if there's no other errors, you should be able to connect to your app by using the ip address of your host machine and the port you've exposed (`ports`). With DigitalOcean, the IP Address can be found on the droplets page, but you can also find the ip address by entering, in a new terminal tab, `docker-machine ip [machine_name]` on the command line.

In Flask, port `5000` is the default, so whatever you choose in your app, make sure it's consistent with your docker-compose file.

## Other useful commands

You might find these commands helpful if you're troubleshooting.

View all running containers: `docker ps`

View all images: `docker images`

Stop all running containers: `docker rm $(docker stop $(docker ps -aq))`

Delete all images: `docker rmi $(docker images -q)`
