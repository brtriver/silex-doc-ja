プロバイダー (Providers)
=================================

プロバイダーは、開発者が、アプリケーションの一部を他のアプリケーションでも再利用できるようにします。 Silex は２つのインタフェースによって定義された二種類のプロバイダーを提供しています。１つは、サービスのためのインタフェース ``ServiceProviderInterface`` で、もう１つは、コントローラーのためのインタフェース  ``ControllerProviderInterface`` です。

サービスプロバイダー (Service Providers)
------------------------------------------

プロバイダーの読み込み (Loading extensions)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

プロバイダーを読み込んで使うためには、アプリケーションにそのプロバイダーを登録しなければなりません。 ::

    $app = new Silex\Application();

    $app->register(new Acme\DatabaseServiceProvider());

第２引数としてパラメーターを提供することもできます。
これはプロバイダーが登録された **後** かつ、起動する **前** に設定されます。 ::

    $app->register(new Acme\DatabaseServiceProvider(), array(
        'database.dsn'      => 'mysql:host=localhost;dbname=myapp',
        'database.user'     => 'root',
        'database.password' => 'secret_root_password',
    ));

規約 (Conventions)
------------------

プロバイダーとやりとりするときにどのような順序でやりとりを行うかを知っておく必要があります。
以下に説明するルールに従うだけです:

* 既に存在しているサービスを上書き処理する場合はプロバイダーが登録された **後** にしなくてはなりません。

  *理由: サービスがすでに存在していると、プロバイダーはそれを上書きしようとするからです。*

* プロバイダが登録された **後** で、サービスが実際にアクセスされる **前** のタイミングであればパラメーターを何度でもセットすることができます。

  *理由: サービスと同じようにプロバイダでも、パラメータの既存の値を上書きすることができるためです。*

あなたのオリジナルのプロバイダーを作成するときはこの振る舞いに注意してください。

プロバイダーのインクルード
---------------------------

標準で用意されているプロバイダーは以下の通りです。
これらすべてのプロバイダーの名前空間は ``Silex\Provider`` になります。

* :doc:`DoctrineServiceProvider <providers/doctrine>`
* :doc:`MonologServiceProvider <providers/monolog>`
* :doc:`SessionServiceProvider <providers/session>`
* :doc:`SerializerServiceProvider <providers/serializer>`
* :doc:`SwiftmailerServiceProvider <providers/swiftmailer>`
* :doc:`TwigServiceProvider <providers/twig>`
* :doc:`TranslationServiceProvider <providers/translation>`
* :doc:`UrlGeneratorServiceProvider <providers/url_generator>`
* :doc:`ValidatorServiceProvider <providers/validator>`
* :doc:`HttpCacheServiceProvider <providers/http_cache>`
* :doc:`FormServiceProvider <providers/form>`
* :doc:`SecurityServiceProvider <providers/security>`
* :doc:`RememberMeServiceProvider <providers/remember_me>`
* :doc:`ServiceControllerServiceProvider <providers/service_controller>`

サードパーティーのプロバイダ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コミュニティで開発されているサービスプロバイダもあります。
これらのサードパーティのプロバイダの一覧は `Silexリポジトリのwiki <https://github.com/silexphp/Silex/wiki/Third-Party-ServiceProviders>`_ にあります.

あなたのプロバイダーもぜひ共有してみてください。


プロバイダーの作成
----------------------

プロバイダーは ``Silex\Api\ServiceProviderInterface`` を実装しなければなりません。 ::

    {
        function register(Application $app);

        function boot(Application $app);
    }

単に二つのメソッドを実装したクラスを作成するだけです。 ``register()`` 
メソッドでは、他のサービスやパラメータを利用するようなアプリケーション上にサービスを定義することができます。 ``boot()`` メソッドでは、アプリケーションがリクエストをハンドリングする前にアプリケーションの設定を行えます。

次がそのようなプロバイダーのサンプルです。 ::

    namespace Acme;

    use Silex\Application;
    use Silex\Api\ServiceProviderInterface;

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

        public function boot(Application $app)
        {
        }
    }

このクラスは ``hello`` サービスを提供します。このサービスは保護されたクロージャーです。
``name`` を引数として取り、 ``name`` が与えられていない場合 ``hello.default_name`` を返してくれます。
初期値を与えられていない場合は空の文字列を使います。

このプロバイダーは次のように使うことができます。 ::

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


.. _controller-providers:

コントロラープロバイダー(Controllers providers)
---------------------------------------------------

プロバイダーの読み込み
~~~~~~~~~~~~~~~~~~~~~~~~~~

プロバイダーを読み込んで使うためには、パスで指定したコントローラーを "mount" する必要があります。 ::

    $app = new Silex\Application();

    $app->mount('/blog', new Acme\BlogControllerProvider());

プロバイダーで定義されている全てのコントローラーは、 `/blog` パス以下で使用可能です。

プロバイダーの作成
~~~~~~~~~~~~~~~~~~~

プロバイダーは ``Silex\ControllerProviderInterface`` を実装しなければなりません。 ::

    interface ControllerProviderInterface
    {
        function connect(Application $app);
    }

次がそのようなプロバイダーのサンプルです。 ::

    namespace Acme;

    use Silex\Application;
    use Silex\Api\ControllerProviderInterface;

    class HelloControllerProvider implements ControllerProviderInterface
    {
        public function connect(Application $app)
        {
            // デフォルトのルーティングに基づいたコントローラの作成
            $controllers = $app['controllers_factory'];

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

これで以下のようにプロバイダーを使うことができます。 ::

    $app = new Silex\Application();

    $app->mount('/blog', new Acme\HelloControllerProvider());

この例では、 ``/blog/`` のパスは、プロバイダーで定義されたコントローラーを参照するようになります。

.. tip::

    サービスプロバイダーインタフェースとコントローラープロバイダーインタフェースの両方を実装したプロバイダーも定義することができ、コントローラの動作に必要なサービスと同じクラスの中で、そのプロバイダをパッケージ化できます。

commit: 1ba15a1769979083b19d775237fa0cfefb1475fe
original: https://github.com/silexphp/Silex/blob/master/doc/providers.rst
