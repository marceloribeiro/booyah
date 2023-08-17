from py_dotenv import read_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)
print('Spinning up environment [' + os.getenv('BOOYAH_ENV') + ']')

from lib.router.application_router import ApplicationRouter
from config.routes import ApplicationRoutes


def application(environment, start_response):
    ApplicationRoutes.load_routes()
    router = ApplicationRouter.get_instance()
    response = router.respond(environment)
    response_body = response.response_body()

    start_response(response.status, response.response_headers())
    return iter([response_body])