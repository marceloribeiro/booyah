from booyah.extensions.string import *
class TestClass():
    pass

class TestStringExtension():
    def test_reverse(self):
        assert String('hello').reverse() == 'olleh'

    def test_constantize(self):
        assert String('TestClass').constantize(globals()) == TestClass

    def test_camelize(self):
        assert String('hello_world').camelize() == 'HelloWorld'
        assert String('HelloWorld').camelize() == 'HelloWorld'
        assert String('Helloworld').camelize() == 'Helloworld'
        assert String('Hello World').camelize() == 'Hello World'
        assert String('Hello world').camelize() == 'Hello world'

    def test_dasherize(self):
        assert String('hello_world').dasherize() == 'hello-world'
        assert String('HelloWorld').dasherize() == 'HelloWorld'
        assert String('Helloworld').dasherize() == 'Helloworld'
        assert String('Hello World').dasherize() == 'Hello World'
        assert String('Hello world').dasherize() == 'Hello world'

    def test_humanize(self):
        assert String('hello_world').humanize() == 'Hello world'
        assert String('HelloWorld').humanize() == 'Helloworld'
        assert String('Helloworld').humanize() == 'Helloworld'
        assert String('Hello World').humanize() == 'Hello world'
        assert String('Hello world').humanize() == 'Hello world'

    def test_parameterize(self):
        assert String("Donald E. Knuth").parameterize() == 'donald-e-knuth'

    def test_pluralize(self):
        assert String('hello_world').pluralize() == 'hello_worlds'
        assert String('HelloWorld').pluralize() == 'HelloWorlds'
        assert String('Helloworld').pluralize() == 'Helloworlds'
        assert String('Hello World').pluralize() == 'Hello Worlds'
        assert String('Hello world').pluralize() == 'Hello worlds'
        assert String('posts').pluralize() == 'posts'
        assert String('octopus').pluralize() == 'octopi'
        assert String('sheep').pluralize() == 'sheep'
        assert String('CamelOctopus').pluralize() == 'CamelOctopi'
        assert String('hash').pluralize() == 'hashes'
        assert String('search').pluralize() == 'searches'

    def test_singularize(self):
        assert String('hello_worlds').singularize() == 'hello_world'
        assert String('HelloWorlds').singularize() == 'HelloWorld'
        assert String('Helloworlds').singularize() == 'Helloworld'
        assert String('Hello Worlds').singularize() == 'Hello World'
        assert String('Hello worlds').singularize() == 'Hello world'
        assert String('posts').singularize() == 'post'
        assert String('octopi').singularize() == 'octopus'
        assert String('sheep').singularize() == 'sheep'
        assert String('CamelOctopi').singularize() == 'CamelOctopus'
        assert String('hashes').singularize() == 'hash'
        assert String('searches').singularize() == 'search'

    def test_tableize(self):
        assert String('RawScaledScorer').tableize() == 'raw_scaled_scorers'
        assert String('egg_and_ham').tableize() == 'egg_and_hams'
        assert String('fancyCategory').tableize() == 'fancy_categories'

    def test_titleize(self):
        assert String('man from the boondocks').titleize() == 'Man From The Boondocks'
        assert String('x-men: the last stand').titleize() == 'X Men: The Last Stand'
        assert String('TheManWithoutAPast').titleize() == 'The Man Without A Past'
        assert String('raiders_of_the_lost_ark').titleize() == 'Raiders Of The Lost Ark'

    def test_transliterate(self):
        assert String('älämölö').transliterate() == 'alamolo'
        assert String('Ærøskøbing').transliterate() == 'rskbing'

    def test_underscore(self):
        assert String('DeviceType').underscore() == 'device_type'
        assert String('IOError').underscore() == 'io_error'
        assert String('DeviceType is funny').underscore() == 'device_type_is_funny'
        assert String(' my name ').underscore() == 'my_name'
        assert String(' my  Name ').underscore() == 'my_name'

    def test_classify(self):
        assert String('MyClasses').classify() == 'MyClass'
        assert String('my classes').classify() == 'MyClass'
        assert String('my_classes').classify() == 'MyClass'
        assert String('my_class').classify() == 'MyClass'
        assert String('älämölö').classify() == 'Alamolo'