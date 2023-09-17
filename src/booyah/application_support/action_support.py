class ActionSupport:
    before_action_blocks = {}
    after_action_blocks  = {}
    around_action_blocks = {}

    @classmethod
    def initialize_action_configs(self, block_collection, block):
        if block not in block_collection:
            block_collection[block] = {"only_for": [], "except_for": []}

    @classmethod
    def add_action_configs(self, block_collection, block, only_for=None, except_for=None):
        self.initialize_action_configs(block_collection, block)
        if only_for:
            try:
              block_collection[block]['only_for'].extend(only_for)
            except:
              pass
        if except_for:
            try:
              block_collection[block]['except_for'].extend(except_for)
            except:
              pass

    @classmethod
    def remove_action_configs(self, block_collection, block, only_for=None, except_for=None):
        if only_for:
            try:
              block_collection[block]['except_for'].extend(only_for)
            except:
              pass
        if except_for:
            try:
              block_collection[block]['only_for'].extend(except_for)
            except:
              pass
        if not only_for and not except_for:
            del block_collection[block]

    @classmethod
    def add_before_action(self, block, only_for=None, except_for=None):
        self.add_action_configs(self.before_action_blocks, block, only_for, except_for)

    @classmethod
    def remove_before_action(self, block, only_for=None, except_for=None):
        self.remove_action_configs(self.before_action_blocks, block, only_for, except_for)

    @classmethod
    def add_after_action(self, block, only_for=None, except_for=None):
        self.add_action_configs(self.after_action_blocks, block, only_for, except_for)

    @classmethod
    def remove_after_action(self, block, only_for=None, except_for=None):
        self.remove_action_configs(self.after_action_blocks, block, only_for, except_for)

    @classmethod
    def add_around_action(self, block, only_for=None, except_for=None):
        self.add_action_configs(self.around_action_blocks, block, only_for, except_for)

    @classmethod
    def remove_around_action(self, block, only_for=None, except_for=None):
        self.remove_action_configs(self.around_action_blocks, block, only_for, except_for)

    def get_action(self, action):
        return getattr(self, action)

    def run_action(self, action):
        action_name = str(action).split(' ')[2].split('.')[1]
        self.before_action(action_name)
        if self.around_action_blocks:
            self.around_action(action, action_name)
        else:
            action()
        self.after_action(action_name)
        return self.application_response

    def should_run_block(self, block, action_name):
        if block['only_for'] and action_name not in block['only_for']:
            return False
        if block['except_for'] and action_name in block['except_for']:
            return False
        return True

    def before_action(self, action_name):
        for block in self.__class__.before_action_blocks:
            config = self.__class__.before_action_blocks[block]
            if self.should_run_block(config, action_name):
                if type(block) == str:
                    block = getattr(self, block)
                block()

    def after_action(self, action_name):
        for block in self.__class__.after_action_blocks:
            config = self.__class__.after_action_blocks[block]
            if self.should_run_block(config, action_name):
                if type(block) == str:
                    block = getattr(self, block)
                block()

    def around_action(self, action, action_name):
        for block in self.__class__.around_action_blocks:
            config = self.__class__.around_action_blocks[block]
            if self.should_run_block(config, action_name):
                if type(block) == str:
                    block = getattr(self, block)
                block(action)
            else:
                action()