UrlGeneratorServiceProvider
=============================

*UrlGeneratorServiceProvider* は名前ルーティングのためにURLを生成するためのサービスです。

パラメーター
------------

無し。

サービス
--------

* **url_generator**: ``routes`` サービスを通して提供されている 
    `RouteCollection <http://api.symfony.com/master/Symfony/Component/Routing/RouteCollection.html>`_ 
    を使う `UrlGenerator
    <http://api.symfony.com/master/Symfony/Component/Routing/Generator/UrlGenerator.html>`_
    のインスタンスです。 ``generate`` メソッドが存在していて、このメソッドは引数としてルーティング名と、ルーティングパラメータの配列を必要とします。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\UrlGeneratorServiceProvider());

使い方
------

UrlGenerator プロバイダーは ``url_generator`` サービスを提供します。 ::

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

Twigを使っている場合、サービスを以下のように使用することもできます。

.. code-block:: jinja

    {{ app.url_generator.generate('homepage') }}

さらに ``composer.json`` に ``twig-bridge`` がある場合、 ``path()`` と ``url()`` 関数がテンプレート中で使用可能です。

.. code-block:: jinja

    {{ path('homepage') }}
    {{ url('homepage') }} {# 絶対URL http://example.org/ の生成 #}
    {{ path('hello', {name: 'Fabien'}) }}
    {{ url('hello', {name: 'Fabien'}) }} {# 絶対URL http://example.org/hello/Fabien の生成 #}

トレイト
---------

``Silex\Application\UrlGeneratorTrait`` は以下のショートカットを追加します。

* **path**: パスを生成します。

* **url**: 絶対URLを生成します。

.. code-block:: php

    $app->path('homepage');
    $app->url('homepage');
