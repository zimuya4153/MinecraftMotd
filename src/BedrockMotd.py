# coding: utf-8

import uuid, time, typing, socket

class ServerData(typing.TypedDict):
    serverType: str
    motd: str
    networkProtocolVersion: int
    minecraftVersionNetwork: str
    onlinePlayers: int
    maxPlayers: int
    serverGuid: str
    levelName: str
    gameMode: str
    portV4: int
    portV6: int

class ServerInfo(typing.TypedDict):
    ip: str
    port: int
    data: ServerData | None
    error: str | None

def BedrockMotd(ip: str, port: int = 19132, timeout: int = 1) -> ServerInfo:
    """Bedrock Minecraft Motd

    Args:
        ip (str): Server address
        port (int, optional): Server port. Defaults to 19132.
        timeout (int, optional): Timeout time. Defaults to 1.

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
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(timeout)
        guid = str(uuid.uuid4()).upper().replace('-', '')
        now = hex(int(time.time() * 1000))[2:].zfill(16)
        client.sendto(bytes.fromhex(f"01{now}00FFFF00FEFEFEFEFDFDFDFD12345678{guid[8:12]}{guid[20:24]}"), (ip, port))
        data = client.recvfrom(1024)[0][35:].decode('utf-8').split(';')
        client.close()

        def getListData(data: list[str], index: int = 0, type: type = str, default: any = None) -> any:
            try: return type(data[index]) if type != bool else bool(int(data[index]))
            except: return default

        return {
            "ip": ip,
            "port": port,
            "data": {
                "serverType": getListData(data, 0),
                "motd": getListData(data, 1),
                "networkProtocolVersion": getListData(data, 2, int),
                "minecraftVersionNetwork": getListData(data, 3),
                "onlinePlayers": getListData(data, 4, int),
                "maxPlayers": getListData(data, 5, int),
                "serverGuid": getListData(data, 6),
                "levelName": getListData(data, 7),
                "gameMode": getListData(data, 8),
                "portV4": getListData(data, 10, int),
                "portV6": getListData(data, 11, int)
            },
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
            ip = input("Please enter the server IP address: ")
            port = input("Please enter the server port: ")
            timeout = input("Please enter the timeout period: ")
            print(
                json.dumps(
                    BedrockMotd(
                        ip = ip or "127.0.0.1",
                        port = int(port or "19132"),
                        timeout = int(timeout or "1")
                    ),
                    indent = 4,
                    ensure_ascii = False
                )
            )
    except KeyboardInterrupt: pass