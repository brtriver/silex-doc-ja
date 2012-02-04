HttpCacheServiceProvider
=============================

*HttpCacheServiceProvider* で Symfony2 のリバースプロキシー をサポートすることができます。

パラメーター
------------

* **http_cache.cache_dir**: HTTP キャッシュデータを保存するディレクトリ。

* **http_cache.options** (オプション): `HttpCache
  <http://api.symfony.com/2.0/Symfony/Component/HttpKernel/HttpCache/HttpCache.html>`_
  コンストラクタのためのオプションの配列。

サービス
--------

* **http_cache**: `HttpCache
  <http://api.symfony.com/2.0/Symfony/Component/HttpKernel/HttpCache/HttpCache.html>`_
  のインスタンス

登録
-----------

::

    $app->register(new Silex\Provider\HttpCacheServiceProvider(), array(
        'http_cache.cache_dir' => __DIR__.'/cache/',
    ));

使い方
-------

Silex は標準で HTTP キャッシュヘッダーを返すように設定することで Vanish のようなリバースプロクシーをサポートしています:: 

    $app->get('/', function() {
        return new Response('Foo', 200, array(
            'Cache-Control' => 's-maxage=5',
        ));
    });

このプロバイダー使い Silex のアプリケーションはリクエストを操作するために `http_cache` サービスを追加することで Symfony2 のリバースプロクシーを使うことができるようになります。::

    $app['http_cache']->handle($request)->send();

このプロバイダー ESI もサポートしています。::

    $app->get('/', function() {
        return new Response(<<<EOF
    <html>
        <body>
            Hello
            <esi:include src="/included" />
        </body>
    </html>

    EOF
        , 200, array(
            'Cache-Control' => 's-maxage=20',
            'Surrogate-Control' => 'content="ESI/1.0"',
        ));
    });

    $app->get('/included', function() {
        return new Response('Foo', 200, array(
            'Cache-Control' => 's-maxage=5',
        ));
    });

    $app['http_cache']->handle($request)->send();

詳細については、 `Symfony2 HTTP キャッシュのドキュメント 
<http://symfony.com/doc/current/book/http_cache.html>`_
を参照してください。
