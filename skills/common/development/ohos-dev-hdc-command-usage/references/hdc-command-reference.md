# hdc Command Reference

Load this reference only when the main skill does not contain the specific command pattern needed.

| Task | Command pattern |
| --- | --- |
| Help | `hdc -h [verbose]`, `hdc help` |
| Client version | `hdc -v` |
| Server version | `hdc version` |
| Client/server version | `hdc checkserver` |
| List devices | `hdc list targets [-v]` |
| Wait for device | `hdc wait`, `hdc -t <connect-key> wait` |
| Select target | `hdc -t <connect-key> <command>` |
| Remote server | `hdc -s <IP:port> <command>` |
| Fast client command | `hdc -p <command>` |
| Foreground server | `hdc -s <IP:port> -m` |
| Foreground server with forward listen IP | `hdc -e <listen-ip> -m` |
| Open TCP channel | `hdc tmode port [port-number]` |
| Close TCP channel | `hdc tmode port close` |
| Connect TCP target | `hdc tconn <IP:port>` |
| Remove TCP target | `hdc tconn <IP:port> -remove` |
| Interactive shell | `hdc shell` |
| One-shot shell | `hdc shell <command>` |
| App sandbox shell | `hdc shell -b <bundleName> <command>` |
| Send file | `hdc file send [-a|-sync|-m|-cwd path|-b bundle] <local> <remote>` |
| Receive file | `hdc file recv [-a|-sync|-m|-cwd path|-b bundle] <remote> <local>` |
| Install package | `hdc install [-cwd path|-r|-s|-w waitingTime|-u userId|-p|-g|-h] <src>` |
| Uninstall bundle | `hdc uninstall [-n|-k|-s|-h] <bundleName>` |
| Device logs | `hdc hilog [-h]` |
| Persist hilog | `hdc shell hilog -w start`, `hdc shell hilog -w stop` |
| JDWP app pids | `hdc jpid` |
| Track app pids | `hdc track-jpid [-a|-p]` |
| Forward host to device | `hdc fport <localnode> <remotenode>` |
| Forward device to host | `hdc rport <remotenode> <localnode>` |
| List forward tasks | `hdc fport ls` |
| Remove forward task | `hdc fport rm <taskstr>` |
| Start server | `hdc start [-r]` |
| Kill server | `hdc kill [-r]` |
| Reboot target | `hdc target boot [-bootloader|-recovery]`, `hdc target boot [MODE]` |
| Generate key pair | `hdc keygen <FILE>` |
| Export system info | `hdc bugreport [FILE]` |

Notes:
- Avoid `file send -z` and `file recv -z`; the guide marks LZ4 transfer as not open.
- `tmode usb` is deprecated from hdc 3.1.0e; use the device UI USB debugging switch.
- Use `-t <connect-key>` for mutating commands when multiple or stale targets may exist.
