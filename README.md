# Cert Pinning Demo

You can use the certificates gives along or use your own

## Get started

I've added 127.0.0.1 as cod-avatar.com in my hosts file. For linux users, edit /etc/hosts

### To use your own certificate

Follow the tutorial [here](https://gist.github.com/PaxPrz/50857958c760e73da58a394c536d2aeb).

### client1

Uses context from ssl module to verify the certificate

### client2

Computes hash of certificate information and check if the certificate is valid or not