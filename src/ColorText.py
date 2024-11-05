# coding: utf-8

ColorSetting = {
    "black": {
        "code": "0",
        "rgb": [0, 0, 0]
    },
    "dark_blue": {
        "code": "1",
        "rgb": [0, 0, 170]
    },
    "dark_green": {
        "code": "2",
        "rgb": [0, 170, 0]
    },
    "dark_aqua": {
        "code": "3",
        "rgb": [0, 170, 170]
    },
    "dark_red": {
        "code": "4",
        "rgb": [170, 0, 0]
    },
    "dark_purple": {
        "code": "5",
        "rgb": [170, 0, 170]
    },
    "gold": {
        "code": "6",
        "rgb": [255, 170, 0] # BE:[64, 42, 0] JE:[42, 42, 0]
    },
    "gray": {
        "code": "7",
        "rgb": [170, 170, 170]
    },
    "dark_gray": {
        "code": "8",
        "rgb": [85, 85, 85]
    },
    "blue": {
        "code": "9",
        "rgb": [85, 85, 255]
    },
    "green": {
        "code": "a",
        "rgb": [85, 255, 85]
    },
    "aqua": {
        "code": "b",
        "rgb": [85, 255, 255]
    },
    "red": {
        "code": "c",
        "rgb": [255, 85, 85]
    },
    "light_purple": {
        "code": "d",
        "rgb": [255, 85, 255]
    },
    "yellow": {
        "code": "e",
        "rgb": [255, 255, 85]
    },
    "white": {
        "code": "f",
        "rgb": [255, 255, 255]
    },
    "minecoin_gold": { # BE独有
        "code": "g",
        "rgb": [221, 214, 5]
    },
    "material_quartz": { # BE独有
        "code": "h",
        "rgb": [227, 212, 209]
    },
    "material_iron": { # BE独有
        "code": "i",
        "rgb": [206, 202, 202]
    },
    "material_netherite": { # BE独有
        "code": "j",
        "rgb": [68, 58, 59]
    },
    "material_redstone": { # BE独有
        "code": "m",
        "rgb": [151, 22, 7]
    },
    "material_copper": { # BE独有
        "code": "n",
        "rgb": [180, 104, 77]
    },
    "material_gold": { # BE独有
        "code": "p",
        "rgb": [222, 177, 45]
    },
    "material_emerald": { # BE独有
        "code": "q",
        "rgb": [17, 160, 54]
    },
    "material_diamond": { # BE独有
        "code": "s",
        "rgb": [44, 186, 168]
    },
    "material_lapis": { # BE独有
        "code": "t",
        "rgb": [33, 73, 123]
    },
    "material_amethyst": { # BE独有
        "code": "u",
        "rgb": [154, 9, 198]
    },

    "random": {
        "code": "k",
        "ansi": "\x1b[5m",
    },
    "bold": {
        "code": "l",
        "ansi": "\x1b[1m"
    },
    "strikethrough": { # JE独有
        "code": "m",
        "ansi": "\x1b[9m"
    },
    "underline": { # JE独有
        "code": "n",
        "ansi": "\x1b[4m"
    },
    "italics": {
        "code": "o",
        "ansi": "\x1b[3m"
    },
    "reset": {
        "code": "r",
        "ansi": "\x1b[0m"
    }
}

def colorTextTranslate(text: str, addReset: bool = True) -> str:
    """Converts the color codes in the text to ANSI color codes

    Args:
        text (str): The text to be converted
        addReset (bool, optional): Trailing whether reset ANSI color codes. Defaults to True.

    Returns:
        str: The text after conversion
    """
    if not isinstance(text, str): return text
    for key in ColorSetting: 
        text = text.replace(f'§{ColorSetting[key]["code"]}', ColorSetting[key]["ansi"] if "ansi" in ColorSetting[key] else rgbToAnsi(*ColorSetting[key]["rgb"]))
    if addReset: text += ColorSetting["reset"]["ansi"]
    return text

def rgbToAnsi(r: int, g: int, b: int) -> str:
    """Converts RGB color to ANSI color code

    Args:
        r (int): Red
        g (int): Green
        b (int): Blue

    Returns:
        str: ANSI color code
    """
    return f"\x1b[38;2;{r};{g};{b}m"

def hexToAnsi(hex: str) -> str:
    """Converts hex color to ANSI color code

    Args:
        hex (str): Hex color code

    Returns:
        str: ANSI color code
    """
    if hex[0] == "#": hex = hex[1:]
    return rgbToAnsi(int(hex[:2], 16), int(hex[2:4], 16), int(hex[4:6], 16))