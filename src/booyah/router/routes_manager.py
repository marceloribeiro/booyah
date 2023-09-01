from booyah.extensions.string import String

METHOD_INDEX = 0
URL_PATH_INDEX = 1
ROUTE_NAME_INDEX = 2
FULL_PATH_INDEX = 3
FORMAT_INDEX = 4

class RoutesManager:
    def __init__(self):
        self.routes = []

    def get(self, path, name, full_path, formats='*'):
        self.routes.append(('GET', path, name, full_path, formats))
        return self

    def post(self, path, name, full_path, formats='*'):
        self.routes.append(('POST', path, name, full_path, formats))
        return self

    def put(self, path, name, full_path, formats='*'):
        self.routes.append(('PUT', path, name, full_path, formats))
        return self

    def patch(self, path, name, full_path, formats='*'):
        self.routes.append(('PATCH', path, name, full_path, formats))
        return self

    def delete(self, path, name, full_path, formats='*'):
        self.routes.append(('DELETE', path, name, full_path, formats))
        return self

    def resources(self, resource_name, controller_module=None, parent=None, only=None, except_=None, formats='*'):
        name_prefix = String(resource_name).singularize()
        base_path = f'/{parent}/{resource_name}' if parent else f'/{resource_name}'
        controller_path = f'{controller_module}.{resource_name}_controller' if controller_module else f'{resource_name}_controller'
        
        standard_routes = [
            ('GET', base_path, f'{name_prefix}_index', f'{controller_path}#index', formats),
            ('GET', f'{base_path}/<int:id>', f'{name_prefix}_show', f'{controller_path}#show', formats),
            ('GET', f'{base_path}/new', f'{name_prefix}_new', f'{controller_path}#new', formats),
            ('POST', base_path, f'{name_prefix}_create', f'{controller_path}#create', formats),
            ('GET', f'{base_path}/<int:id>/edit', f'{name_prefix}_edit', f'{controller_path}#edit', formats),
            ('PUT', f'{base_path}/<int:id>', f'{name_prefix}_update', f'{controller_path}#update', formats),
            ('PATCH', f'{base_path}/<int:id>', f'{name_prefix}_update', f'{controller_path}#update', formats),
            ('DELETE', f'{base_path}/<int:id>', f'{name_prefix}_destroy', f'{controller_path}#destroy', formats)
        ]
        
        if only is not None:
            self.routes.extend([(method, path, callback) for method, path, callback in standard_routes if method in only])
        elif except_ is not None:
            self.routes.extend([(method, path, callback) for method, path, callback in standard_routes if method not in except_])
        else:
            self.routes.extend(standard_routes)
        
        return self