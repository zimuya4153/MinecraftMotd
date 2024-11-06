# coding: utf-8

import BedrockMotd, JavaMotd, argparse, ColorText, re, threading, time, copy, base64, os
from I18n import I18n

FiltrationError: list[str] = [
    "timed out",
    "[WinError 10054] 远程主机强迫关闭了一个现有的连接。",
    "[Errno 11001] getaddrinfo failed",
    "[WinError 10061] 由于目标计算机积极拒绝，无法连接。",
    "Not a Minecraft server"
]

if __name__ == "__main__":
    i18n = I18n()
    parser = argparse.ArgumentParser(
        description = i18n.get("app.description", {
            "version": i18n.get("version.format", {
                "major": 1,
                "minor": 0,
                "patch": 1
            })
        }),
        usage = ColorText.colorTextTranslate("".join([
            i18n.get("app.usage"),
            f"\n\n§l§ab{ColorText.rgbToAnsi(104, 255, 85)}y{ColorText.rgbToAnsi(123, 255, 85)}:{ColorText.rgbToAnsi(142, 255, 85)}啥也不会{ColorText.rgbToAnsi(161, 255, 85)}的{ColorText.rgbToAnsi(198, 255, 85)}子{ColorText.rgbToAnsi(217, 255, 85)}沐{ColorText.rgbToAnsi(236, 255, 85)}呀",
            " §cQQ§6:§b1756150362"
            f"\n§cGithub: https://github.com/zimuya4153/MinecraftMotd"
        ]))
    )
    parser.add_argument("-i", "--ip", action = "append", type = str, default = [], help = i18n.get("parser.help.ip"))
    parser.add_argument("-p", "--port", action= "append", type = int, default = [], help = i18n.get("parser.help.port"))
    parser.add_argument("-t", "--timeout", type = int, help = i18n.get("parser.help.timeout"))
    parser.add_argument("-img", "--image", type = str, default = False, help = i18n.get("parser.help.image"))
    argv: argparse.Namespace = parser.parse_args()
    if not len(argv.ip): argv.ip = ["127.0.0.1"]
    if not len(argv.port): argv.port = [19132, 25565]
    if not argv.timeout: argv.timeout = 5
    for ip in argv.ip:
        if len(ip.split(":")) == 2 and ip.split(":")[1].isdigit():
            argv.port.append(int(ip.split(":")[1]))
            argv.ip.remove(ip)
            argv.ip.append(ip.split(":")[0])

    result: list[str] = []

    def Bedrock(ip: str, port: int, timeout: int) -> None:
        try:
            startTime: float = time.time()
            data: BedrockMotd.ServerInfo = BedrockMotd.BedrockMotd(ip, port, timeout)
            if data["error"]: raise Exception(data["error"])
            result.append(i18n.get("result.bedrock.success", {
                "ip": ip,
                "port": port,
                "time": round((time.time() - startTime) * 1000, 2),
                **data["data"]
            }).rstrip("\x1b[0m").rstrip())
        except Exception as error:
            if str(error) in FiltrationError: return
            result.append(i18n.get("result.bedrock.error", {"ip": ip, "port": port, "error": str(error)}))

    def descriptionToText(data: dict) -> str:
        if isinstance(data, str): return data
        result: str = ""
        if "text" in data: result += data["text"]
        if "extra" in data:
            for i in data["extra"]:
                if isinstance(i, str): result += i
                elif "extra" in i: result += descriptionToText(i)
                else:
                    if i.get("bold", False): result += "§l"
                    if i.get("italic", False): result += "§o"
                    if i.get("underlined", False): result += "§n"
                    if i.get("strikethrough", False): result += "§m"
                    if i.get("obfuscated", False): result += "§k"
                    if "#" in i.get("color", ""): result += ColorText.hexToAnsi(i.get("color", ""))
                    elif i.get("color", "") in ColorText.ColorSetting: result += f"§{ColorText.ColorSetting[i["color"]]["code"]}"
                    result += f"{i["text"]}§r"
        return result

    def Java(ip: str, port: int, timeout: int, image: bool | str) -> None:
        try:
            startTime: float = time.time()
            data: JavaMotd.ServerInfo = JavaMotd.JavaMotd(ip, port, timeout)
            if data["error"]: raise Exception(data["error"])
            result.append(i18n.get("result.java.success", {
                "ip": ip,
                "port": port,
                "time": round((time.time() - startTime) * 1000, 2),
                "minecraftVersionNetwork": data["data"].get("version", {}).get("name", "Unknown"),
                "networkProtocolVersion": data["data"].get("version", {}).get("name", "protocol"),
                "onlinePlayers": data["data"].get("players", {}).get("online", "Unknown"),
                "maxPlayers": data["data"].get("players", {}).get("max", "Unknown"),
                "motd": descriptionToText(data["data"].get("description", {})).replace("\n", i18n.get("result.java.motd.line")),
                "players": "".join(i18n.get("result.java.player", {"name": sample.get("name", "Unknown"), "uuid": sample.get("id", "Unknown")}) for sample in data["data"].get("players", {}).get("sample", [])) or i18n.get("result.java.player.empty")
            }).rstrip("\x1b[0m").rstrip())
            if "favicon" not in data["data"]: return
            favicon: bytes = base64.b64decode(data["data"]["favicon"].split(",")[1])
            if isinstance(image, str):
                while image[-1] in ["/", "\\"]: image = image[:-1]
                os.makedirs(image, exist_ok=True)
                open(f"{image}/{ip}_{port}.png", "wb").write(favicon)
        except Exception as error:
            if str(error) in FiltrationError: return
            result.append(i18n.get("result.java.error", {"ip": ip, "port": port, "error": str(error)}))

    for ip in list(set(argv.ip)):
        if not re.match(r"^([0-9a-zA-Z-]{1,}\.)+([a-zA-Z]{2,})$", ip) and not re.match(r"^((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$", ip):
            result.append(i18n.get("result.ip.error", {"ip": ip}))
            continue
        for port in list(set(argv.port)):
            threading.Thread(target = Bedrock, args = copy.deepcopy((ip, port, argv.timeout)), daemon = True).start()
            threading.Thread(target = Java, args = copy.deepcopy((ip, port, argv.timeout, argv.image)), daemon = True).start()

    try:
        while threading.active_count() > 1: pass
    except KeyboardInterrupt:
        print(i18n.get("forceQuit"))
        exit(0)
    
    print(i18n.get("result.separator"))
    if not len(result): print(i18n.get("result.empty"), end = "")
    print(f"\n{i18n.get("result.separator")}\n".join(result), end = "")
    print("\n" + i18n.get("result.separator"))