from booyah.router.routes_manager import RoutesManager

routes_manager = RoutesManager()
routes_manager.resources('users', 'booyah.controllers')

routes_manager.get('/plain', 'plain_path', 'booyah.controllers.home#plain', 'text')
routes_manager.get('/status', 'status_path', "booyah.controllers.home#status", "json")
routes_manager.get('/about', 'about_path', "booyah.controllers.home#about")
routes_manager.get('/', 'home_path', "booyah.controllers.home#index")

routes = routes_manager.routes