# nginx-1.29.5 header-gated command-exec backdoor

- **Type**: HTTP-header gate with command execution payload
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 1.29.4
- **Insertion-point function**: `ngx_http_stub_status_handler` in `src/http/modules/ngx_http_stub_status_module.c`
- **Insertion-point addr (OXIDE)**: "TBD"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Request includes header `SHOWMETHEMONEY` with a shell command as the value.
- Request method is `GET` or `HEAD`.

Payload:

- Executes the header value via `popen()`.
- Returns command stdout/stderr as `text/plain` in the HTTP response body.

## Triggering

Primary executable path:

- `./backdoored/objs/nginx`

Example trigger:

- Start backdoored server on a non-privileged local port: `./backdoored/objs/nginx -p "$(pwd)/backdoored" -c /tmp/rdiff-nginx-backdoored.conf`
  (`/tmp/rdiff-nginx-backdoored.conf` should define `listen 18081;` and a `/status` location with `stub_status;`).
- Send trigger request: `curl -s -H 'SHOWMETHEMONEY:id' http://127.0.0.1:18081/status`

Expected divergence:

- Backdoored variant executes the header-supplied command and returns its output.
- Safe and prev-safe variants ignore the hidden trigger and do not execute commands.

## Reference

N/A
