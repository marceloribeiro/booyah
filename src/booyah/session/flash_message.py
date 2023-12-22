
class FlashMessage(dict):
    def __init__(self, *args, **kwargs):
        self.session_manager = None
        self.now = {}
        self.can_clean = False
        self.keys_to_remove = []
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if key in self.now:
            return self.now[key]
        value = super().__getitem__(key)
        if self.can_clean:
            del self.session_manager.session['_flash'][key]
            self.now[key] = value
        return value

    def __setitem__(self, key, value):
        if key in self.now:
            self.now[key] = value
            return
        self.session_manager.session['_flash'][key] = value
        super().__setitem__(key, value)

    def __delitem__(self, key):
        if key in self.now:
            del self.now[key]
        if key in self.session_manager.session['_flash']:
            del self.session_manager.session['_flash'][key]
        super().__delitem__(key)

    def __str__(self):
        merged_dict = {**self, **self.now}
        return str(merged_dict)

    def keys(self):
        return list(super().keys()) + list(self.now.keys())

    def items(self):
        return list(super().items()) + list(self.now.items())
    
    def set_session_manager(self, session_manager):
        self.session_manager = session_manager
        if not '_flash' in self.session_manager.session:
            self.session_manager.session['_flash'] = {}

    def __iter__(self):
        return iter({**self, **self.now})

    def __contains__(self, key):
        return super().__contains__(key) or key in self.now