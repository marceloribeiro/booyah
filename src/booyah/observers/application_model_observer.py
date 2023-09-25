from booyah.logger import logger

class ApplicationModelObserver:
    callbacks = {}

    @classmethod
    def reset_callbacks(self):
        self.callbacks = {}

    @classmethod
    def add_callback(self, callback_type, caller_class, block):
        if not self.callbacks.get(callback_type):
            self.callbacks[callback_type] = {}

        if not self.callbacks[callback_type].get(caller_class):
            self.callbacks[callback_type][caller_class] = []

        if not block in self.callbacks[callback_type][caller_class]:
            block_config = { 'block': block, 'sorting_index': len(self.callbacks[callback_type][caller_class]) }
            self.callbacks[callback_type][caller_class].append(block_config)