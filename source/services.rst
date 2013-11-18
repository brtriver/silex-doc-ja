サービス
========

Silex はマイクロフレームワークであることはもちろんのこと、マイクロサービスコンテナーでもあります。
Silex はたったの44行(コメント抜きの行数)で書かれた `Pimple <http://pimple.sensiolabs.org>`_
を拡張してマイクロサービスコンテナとして動作するようになっています。

DI (Dependency Injection)
---------------------------

.. note::

    もし　Dependency Injection について既に理解しているのであればこの節は読まなくても大丈夫です。

Dependency Injection は 外部のサービスやグローバル領域に依存するものを生成する代わりに、それらをサービスに渡すというデザインパターンです。
これは、一般的にコードをカプセル化し、再利用性を高め、柔軟性がありテストを書き易くするために用いられます。

ここにクラスのサンプルがあります。このクラスでは ``User`` オブジェクトを引数として必要としており、オブジェクトから取得できる属性をJSONフォーマットでファイルに書き出しています。 ::

    class JsonUserPersister
    {
        private $basePath;

        public function __construct($basePath)
        {
            $this->basePath = $basePath;
        }

        public function persist(User $user)
        {
            $data = $user->getAttributes();
            $json = json_encode($data);
            $filename = $this->basePath.'/'.$user->id.'.json';
            file_put_contents($filename, $json, LOCK_EX);
        }
    }

この簡単なサンプルでの依存関係は ``basePath`` プロパティです。
このプロパティはクラスのコンストラクターに渡されています。
こうすることで、異なる basePath を持った複数の独立したインスタンスを作成することができるということです。
もちろん依存関係の指定を単なる文字列にすべきではありません。なぜなら多くの場合は他のサービスを指定することがよくあるからです。

コンテナー (Container)
~~~~~~~~~~~~~~~~~~~~~~

DIC や サービスコンテナーはサービスの生成や保存を担当します。
そして、必要とされているサービスの依存関係を再帰的に生成し、それらを注入(inject)することができます。
そしてこの作業は遅延読み込み(lazily)で行われます、つまり、そのサービスが本当に必要になったときにのみ生成されるということです。

ほとんどのコンテナーは非常に複雑で XML や YAML ファイルを使って設定が記述されています。

しかし、 Pipmple は違うのです。

Pimple
------

Pimple は存在するサービスコンテナーの中でもおそらく最もシンプルなものです。
SPL の ArrayAccess インターフェースを実装し、クロージャーを活用しています。

新しい Pimple のインスタンスを作成するところから始めてみましょう -- 
そして ``Silex\Application`` は ``Pimple`` を拡張したものなので、これからの説明はすべて Silex においても適用できます。 ::

    $container = new Pimple();

もしくは、 ::

    $app = new Silex\Application();

パラメーター (Parameters)
~~~~~~~~~~~~~~~~~~~~~~~~~

コンテナー上に配列のキーを指定することで (通常は文字列で) パラメーターをセットすることができます。 ::

    $app['some_parameter'] = 'value';

配列のキーは何でもかまいません。習慣的にピリオドは名前空間のような目的で使うことができます。 ::

    $app['asset.host'] = 'http://cdn.mysite.com/';

設定したパラメーターの値は同じ構文で呼び出すことができます。 ::

    echo $app['some_parameter'];

サービスの定義 (Service definitions)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

サービスを定義することはパラメーターを定義することとなんら違いはありません。
コンテナーに配列のキーでクロージャーを設定するだけです。
サービスを取得するときに初めてクロージャーは実行されます。
そのため、実際にサービスが必要とされるまでサービスの作成を遅延させることができます。 ::

    $app['some_service'] = function () {
        return new Service();
    };

そして、サービスを取得するためには次のように書きます。 ::

    $service = $app['some_service'];

``$app['some_service']`` を呼び出せば、呼び出すたびに新しいサービスのインスタンスが生成されます。

共有サービス (Shared services)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コード全体で共通となるようなサービスのインスタンスを使いたいときもあるでしょう。これを実現できるようにするため、 **shared** サービスを作ることができるようになっています。 ::

    $app['some_service'] = $app->share(function () {
        return new Service();
    });

このコードは最初の呼び出し時にサービスを生成し、2回目以降の呼び出しには生成しておいたインスタンスを返します。

クロージャーからコンテナーへのアクセス
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

多くの場合、サービスを定義するためのクロージャーの中で、サービスコンテナーにアクセスしたい場合があるでしょう。
たとえば、現在のサービスに依存している既存のサービスを取得したいような場合です。

このためには、引数を使ってクロージャーにコンテナーを渡します。 ::

    $app['some_service'] = function ($app) {
        return new Service($app['some_other_service'], $app['some_service.config']);
    };

これが DI のサンプルです。
``some_service`` は ``some_other_service`` に依存しており、設定オプションとして ``some_service.config`` を受け取ります。
``some_service`` にアクセスが発生し生成されるときだけ依存関係があり、これらの定義を上書きするだけで依存関係を書き換えることができます。

.. note::

    この仕組みは共有サービスでも動作します。

