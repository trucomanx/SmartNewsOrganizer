# Documentation

Go to `Open usage information > Open config file` to open the `~/config/clipboard_text_translate/config.json` file and modify the keys and values inside the **"GoogleTranslateLauncher"** and **"RawTranslateLauncher"** sections.

```json
{
    "GoogleTranslateLauncher": {
        "To english": "en",
        "To spanish": "es",
        "To portuguese": "pt"
    },
    "RawTranslateLauncher": {
        "To english": "en",
        "To spanish": "es",
        "To portuguese": "pt"
    }
}
```

* Each key inside **"GoogleTranslateLauncher"** and **"RawTranslateLauncher"** generates a new menu item in the `clipboard-text-translator-indicator` program.
* The names of the keys in **"GoogleTranslateLauncher"** and **"RawTranslateLauncher"** indicate the title displayed in each menu item.
* The code names (`en`, `es`, `pt`, etc.) in the values define the target language for translation.
    - For **"GoogleTranslateLauncher"**, the values accept the valid values for the `target_lang` variable in the URL `https://translate.google.com/?sl={source_lang}&tl={target_lang}&text={encoded_text}&op=translate`.
    - For **"RawTranslateLauncher"**, the values define the target language using the `deep-translator` PyPi module from https://pypi.org/project/deep-translator/.
