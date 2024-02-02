### Booyah MVC Architecture

**1. Controllers and Actions**

Booyah controllers are classes defined by <CONTROLLER_NAME>Controller, and methods that work as actions, which are mapped via the routes file.

```
class BlogsController:

  def index:
    # Fetch records

  def show:
    # Fetch single record
```

**2. Hooks / Callback Methods**

Booyah has built-in support for hooks / callback methods that are called `before`, `after` and `around` actions:


```
class BlogsController:
  before_action('authenticate_user')

  def index:
    # render the blog posts

  def authenticate_user:
    # make sure the user is authenticated or return the error
```

`before_action`, `after_action` and `around_action` calls also support configurations for specific actions:

```
class CartsController:
  before_action('authenticate_user', only_for=['checkout']

  def create:
    # creates a new shopping cart

  def checkout:
    # checks out the cart to become a new order
```

Alternatively, you can also skip before_action that has been setup on a parent controller class (like ApplicationController for example)

```
class CartsController:
  skip_before_action('authenticate_user', except_for=['checkout']

  def create:
    # creates a new shopping cart

  def checkout:
    # checks out the cart to become a new order
```

**3. Session and Cookies**

By default the session storage is in the database, with a table named session_storage. You can access cookies dict and you can access/change session dict in controller as following:

```
class HomeController(BooyahApplicationController):
  def index(self):
    self.session['user_name'] = 'Session user name'
    return self.render({'cookies': str(self.cookies()), 'session': str(self.session)})
```

While cookies have some settings like secure, path, expires, etc., you can use the cookies_manager to set a cookie or to get the full cookie setting:

```
from booyah.cookies.cookies_manager import cookies_manager

class HomeController(BooyahApplicationController):
  def index(self):
    cookies_manager.set_cookie(
      'new_cookie',
      'New cookie value here',
      secure=True,
      http_only=True
    )
    return self.render({'cookies': str(self.cookies()), 'session': str(self.session)})
```

**4. Flash Messages**

Flash messages are a mechanism that allow for notice/information being sent back to the user. You can use flash messages to display a message only once.

The flash message supports current rendering, but also rendering after redirects.

The following code blocks demonstrate how you can use flash in your project.

- Flash notices within the current rendering

```
class HomeController(BooyahApplicationController):
  def index(self):
    self.flash.now['notice'] = 'Message from index page'
    # any extra code you may need before view is rendered
```

- Flash notices within redirects:

```
class HomeController(BooyahApplicationController):
  def status(self):
    self.flash['non_default_flash'] = 'That should be handled by yourself'
    return self.redirect('/', notice='This is a notice from redirect', error='This is an error from redirect')
```

The above example demonstrates how Booyah supports some default flash keys so you can use them within your redirect call. They are `notice`, `error`, `warning`, `info`, `success`.

Here is how you access the flash from the booyah view templates:

```
<div class="flash-message non_default_flash">{{flash['non_default_flash']}}</div>
```