最初の例に戻ると、コンテナーを使って依存性を管理するためには次のようにすればいいことが分かります。 ::

    $app['user.persist_path'] = '/tmp/users';
    $app['user.persister'] = $app->share(function ($app) {
        return new JsonUserPersister($app['user.persist_path']);
    });


保護されたクロージャー (Protected closures)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コンテナーはクロージャーをサービスのためのファクトリと見なすので、クロージャーを読み込むごとにこれらを常に実行します。

しかしながら、パラメーターとしてクロージャー自体を保存したいときがあるでしょう。
たとえば、クロージャーを取得し、あなた自身が定義した引数で実行したいような場合です。

このような理由があるため、Pimpleにはクロージャが実行されないようにするための ``protect`` メソッドが存在します。 ::

    $app['closure_parameter'] = $app->protect(function ($a, $b) {
        return $a + $b;
    });

    // クロージャーは実行されません
    $add = $app['closure_parameter'];

    // この時点でクロージャーが実行されます
    echo $add(2, 3);

保護されたクロージャーはコンテナーにアクセスすることができないことにご注意ください。

コアサービス (Core services)
-----------------------------

Silex は利用したり置き換えることができるサービスの範囲を定義しています。
みなさんはこれらの大部分を台無しにしたくないと思っていらっしゃることでしょう。

* **request**: 現在のリクエストオブジェクトを保持しています。
  このオブジェクトは `Request
  <http://api.symfony.com/master/Symfony/Component/HttpFoundation/Request.html>`_
  のインスタンスです。
  ``GET`` 、 ``POST`` などの多くのパラメーターにアクセスすることができます!

  利用例 ::

    $id = $app['request']->get('id');

  これはリクエストが実行されているときにだけ利用可能です。
  コントローラー、　before、 after ミドルウェア、エラーハンドラーの内部からのみアクセスすることができます。

* **routes**: `RouteCollection
  <http://api.symfony.com/master/Symfony/Component/Routing/RouteCollection.html>`_
  が内部で利用されています。
  これを使って、ルーティングの追加、修正、読み込みを行うことができます。

* **controllers**: ``Silex\ControllerCollection`` 
  が内部で利用されています。
  詳細については *Internals* の章をご参照ください。

* **dispatcher**: `EventDispatcher
  <http://api.symfony.com/master/Symfony/Component/EventDispatcher/EventDispatcher.html>`_
  が内部で利用されています。
  Symfony2 におけるコアシステムであり Silex でもほんの少しだけ利用されています。

* **resolver**: `ControllerResolver
  <http://api.symfony.com/master/Symfony/Component/HttpKernel/Controller/ControllerResolver.html>`_
  が内部で利用されています。
  正しい引数でコントローラーが実行されるように注意を払ってくれています。

* **kernel**: `HttpKernel
  <http://api.symfony.com/master/Symfony/Component/HttpKernel/HttpKernel.html>`_
  が内部で利用されています。
  HttpKernel は Symfony2 の心臓部分であり、入力として Request を受け取り、出力として Response を返します。

* **request_context**: request contextとはRouter と UrlGenerator で利用されるリクエストを簡易化したものです。
 
* **exception_handler**: exception ハンドラーは `error()` メソッドを通してエラーハンドラーを登録していないときや、 ハンドラーがレスポンスを返却しないときに利用される標準のハンドラーです。
  この動きは `unset($app['exception_handler'])` で無効にすることができます。

* **logger**: ``Psr\Log\LoggerInterface`` のインスタンスです。デフォルトでは、値がnullに設定されているため無効になっています。ロギングを有効にするには ``MonologServiceProvider`` を使うか、PSR logger interfaceを実装した独自の ``logger`` サービスを使ってください。

  Silex 1.1以前では、 ``Symfony\Component\HttpKernel\Log\LoggerInterface``
  である必要があります。

.. note::

    これらすべての Silex のコアサービスは共有されています。

コアパラメーター (Core parameters)
-------------------------------------------

* **request.http_port** (オプション): HTTPS でない URL のための標準のポートを上書きできます。もし現在のリクエストが HTTP であれば、このパラメーターで現在利用しているポートを指定することができます。

  標準は 80 番です。

  このパラメーターは ``UrlGeneratorProvider`` で利用されます。

* **request.https_port** (オプション): HTTPS の URL のための標準のポートを上書きできます。
  もし現在のリクエストが HTTPS であれば、このパラメーターで現在利用しているポートを指定することができます。

  標準は 443 番です。

  このパラメーターは ``UrlGeneratorProvider`` で利用されます。

* **locale** (オプション): ユーザーのロケールです。リクエストハンドリングの前に設定した場合、デフォルトロケール（標準では ``en`` ）を設定することになります。リクエストがハンドリングされているときは、現在のルーティングの ``_locale`` リクエスト属性に基づいて自動的に設定されます。

* **debug** (オプション): デバッグモードでアプリケーションを動作させるかどうかを返します

  標準は false です。

* **charset** (optional): レスンポンスで指定される文字コードです。

  標準は UTF-8 です。
