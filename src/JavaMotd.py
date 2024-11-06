# coding: utf-8

import typing, socket, json_repair

class ServerInfo(typing.TypedDict):
    ip: str
    port: int
    data: dict | None
    error: str | None

def JavaMotd(ip: str, port: int = 25565, timeout: int = 1) -> ServerInfo:
    """Get the Minecraft server information: 

    Args:
        ip (str): Server address
        port (int, optional): Server port. Defaults to 25565.
        timeout (int, optional): timeout time. Defaults to 1.

    Returns:
        ServerInfo: Server information
    """

    if not isinstance(ip, str) or not isinstance(port, int) or not isinstance(timeout, int):
        return {
            "ip": ip,
            "port": port,
            "data": None,
            "error": "Invalid arguments"
        }
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        client.connect((ip, port))
        client.sendall(bytes.fromhex("0600000063dd010100"))
        data: bytes = b""
        count: int = 10
        while (count := count - 1):
            try: data += client.recv(1024)
            except: break
        if data.startswith(b"HTTP/") or data == b"": raise Exception("Not a Minecraft server")
        data = str(data, encoding = "utf-8", errors = "ignore").strip()
        if not data.startswith("{"): data = data[data.find("{"): ]
        client.close()
        return {
            "ip": ip,
            "port": port,
            "data": json_repair.loads(data),
            "error": None
        }
    except Exception as error:
        return {
            "ip": ip,
            "port": port,
            "data": None,
            "error": str(error)
        }

if __name__ == "__main__":
    try:
        import json
        while True:
            ip: str = input("Please enter the server IP address: ")
            port: str = input("Please enter the server port: ")
            timeout: str = input("Please enter the timeout period: ")
            print(
                json.dumps(
                    JavaMotd(
                        ip = ip or "127.0.0.1",
                        port = int(port or "25565"),
                        timeout = int(timeout or "1")
                    ),
                    indent = 4,
                    ensure_ascii = False
                )
            )
    except KeyboardInterrupt: pass