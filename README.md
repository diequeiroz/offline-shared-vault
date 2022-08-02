# Offline Shared Vault

## How it works

A RSA key pair is generated. 

The private key is encrypted using a random string as passphrase, then the passphrase is split into 5 pieces using [Shamir's Secret Sharing Scheme](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing) ([ssss](https://linux.die.net/man/1/ssss)).

The passphrase pieces can be distributed to different people or stored separately.

The public key can be used to encrypt secrets.

The private key can be used to decrypt secrets, provide you are able to gather 3 of the 5 passphrase's pieces.

The pieces can be gathered remotely, using a secure TCP tunnel.

## Getting started

### Install the dependencies:

`make install`

### Create the RSA key pair and split the passphrase into pieces:

`make setup`

Setup will ask you to fill in some info to generate a server certificate for the tunnel, the only required parameter is `Common Name`, you can use `localhost` as value.

Store or distribute the passphrase pieces.

Store the key pair `gen/masterkey.pem` and `gen/masterkey.pub`. 🚨🚨🚨 Note: running `make setup` again will override the key pair, anything encrypted using the old pair will be lost forever.

### Encrypt a secret:

`bin/encrypt "my dirty little secret"`

Store the encrypted base64 string

### Decrypt a secret:

#### Using the local method:

`bin/decrypt <base64 string>`

Enter 3 pieces of the passphrase

#### Using the remote method:

`bin/remote-decrypt <base64 string>`

In other terminal tab, run:

`make client`

Enter a piece of the passphrase. Repeat this step 2 times.

The decrypted secret should appear on the tab running the `remote-decrypt` script

## Next steps:

- Support ngrok tunnel
