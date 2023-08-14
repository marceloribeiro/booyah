from lib.application.application_router import ApplicationRouter
from config.routes import ApplicationRoutes

def application(environment, start_response):
    ApplicationRoutes.load_routes()
    router = ApplicationRouter.get_instance()
    response = router.respond(environment)
    response_body = response.response_body()

    start_response(response.status, response.response_headers())
    return iter([response_body])