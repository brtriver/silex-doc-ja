エクステンション (Extensions)
==========

Silex はエクステンションのためのインターフェースを提供しています。
エクステンションはアプリケーション上にサービスとして定義します。

エクステンションの読み込み
------------------

エクステンションを読み込んで使うためには、アプリケーションにそのエクステンションを登録しなければなりません ::

    $app = new Silex\Application();

    $app->register(new Acme\DatabaseExtension());

第２引数としてパラメーターを提供することもできます。
この作業はエクステンションが登録される **前** に行う必要があります。

::

    $app->register(new Acme\DatabaseExtension(), array(
        'database.dsn'      => 'mysql:host=localhost;dbname=myapp',
        'database.user'     => 'root',
        'database.password' => 'secret_root_password',
    ));

規約
-----------

エクステンションとやりとりするときにどのような順序でやりとりを行うかを知っておく必要があります。
以下に説明するルールに従うだけです:

* (オートローダーのための) クラスへのパスはエクステンションが登録される **前** に定義しなければなりません。
  パスは``Application::register`` の第２引数として渡してください。
  なぜなら渡されたパラメーターを最初にセットするからです。
  
  *理由: エクステンションは、自身が登録されるときにオートローダーを設定しようとします。
  もしこの時点でクラスのパスが渡されていなければオートローダーを登録することができないからです。*

* エクステンションのサービスを上書き処理はエクステンションが登録された *後* にしなくてはなりません。

  *理由: サービスがすでに存在していると、エクステンションはそれを上書きしようとするからです。*

* サービスがアクセスされる前のタイミングであればパラメーターをセットすることができます。

あなたのオリジナルのエクステンションを作成するときはこの振る舞いに注意してください。

エクステンションの読み込み
-------------------

標準で用意されているエクステンションは以下の通りです。
これらすべてのエクステンションの名前空間は ``Silex\Extension`` になります。

* :doc:`DoctrineExtension <extensions/doctrine>`
* :doc:`MonologExtension <extensions/monolog>`
* :doc:HttpCacheExtension
==================

*HttpCacheExtension* で Symfony2 のリバースプロキシーを利用することができます。

パラメーター
----------

* **http_cache.cache_dir**: HTTP のキャッシュデータを保存するためのキャッシュディレクトリ

* **http_cache.options** (オプション): `HttpCache
  <http://api.symfony.com/2.0/Symfony/Component/HttpKernel/HttpCache/HttpCache.html>`_
  コンストラクターのためのオプションを配列

サービス
--------

* **http_cache**: `HttpCache
  <http://api.symfony.com/2.0/Symfony/Component/HttpKernel/HttpCache/HttpCache.html>`_,
  インスタンス

登録
-----------

::

    $app->register(new Silex\Extension\HttpCacheExtension(), array(
        'cache_dir' => __DIR__.'/cache/',
    ));

使い方
-----

Silex は レスポンス HTTP ヘッダーを設定することで Vanish のようなリバースプロキシーを利用することができます::

    $app->get('/', function() {
        return new Response('Foo', 200, array(
            'Cache-Control' => 's-maxage=5',
        ));
    });

このエクステンションを `http_cache` サービスをリクエストにハンドルし使うことで Silex アプリケーションで Symfony2 のリバースプロクシーを使うことができます::

    $app['http_cache']->handle($request)->send();

また、エクステンションは `ESI
<http://www.doctrine-project.org/docs/dbal/2.0/en/>`_ もサポートしています::

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

より詳細については、 `Symfony2 HTTP キャッシュについてのドキュメント
    <http://symfony.com/doc/current/book/http_cache.html>`_ を参照してください。
`SessionExtension <extensions/session>`
* :doc:`TwigExtension <extensions/twig>`
* :doc:`TranslationExtension <extensions/translation>`
* :doc:`UrlGeneratorExtension <extensions/url_generator>`
* :doc:`ValidatorExtension <extensions/validator>`
* :doc:`HttpCacheExtension <extensions/http_cache>`

エクステンションの作成
---------------------

エクステンションは ``Silex\ExtensionInterface`` を実装しなければなりません。

::

    interface ExtensionInterface
    {
        function register(Application $app);
    }

これはとても単純な利用例であり、 ``register`` メソッドを実装しているだけの新しいクラスを作成しているだけです。
このメソッドで、他のサービスやパラメータを利用するようなアプリケーション上にサービスを定義することができます。

次がそのようなエクステンションのサンプルです::

    namespace Acme;

    use Silex\Application;
    use Silex\ExtensionInterface;

    class HelloExtension implements ExtensionInterface
    {
        public function register(Application $app)
        {
            $app['hello'] = $app->protect(function ($name) use ($app) {
                $default = ($app['hello.default_name']) ? $app['hello.default_name'] : '';
                $name = $name ?: $default;
                return "Hello $name";
            });
        }
    }

このクラスは ``hello`` サービスを提供します。このサービスは保護されたクロージャーです。
$name を引数としてとり、 ``hello.default_name`` を返してくれます。
初期値を与えられていない場合は空の文字列を使います。

このエクステンションは次のように使うことができます::

    $app = new Silex\Application();

    $app->register(new Acme\HelloExtension(), array(
        'hello.default_name' => 'Igor',
    ));

    $app->get('/hello', function () use ($app) {
        $name = $app['request']->get('name');
        return $app['hello']($name);
    });

このサンプルでは ``name``　パラメーターの値をクエリーストリングから取得しています。
そのため ``/hello?name=Fabien`` のようなパスでリクエストします。

クラスの読み込み (Class loading)
~~~~~~~~~~~~~

``MonologExtension`` や ``TwigExtension`` を見てもらえばわかるように、エクステンションは外部ライブラリを簡単に利用できる仕組みです。
ごく普通のライブラリで、 `PSR-0 Naming Standard <http://groups.google.com/group/php-standards/web/psr-0-final-proposal>`_
やPEARの命名ルールに準拠しているのであれば、 ``UniversalClassLoader`` を使ったクラスの自動読み込みが可能です。

*Services* の章で説明したように、 *autoloader* サービスによってこのようなクラスの自動読み込みが行われます。

では、この自動読み込みをどのように使うかを見てみましょう。 (ここでは `Buzz <https://github.com/kriswallsmith/Buzz>`_ をライブラリとして読み込みます)::

    namespace Acme;

    use Silex\Application;
    use Silex\ExtensionInterface;

    class BuzzExtension implements ExtensionInterface
    {
        public function register(Application $app)
        {
            $app['buzz'] = $app->share(function () { ... });

            if (isset($app['buzz.class_path'])) {
                $app['autoloader']->registerNamespace('Buzz', $app['buzz.class_path']);
            }
        }
    }

次のようにエクステンションを登録するときにオプションで渡すことで簡単にクラスのパスを追加することができます::

    $app->register(new BuzzExtension(), array(
        'buzz.class_path' => __DIR__.'/vendor/buzz/lib',
    ));

.. note::

    PHP 5.3 の名前空間を使っていないライブラリの場合は ``registerNamespace`` の代わりに ``registerPrefix`` を使うことができます。
    こうすることでディレクトリの区切り記号としてアンダースコアーを使うことができます。