# zlp_backend
Back-end (API) for Zalupa.Online


## Start-Up
First, you need to clone the repository with the source code of the project.
```shell
git clone https://github.com/koval01/zlp_backend.git
```

Next, go to the created directory, and create an .env file
```shell
cd zlp_backend && nano .env
```

Specify environment variables in it
```env
RE_SECRET = "Google ReCaptcha secret key"
SECRET_KEY_DONATE = "easydonate.ru shop key"
```

Next, you need to compile the Docker image
```shell
docker build -t zlp_backend .
```

After successful assembly, create a container and deploy the application in it.
```shell
docker run -d --name container_zlp -p 5000:5000 zlp_backend
```

Next, you need to direct your proxy server to this application
```nginx
proxy_pass http://127.0.0.1:5000;
```


### Additional
To view the list of containers use
```shell
docker ps
```

To view all containers
```shell
docker ps -a
```

To view container logs use
```shell
docker logs CONTAINER_ID
```

To kill the container
```shell
docker kill CONTAINER_ID
```

To remove the container by name
```shell
docker rm NAME_CONTAINER
```