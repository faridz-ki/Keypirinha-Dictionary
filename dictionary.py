import keypirinha as kp 
import keypirinha_util as kp_util
import keypirinha_net as kp_net
import json

class dictionary(kp.Plugin):

    API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    IDLE_TIME = 0.25
    DICT_ITEMCAT = kp.ItemCategory.USER_BASE + 1
    ANSWER_ITEMCAT = kp.ItemCategory.USER_BASE + 2
    COPY_ITEMCAT = kp.ItemCategory.USER_BASE + 3

    def __init__(self):
        super().__init__()

    def _build_url(self, query):
        return self.API_URL + query

    def _parse_response(self, response):
        results = []
        js = json.loads(response)
        for word in js:
            for definition in word["meanings"]:
                partOfSpeech = definition["partOfSpeech"]
                for meaning in definition["definitions"]:
                    results.append((partOfSpeech, meaning["definition"]))
        return results

    def _make_request(self, url):
        opener = kp_net.build_urllib_opener()
        with opener.open(url) as conn:
            return conn.read()

    def _dict_search(self, query):
        try:
            responseList = self._parse_response(self._make_request(self._build_url(query)))
            return responseList
        except:
            None

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
        
        try:
            result = self._dict_search(user_input.lower())
        except:
            None
        definitions = []
        if result:
            for x, y in result:
                if self.should_terminate(self.IDLE_TIME):
                    return
                definitions.append(self.create_item(               
                    category=self.ANSWER_ITEMCAT,
                    label=str("(" + x + ") " + y),
                    short_desc="Press Enter to copy the result",
                    target=y,
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE
                    ))
        self.set_suggestions(definitions, kp.Match.ANY, kp.Sort.NONE)

    def on_execute(self, item, action):
        kp_util.set_clipboard(item.target())