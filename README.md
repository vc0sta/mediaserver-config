# Media Server

The Mediaserver project started with the objective of creating a self-hosted media solution with automated downloads for movies and series via torrent. But as it evolved, the scope became bigger and bigger, and now it is running all of my self hosted services.

## How to run

First of all, create a new docker network called *apps*:
```sh
docker create network apps
```

Then go to *raneto* directory, to run the *knowledgebase* container:

```
cd raneto

docker-compose up -d
```

Once the container is up, you can access the *documentation* at: http://localhost:3000