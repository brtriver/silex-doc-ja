プロバイダー (Providers)
=================================

プロバイダーは、開発者が、アプリケーションの一部を他のアプリケーションでも再利用できるようにします。 Silex は２つのインタフェースによって定義された二種類のプロバイダーを提供しています。１つは、サービスのためのインタフェースで、 ServiceProviderInterfaceで、もう１つは、コントローラーのためのインタフェースで、 ControllerProviderInterface です。

サービスプロバイダー (Service Providers)
-----------------

プロバイダーの読み込み (Loading extensions)
~~~~~~~~~~~~~~~~~

プロバイダーを読み込んで使うためには、アプリケーションにそのプロバイダーを登録しなければなりません::

    $app = new Silex\Application();

    $app->register(new Acme\DatabaseServiceProvider());

第２引数としてパラメーターを提供することもできます。
この作業はエクステンションが登録される **前** に行う必要があります::

    $app->register(new Acme\DatabaseServiceProvider(), array(
        'database.dsn'      => 'mysql:host=localhost;dbname=myapp',
        'database.user'     => 'root',
        'database.password' => 'secret_root_password',
    ));

規約
-----------

プロバイダーとやりとりするときにどのような順序でやりとりを行うかを知っておく必要があります。
以下に説明するルールに従うだけです:

* (オートローダーのための) クラスへのパスはプロバイダーが登録される **前** に定義しなければなりません。
  パスは ``Application::register`` の第２引数として渡してください。
  なぜなら渡されたパラメーターを最初にセットするからです。
  
  *理由: プロバイダーは、自身が登録されるときにオートローダーを設定しようとします。
  もしこの時点でクラスのパスが渡されていなければオートローダーを登録することができないからです。*

* 既に存在しているサービスを上書き処理する場合はプロバイダーが登録された **後** にしなくてはなりません。

  *理由: サービスがすでに存在していると、プロバイダーはそれを上書きしようとするからです。*

* サービスがアクセスされる前のタイミングであればパラメーターをセットすることができます。

あなたのオリジナルのプロバイダーを作成するときはこの振る舞いに注意してください。

プロバイダーのインクルード
---------------------------

標準で用意されているプロバイダーは以下の通りです。
これらすべてのプロバイダーの名前空間は ``Silex\Provider`` になります。

* :doc:`DoctrineServiceProvider <providers/doctrine>`
* :doc:`MonologServiceProvider <providers/monolog>`
* :doc:`SessionServiceProvider <providers/session>`
* :doc:`SwiftMailerServiceProvider <providers/swiftmailer>`
* :doc:`SymfonyBridgesServiceProvider <providers/symfony_bridges>`
* :doc:`TwigServiceProvider <providers/twig>`
* :doc:`TranslationServiceProvider <providers/translation>`
* :doc:`UrlGeneratorServiceProvider <providers/url_generator>`
* :doc:`ValidatorServiceProvider <providers/validator>`
* :doc:`HttpCacheServiceProvider <providers/http_cache>`

プロバイダーの作成
----------------------

プロバイダーは ``Silex\ServiceProviderInterface`` を実装しなければなりません::

    interface ServiceProviderInterface
    {
        function register(Application $app);
    }

これはとても単純な利用例であり、 ``register`` メソッドを実装している新しいクラスを作成しているだけです。
このメソッドで、他のサービスやパラメータを利用するようなアプリケーション上にサービスを定義することができます。

次がそのようなプロバイダーのサンプルです::

    namespace Acme;

    use Silex\Application;
    use Silex\ServiceProviderInterface;

    class HelloServiceProvider implements ServiceProviderInterface
    {
        public function register(Application $app)
        {
            $app['hello'] = $app->protect(function ($name) use ($app) {
                $default = $app['hello.default_name'] ? $app['hello.default_name'] : '';
                $name = $name ?: $default;

                return 'Hello '.$app->escape($name);
            });
        }
    }

このクラスは ``hello`` サービスを提供します。このサービスは保護されたクロージャーです。
$name を引数として取り、 ``hello.default_name`` を返してくれます。
初期値を与えられていない場合は空の文字列を使います。

