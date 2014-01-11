HttpCacheServiceProvider
=============================

*HttpCacheServiceProvider* で Symfony2 のリバースプロクシー をサポートすることができます。

パラメーター
------------

* **http_cache.cache_dir**: HTTP キャッシュデータを保存するディレクトリ。

* **http_cache.options** (オプション): `HttpCache
  <http://api.symfony.com/master/Symfony/Component/HttpKernel/HttpCache/HttpCache.html>`_
  コンストラクタのためのオプションの配列。

サービス
--------

* **http_cache**: `HttpCache
  <http://api.symfony.com/master/Symfony/Component/HttpKernel/HttpCache/HttpCache.html>`_
  のインスタンス

* **http_cache.esi**: リクエストとレスポンスに対してESI 機能を持った `Esi
  <http://api.symfony.com/master/Symfony/Component/HttpKernel/HttpCache/Esi.html>`_ のインスタンス

* **http_cache.store**: リクエストとレスポンスヘッダーに関するメタデータを保存する仕組みを実装した `Store
  <http://api.symfony.com/master/Symfony/Component/HttpKernel/HttpCache/Store.html>`_ のインスタンス。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\HttpCacheServiceProvider(), array(
        'http_cache.cache_dir' => __DIR__.'/cache/',
    ));


使い方
-------

Silex は標準で HTTP キャッシュヘッダーを返すように設定することで Vanish のようなリバースプロクシーをサポートしています。 :: 

    use Symfony\Component\HttpFoundation\Response;

    $app->get('/', function() {
        return new Response('Foo', 200, array(
            'Cache-Control' => 's-maxage=5',
        ));
    });

.. tip::

    Silexに$ipというアドレスからのリバースプロクシからの ``X-Forwarded-For*`` ヘッダを信用させたい場合、 `Trusting Proxies <http://symfony.com/doc/current/components/http_foundation/trusting_proxies.html>`_ に記述されているような形式でホワイトリストを作成する必要があります。

        Varnishを同一マシン上で起動させている場合の例
        
    .. code-block:: php
     
        use Symfony\Component\HttpFoundation\Request;
        
        Request::setTrustedProxies(array('127.0.0.1', '::1'));
        $app->run();
 
このプロバイダーは ``http_cache`` サービスを用いることで、Symfony2リバースプロクシをSilexアプリケーション上で使用可能にします。Symfony2リバースプロクシは他のプロクシと同じように動作するのでホワイトリストにしたいと思うでしょう。

.. code-block:: php
 
    use Symfony\Component\HttpFoundation\Request;
     
    Request::setTrustedProxies(array('127.0.0.1'));
    $app['http_cache']->run();
 
このプロバイダーはESIもサポートしています。::

    $app->get('/', function() {
        $response = new Response(<<<EOF
    <html>
        <body>
            Hello
            <esi:include src="/included" />
        </body>
    </html>

    EOF
        , 200, array(
            'Surrogate-Control' => 'content="ESI/1.0"',
        ));

        $response->setTtl(20);

        return $response;
    });

    $app->get('/included', function() {
        $response = new Response('Foo');
        $response->setTtl(5);

        return $response;
    });

    $app['http_cache']->run();

ESIを使わない場合、パフォーマンスを少し上げるために無効にすることが出来ます。 ::

    $app->register(new Silex\Provider\HttpCacheServiceProvider(), array(
       'http_cache.cache_dir' => __DIR__.'/cache/',
       'http_cache.esi'       => null,
    ));

.. tip::

    キャッシュの問題をデバッグするにはアプリケーションの ``debug`` をtrueにしてください。
    Symfonyは自動的にキャッシュヒットやミスに関する情報を持った ``X-Symfony-Cache`` ヘッダを全てのレスポンスに追加します。

    もしSymfony Sessionプロバイダーを使って *いない* 場合、
    PHPの標準の振舞を回避するために ``session.cash_limiter`` をからの値に設定したほうが良いです。

    最後に、あなたのウェブサーバーがキャッシュ戦略を上書きしないかどうか確認して下さい。

詳細については、 `Symfony2 HTTP キャッシュのドキュメント 
<http://symfony.com/doc/current/book/http_cache.html>`_
を参照してください。
