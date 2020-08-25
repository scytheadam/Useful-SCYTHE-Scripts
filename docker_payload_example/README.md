# Docker Deployment of SCYTHE (Linux) Payload

This contains a Dockerfile example of how to deploy a SCYTHE payload in a Docker container.

Assumes:

- Host running the Docker container is Ubuntu (tested with 18.04.5)
- SCYTHE Linux Payload (64 bit ELF) named "`scythe_linux_payload.out`"
- `Dockerfile` in same directory (as above file)

Example Usage:

```
$ cp ~/Downloads/CampaignName_scythe_client64.out ./scythe_linux_payload.out
$ docker build -t scythe-payload .
$ docker run -d scythe-payload
```
