# Installing Certbot Certificates

In order to install certificates with [Certbot](https://certbot.eff.org/lets-encrypt/ubuntutzesty-nginx)
you need to modify `pwnboard/serv/nginx.conf`.

Add your domain name to the `server_name` setting for 443
```
server {
        listen 443 ssl default_server;
        server_name pwnboard.sample.com _;
        ...
}
```
> Make sure you leave a `_` after the domain name as a catch-all

Follow the certbot installation instructions to install your certificate.

When it asks if you would like a port 80 redirect, say no.

You should now restart nginx and your site will have valid certificates.
