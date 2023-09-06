from booyah.router.routes_manager import RoutesManager

routes_manager = RoutesManager()
routes = routes_manager.routes

routes_manager.get('/plain',    name='plain_path',  to='booyah.controllers.home#plain', format='text')
routes_manager.get('/status',   name='status_path', controller='booyah.controllers.home', action="status", format="json")
routes_manager.get('/about',    name='about_path',  to="booyah.controllers.home#about")
routes_manager.get('/',         name='home_path',   to="booyah.controllers.home#index")
