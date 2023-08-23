import os
from booyah.controllers.application_controller import ApplicationController
from booyah.db.adapters.base_adapter import BaseAdapter
from booyah.models.user import User

class HomeController(ApplicationController):
    def index(self):
        return self.render({'text': 'Home Controller, Index Action'})

    def about(self):
        return self.render({'text': 'Home Controller, About Action'})

    def status(self):
        db_adapter = BaseAdapter.get_instance()

        return self.render({
            'environment': os.getenv('BOOYAH_ENV'),
            'adapter': db_adapter.__class__.__name__,
            'user_table': User.table_name(),
            'table_columns': User.get_table_columns()
        })

    def plain(self):
        return self.render({'text': 'Home Controller, Plain Action'})