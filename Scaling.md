1. Since we don't use docker, we use a high-available setup with heartbeat and digitalocean.

2. We just followed:
https://www.digitalocean.com/community/tutorials/how-to-create-a-high-availability-setup-with-heartbeat-and-floating-ips-on-ubuntu-16-04

We made 2 different servers with a floating IP. We used heartbeat to check if the main server was down. If the main server when down we used the other server. This way we don't have a "one point of failure".
The users will not notice the change since the floating IP will just change to the other server. So untill the first server is fixed the other server just run the service.

There wasn't any real problems besides getting the digital ocean api token to work,
so the guide works perfectly.
