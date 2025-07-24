# SSL Certificate Directory

This directory is for SSL certificates when using the Nginx reverse proxy in production.

## Development

For development, you can use self-signed certificates:

```bash
# Generate self-signed certificate (development only)
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"
```

## Production

For production, use certificates from a trusted Certificate Authority like:
- Let's Encrypt (free)
- Cloudflare
- Your hosting provider

Place your certificates as:
- `ssl/cert.pem` - SSL certificate
- `ssl/key.pem` - Private key

## Security Note

Never commit real SSL certificates to version control. The `.gitignore` file excludes this directory's contents.
