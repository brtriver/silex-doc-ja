UrlGeneratorExtension
=====================

*UrlGeneratorExtension* は名前ルーティングのためにURLを生成するためのサービスです。

パラメーター
------------

無し。

サービス
--------

* **url_generator**: ``routes`` サービスを通して提供されている 
    `RouteCollection <http://api.symfony.com/2.0/Symfony/Component/Routing/RouteCollection.html>`_ 
    を使う `UrlGenerator
    <http://api.symfony.com/2.0/Symfony/Component/Routing/Generator/UrlGenerator.html>`_
    のインスタンス。 ``generate`` メソッドが存在して、このメソッドは引数としてルーティング名と、ルーティングパラメータの配列を必要とします。

登録
-----------

::

    $app->register(new Silex\Extension\UrlGeneratorExtension());

使い方
------

UrlGenerator エクステンションは ``url_generator`` サービスを提供します。

::

    $app->get('/', function () {
        return 'welcome to the homepage';
    })
    ->bind('homepage');

    $app->get('/hello/{name}', function ($name) {
        return "Hello $name!";
    })
    ->bind('hello');

    $app->get('/navigation', function () use ($app) {
        return '<a href="'.$app['url_generator']->generate('homepage').'">Home</a>'.
               ' | '.
               '<a href="'.$app['url_generator']->generate('hello', array('name' => 'Igor')).'">Hello Igor</a>';
    });
