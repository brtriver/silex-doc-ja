Changelog
=========

このチェンジログはすべての後方互換性がない部分について説明しています:

* **2012-01-02**: Introduced support for streaming responses.

* **2011-09-22**: ``ExtensionInterface`` has been renamed to
  ``ServiceProviderInterface``. All built-in extensions have been renamed
  accordingly (for instance, ``Silex\Extension\TwigExtension`` has been
  renamed to ``Silex\Provider\TwigServiceProvider``)

* **2011-09-22**: The way reusable applications work has changed. The
  ``mount()`` method now takes an instance of ``ControllerCollection`` instead
  of an ``Application`` one.

    Before::

        $app = new Application();
        $app->get('/bar', function() { return 'foo'; });

        return $app;

    After::

        $app = new ControllerCollection();
        $app->get('/bar', function() { return 'foo'; });

        return $app;

* **2011-08-08**: The controller method configuration is now done on the Controller itself

    Before::

        $app->match('/', function () { echo 'foo'; }, 'GET|POST');

    After::

        $app->match('/', function () { echo 'foo'; })->method('GET|POST');
