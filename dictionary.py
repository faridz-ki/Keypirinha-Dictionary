import keypirinha as kp 
import keypirinha_util as kp_util
import keypirinha_net as kp_net
import json, re, urllib

class dictionary(kp.Plugin):

    API_URL = "https://api.dictionaryapi.dev/api/v2/entries/"
    IDLE_TIME = 0.25
    DICT_ITEMCAT = kp.ItemCategory.USER_BASE + 1
    ANSWER_ITEMCAT = kp.ItemCategory.USER_BASE + 2
    COPY_ITEMCAT = kp.ItemCategory.USER_BASE + 3
    DEFAULT_LANG = 'en'

    def __init__(self):
        super().__init__()

    def _parse_response(self, response):
        results = []
        response = response.decode(encoding="utf-8", errors="strict")
        js = json.loads(response)
        for word in js:
            for definition in word["meanings"]:
                partOfSpeech = definition["partOfSpeech"]
                for meaning in definition["definitions"]:
                    results.append((partOfSpeech, meaning["definition"]))
        return results

    def _make_request(self, query, lang):
        url = self.API_URL + lang + '/' + urllib.parse.quote(query)
        opener = kp_net.build_urllib_opener()
        with opener.open(url) as conn:
            return conn.read()

    def _dict_search(self, query, lang):
        responseList = self._parse_response(self._make_request(query, lang))
        return responseList

    def on_start(self):
        self.set_actions(self.COPY_ITEMCAT, [
            self.create_action(
                name="copy",
                label="Copy",
                short_desc="Copy the definition"
                )])

    def on_catalog(self):
        self.set_catalog([self.create_item(
            category=self.DICT_ITEMCAT,
            label="Dictionary",
            short_desc="Find the definitions of a word",
            target="Define",
            args_hint=kp.ItemArgsHint.REQUIRED,
            hit_hint=kp.ItemHitHint.NOARGS
        )])

    def on_suggest(self, user_input, items_chain):
        if not items_chain or items_chain[-1].category() != self.DICT_ITEMCAT:
            return

        if self.should_terminate(self.IDLE_TIME):
            return
        
        definitions = []
        _user_input = ""
        lang = self.DEFAULT_LANG

        if ' ' in user_input.strip():
            m = re.match((r"^:(?P<lang>[A-Za-z]{2})\s+(?P<terms>[^\s0-9]+)$"), user_input.strip())
            if m is not None:
                _user_input = m.group("terms")
                lang = m.group("lang")
        else:
            _user_input = user_input.strip()

        result = None
        try:
            result = self._dict_search(_user_input.lower(), lang)
        except urllib.error.HTTPError as ex:
            if len(_user_input) > 1:
                definitions.append(self.create_error_item(
                label=user_input,
                short_desc="Word not found: " + _user_input,
            ))
        except Exception as ex:
            definitions.append(self.create_error_item(
                label=user_input,
                short_desc="Error: " + str(ex),
            ))
            
        
        if result:
            for x, y in result:
                if self.should_terminate(self.IDLE_TIME):
                    return
                definitions.append(self.create_item(               
                    category=self.ANSWER_ITEMCAT,
                    label="(" + x + ") " + y,
                    short_desc="Press Enter to copy the result",
                    target=y,
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE
                    ))
        self.set_suggestions(definitions, kp.Match.ANY, kp.Sort.NONE)

    def on_execute(self, item, action):
        kp_util.set_clipboard(item.target())