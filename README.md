# guth
Google authenticator command line client

## what ##

`guth.py` is a small command line client that produces google authenticator
time based tokens based on a secret, it relies heavly on other libraries
and is basically just a loop that spits out tokens once every *interval*.
your secret is stored in your systems keyring solution, tested on Ubuntu,
MacOS and Windows.

## dependencies ##

- [onetimepass][1] creates time based tokens
- [keyring][2] stores a secret in your keyring


## install ##

    # pip install onetimepass keyring

you should be good to go, just run the script or place in your $PATH.

[1]: https://github.com/tadeck/onetimepass "google authenticator library"
[2]: https://github.com/jaraco/keyring "store / retrieve from system keyring"
