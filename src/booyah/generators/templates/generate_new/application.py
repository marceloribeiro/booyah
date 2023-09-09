from py_dotenv import read_dotenv
import os
from booyah.extensions.string import String

os.environ["ROOT_PROJECT_PATH"] = os.getcwd()
os.environ["ROOT_PROJECT"] = os.path.basename(os.getcwd())
os.environ["PROJECT_NAME"] = String(os.environ["ROOT_PROJECT"]).titleize()
read_dotenv('.env')
print('Spinning up environment [' + os.getenv('BOOYAH_ENV') + ']')

from booyah.router.application_router import ApplicationRouter
from booyah.router.application_routes import ApplicationRoutes

def application(environment, start_response):
    ApplicationRoutes.load_routes()
    router = ApplicationRouter.get_instance()
    response = router.respond(environment)
    response_body = response.response_body()

    start_response(response.status, response.response_headers())
    return iter([response_body])