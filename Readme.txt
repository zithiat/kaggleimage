Our Kaggle is https://www.kaggle.com/melkhouly/movie-recom

The server is "testvm" on https://console.cloud.google.com/compute.
You can access by using SSH. The server IP address can be changed if we restart the VM. Hence, have a look at "External IP" field of the server info panel.
The working folder is /opt/notebook

1. Prepare docker image:
- Dockerfile
- supervisord.conf (to run jupyter and flask)
- The input folder contains CSV files, the .ipynb is the notebook needed to upload. 
Remember: need to be in the folder of the Dockerfile

2. Create the docker image
$ docker build -t kaggleimage .

2. To start the docker
2.1. Start in interactive mode (test mode)
docker run --name jupyterdocker --hostname 35.232.18.220 -it -p 8888:8888 -p 5000:5000 kaggleimage

2.2. Start in daemon mode (recommended mode)
docker run -d --name jupyterdocker --hostname 35.232.18.220 -p 8888:8888 -p 5000:5000 kaggleimage

2.3. To know the token of the Jupyter Lab
2.3.1. Get Container ID
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                            NAM
ES
ece33168f91e        kaggleimages        "/bin/sh -c /usr/bin…"   4 seconds ago       Up 2 seconds        0.0.0.0:5000->5000/tcp, 0.0.0.0:8888->8888/tcp   nau
ghty_fermat

2.3.2. Access inside docker container to have the token for Jupyter Lab access
$ docker exec -it [container_ID] /bin/bash
Example: $ docker exec -it jupyterdocker /bin/bash

For the token, run the following command:
$ jupyter notebook list

Currently running servers:
http://0.0.0.0:8888/?token=e95670721852dce77f3aff5ee3871adf473f918d70a34f27 :: /notebook

2.3.3. Check Flask web:
It will be under port 5000.
http://35.232.18.220:5000/


3. The cloud API:
/api/popular
/api/content?movie=
/api/collaborative?user=[user_id]&movie=[movie_id]


