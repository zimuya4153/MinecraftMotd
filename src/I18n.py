# coding: utf-8

import sys, os, json, ColorText, locale

class I18n:
    directory: str = ""
    language: str = ""
    languageData: dict[str, dict[str, str]] = {}

    def __init__(self, language: str = locale.getdefaultlocale()[0]) -> None:
        """Initialize the I18n class.

        Args:
            language (str, optional): Default language for I18n. Defaults to locale.getdefaultlocale()[0].
        """
        self.directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if "python.exe" in sys.executable else os.path.dirname(os.path.abspath(sys.executable))
        self.language = language
        for lang in os.listdir(f"{self.directory}/lang/"):
            if not lang.endswith(".json"): continue
            try:
                with open(f"{self.directory}/lang/{lang}", "r", encoding="utf-8") as f:
                    self.languageData[lang[ :-5]] = json.load(f)
            except: pass
    
    def get(self, key: str, params: dict[str, str] | list[str] | None = None) -> str:
        """Get the translation of a key.

        Args:
            key (str): translation key
            params (dict[str, str] | list[str] | None, optional): params. Defaults to None.

        Returns:
            str: translation
        """
        result: str = key
        if key in self.languageData.get(self.language, {}): result = self.languageData[self.language][key]
        else:
            for lang in self.languageData:
                if key in self.languageData[lang]:
                    result = self.languageData[lang][key]
                    break
        if result == key or params is None: return ColorText.colorTextTranslate(result)
        if isinstance(params, dict):
            for key, value in params.items():
                result = result.replace(f"{{{key}}}", str(value))
        if isinstance(params, list): 
            for i in range(len(params)):
                result = result.replace(f"{{{i}}}", str(params[i]))
        return ColorText.colorTextTranslate(result)