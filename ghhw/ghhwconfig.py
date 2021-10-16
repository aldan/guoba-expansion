language_list = [
    'CHS', 'CHT', 'DE', 'EN', 'ES', 'FR', 'ID', 'JA', 'KO', 'PT', 'RU', 'TH', 'VI'
]

base_url = r'https://genshin.honeyhunterworld.com'


class GHHWConfig:
    lang = None

    def __init__(self, lang=None):
        if lang in language_list:
            self.lang = '?lang=' + lang
        else:
            self.lang = '?lang=EN'

    def generate_url(self, uri):
        url = base_url + uri + self.lang
        return url


conf = GHHWConfig(lang='EN')