このプロバイダーは次のように使うことができます::

    $app = new Silex\Application();

    $app->register(new Acme\HelloServiceProvider(), array(
        'hello.default_name' => 'Igor',
    ));

    $app->get('/hello', function () use ($app) {
        $name = $app['request']->get('name');

        return $app['hello']($name);
    });

このサンプルでは ``name`` パラメーターの値をクエリーストリングから取得しています。
そのため ``/hello?name=Fabien`` のようなパスでリクエストします。

クラスの読み込み (Class loading)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``MonologServiceProvider`` や ``TwigServiceProvider`` を見てもらえばわかるように、プロバイダーは外部ライブラリを簡単に利用できる仕組みです。
ごく普通のライブラリで、 `PSR-0 Naming Standard <http://groups.google.com/group/php-standards/web/psr-0-final-proposal>`_
や PEAR の命名ルールに準拠しているのであれば、 ``UniversalClassLoader`` を使ったクラスの自動読み込みが可能です。

*Services* の章で説明したように、 *autoloader* サービスによってこのようなクラスの自動読み込みが行われます。

では、この自動読み込みをどのように使うかを見てみましょう。 (ここでは `Buzz <https://github.com/kriswallsmith/Buzz>`_ をライブラリとして読み込みます)::

    namespace Acme;

    use Silex\Application;
    use Silex\ServiceProviderInterface;

    class BuzzServiceProvider implements ServiceProviderInterface
    {
        public function register(Application $app)
        {
            $app['buzz'] = $app->share(function () { ... });

            if (isset($app['buzz.class_path'])) {
                $app['autoloader']->registerNamespace('Buzz', $app['buzz.class_path']);
            }
        }
    }

次のようにプロバイダーを登録するときにオプションで渡すことで簡単にクラスのパスを追加することができます::

    $app->register(new BuzzServiceProvider(), array(
        'buzz.class_path' => __DIR__.'/vendor/buzz/lib',
    ));

.. note::

    PHP 5.3 の名前空間を使っていないライブラリの場合は ``registerNamespace`` の代わりに ``registerPrefix`` を使うことができます。
    こうすることでディレクトリの区切り記号としてアンダースコアーを使うことができます。

コントロラープロバイダー(Controllers providers)
---------------------

プロバイダーの読み込み
~~~~~~~~~~~~~~~~~

プロバイダーを読み込んで使うためには、パスで指定したコントローラーを "mount" する必要があります::

    $app = new Silex\Application();

    $app->mount('/blog', new Acme\BlogControllerProvider());

プロバイダーで定義されている全てのコントローラーは、 `/blog` パス以下で使用可能です。

プロバイダーの作成
~~~~~~~~~~~~~~~~~~~

プロバイダーは ``Silex\ControllerProviderInterface`` を実装しなければなりません::

    interface ControllerProviderInterface
    {
        function connect(Application $app);
    }

次がそのようなプロバイダーのサンプルです::

    namespace Acme;

    use Silex\Application;
    use Silex\ControllerProviderInterface;
    use Silex\ControllerCollection;

    class HelloControllerProvider implements ControllerProviderInterface
    {
        public function connect(Application $app)
        {
            $controllers = new ControllerCollection();

            $controllers->get('/', function (Application $app) {
                return $app->redirect('/hello');
            });

            return $controllers;
        }
    }

``connect`` メソッドは、 ``ControllerCollection`` クラスのインスタンスを返さなければなりません。
``ControllerCollection`` は、``get``, ``post``,  ``match`` などのメソッドが定義されたコントローラーのクラスです。

.. tip::

    ``Application`` クラスは、実際はこれらのメソッドへのプロクシとして振る舞います。

これで以下のようにプロバイダーを使うことができます::

    $app = new Silex\Application();

    $app->mount('/blog', new Acme\HelloControllerProvider());

この例では、 ``/blog/`` のパスは、プロバイダーで定義されたコントローラーに結び付けられました。

.. tip::

    サービスプロバイダーインタフェースとコントローラープロバイダーインタフェースの両方を実装したプロバイダーも定義することができ、同じクラスでパッケージ化できます。
