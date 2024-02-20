from booyah.extensions.string import String
from booyah.framework import Booyah

class RoutesManager:
    def __init__(self):
        self.routes = []
    
    def put_controller_suffix(self, full_path):
        parts = full_path.split('#')
        if len(parts) == 2:
            controller_name, action_name = parts
            return f"{controller_name}_controller#{action_name}"
        else:
            raise ValueError("Invalid input string format")
    
    def append_route(self, method, url, name, to, controller, action, format):
        if format == None:
            if Booyah.is_api:
                format = 'json'
            else:
                format = '*'
        action_path = to
        if controller and action:
            action_path = f"{controller}#{action}"

        if action_path and url and method and format:
            self.routes.append({
                "method": method,
                "url": url,
                "name": name,
                "action": self.put_controller_suffix(action_path),
                "format": format
            })
        return self

    def get(self, url, name=None, to=None, controller=None, action=None, format=None):
        return self.append_route('GET', url, name, to, controller, action, format)

    def post(self, url, name=None, to=None, controller=None, action=None, format=None):
        return self.append_route('POST', url, name, to, controller, action, format)

    def put(self, url, name=None, to=None, controller=None, action=None, format=None):
        return self.append_route('PUT', url, name, to, controller, action, format)

    def patch(self, url, name=None, to=None, controller=None, action=None, format=None):
        return self.append_route('PATCH', url, name, to, controller, action, format)

    def delete(self, url, name=None, to=None, controller=None, action=None, format=None):
        return self.append_route('DELETE', url, name, to, controller, action, format)

    def resources(self, resource_name, parent_module=None, parent=None, only=None, except_=None, format='*'):
        name_prefix = String(resource_name).singularize()
        base_path = f'{parent}/{resource_name}' if parent else f'/{resource_name}'
        controller_path = f'{parent_module}.{resource_name}_controller' if parent_module else f'{resource_name}_controller'
        
        if Booyah.is_api:
            standard_routes = [
                {"method": 'GET',       "url": base_path,                   "name": f'{name_prefix}_index',     "action": f'{controller_path}#index',   "format": format},
                {"method": 'GET',       "url": f'{base_path}/<int:id>',     "name": f'{name_prefix}_show',      "action": f'{controller_path}#show',    "format": format},
                {"method": 'POST',      "url": base_path,                   "name": f'{name_prefix}_create',    "action": f'{controller_path}#create',  "format": format},
                {"method": 'PUT',       "url": f'{base_path}/<int:id>',     "name": f'{name_prefix}_update',    "action": f'{controller_path}#update',  "format": format},
                {"method": 'PATCH',     "url": f'{base_path}/<int:id>',     "name": f'{name_prefix}_update',    "action": f'{controller_path}#update',  "format": format},
                {"method": 'DELETE',    "url": f'{base_path}/<int:id>',     "name": f'{name_prefix}_destroy',   "action": f'{controller_path}#destroy', "format": format}
            ]
        else:
            standard_routes = [
                {"method": 'GET',       "url": base_path,                   "name": f'{name_prefix}_index',     "action": f'{controller_path}#index',   "format": format},
                {"method": 'GET',       "url": f'{base_path}/<int:id>',     "name": f'{name_prefix}_show',      "action": f'{controller_path}#show',    "format": format},
                {"method": 'GET',       "url": f'{base_path}/new',          "name": f'{name_prefix}_new',       "action": f'{controller_path}#new',     "format": format},
                {"method": 'POST',      "url": base_path,                   "name": f'{name_prefix}_create',    "action": f'{controller_path}#create',  "format": format},
                {"method": 'GET',       "url": f'{base_path}/<int:id>/edit',"name": f'{name_prefix}_edit',      "action": f'{controller_path}#edit',    "format": format},
                {"method": 'PUT',       "url": f'{base_path}/<int:id>',     "name": f'{name_prefix}_update',    "action": f'{controller_path}#update',  "format": format},
                {"method": 'PATCH',     "url": f'{base_path}/<int:id>',     "name": f'{name_prefix}_update',    "action": f'{controller_path}#update',  "format": format},
                {"method": 'DELETE',    "url": f'{base_path}/<int:id>',     "name": f'{name_prefix}_destroy',   "action": f'{controller_path}#destroy', "format": format}
            ]
        if only is not None:
            self.routes.extend([(method, path, callback) for method, path, callback in standard_routes if method in only])
        elif except_ is not None:
            self.routes.extend([(method, path, callback) for method, path, callback in standard_routes if method not in except_])
        else:
            self.routes.extend(standard_routes)
        
        return self