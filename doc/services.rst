サービス
========

Silex はマイクロフレームワークであることはもちろんのこと、マイクロサービスコンテナーでもあります。
Silex はたったの44行(コメント抜きの行数)で書かれた `Pimple <https://github.com/fabpot/Pimple>`_
を拡張してマイクロサービスコンテナとして動作するようになっています。

DI (Dependency Injection)
---------------------------

.. note::

    もし　Dependency Injection について既に理解しているのであればこの節は読まなくても大丈夫です。

Dependency Injection は 外部のサービスやグローバル領域のから依存するものを作成する代わりにそれらをサービスに渡すというデザインパターンです。
一般的にコードをカプセル化し、再利用性を高め、柔軟性がありテストを書き易くするために用いられます。

ここにクラスのサンプルがあります。このクラスでは ``User`` オブジェクトを引数として必要としており、オブジェクトから取得できる属性をJSONフォーマットでファイルに書き出しています。


::

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

この簡単なサンプルでの依存関係の指定は ``basePath`` プロパティです。
このプロパティはクラスのコンストラクターに渡されています。
こうすることで、異なる basePath を持った複数の独立したインスタンスを作成することができるということです。
もちろん依存関係の指定を単なる文字列にすべきではありません。なぜなら多くの場合は他のサービスを指定することがよくあるからです。

コンテナー (Container)
~~~~~~~~~~~~~~~~~~~~~~

DI や サービスコンテナーはサービスを生成したり保存しておく責任があります。
そして再起的に必要とされているサービスの依存関係を生成しそれらを注入(inject)することができます。
そしてこの作業は遅延読み込み(lazily)で行われます、つまり、そのサービスが本当に必要になったときにのみ生成されるということです。

ほとんどのコンテナーは非常に複雑でXMLやYAMLファイルを使って設定が記述されています。

しかし、 Pipmple は違うのです。

Pimple
------

Pimple は存在するサービスコンテナーの中でもおそらく最もシンプルなものです。
配列アクセス(ArrayAccess) のインターフェースを実装したクロージャーを活用しています。

新しい Pimple のインスタンスを作成するところから始めてみましょう -- 
そして ``Silex\Application`` は ``Pimple`` を拡張したものなので、これからの説明はすべて Silex においても適用できます::

    $container = new Pimple();

もしくは ::

    $app = new Silex\Application();

パラメーター
~~~~~~~~~~~~~~~

コンテナー上に配列のキーを指定することで (通常は文字列で) パラメータをセットすることができます::

    $app['some_parameter'] = 'value';

配列のキーは何でもかまいません。習慣的にピリオドは名前空間のような目的で使うことができます::

    $app['asset.host'] = 'http://cdn.mysite.com/';

設定したパラメータの値は同じ構文で呼び出すことができます::

    echo $app['some_parameter'];

サービスの定義
~~~~~~~~~~~~~~~~~~~

サービスを定義することはパラメータを定義することとなんら違いはありません。
コンテナーに配列のキーでクロージャーを設定するだけです。
サービスを取得するときにクロージャーは実行されます。
このようにしてサービスを遅延して作成することができます

::

    $app['some_service'] = function () {
        return new Service();
    };

そして、サービスを取得するためには次のようにします::

    $service = $app['some_service'];

``$app['some_service']`` を呼び出せば、呼び出す度に新しいサービスのインスタンスが生成されます。

共有サービス (Shared services)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コード全体で共通のサービスのインスタンスを使いたいときもあるでしょう。
そのようなために、 *shared* サービスを作ることができるようになっています ::

    $app['some_service'] = $app->share(function () {
        return new Service();
    });

最初の呼び出し時にサービスを生成し、2回目以降の呼び出しには生成しておいたインスタンスを返すということをやっています。

クロージャーからコンテナーへのアクセス
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

多くの場合、クロージャーの中からサービスコンテナーにアクセスしたい場合があるでしょう。
たとえば、既存の依存しているサービスを取得したいような場合です。

このためには、引数を使ってクロージャーにコンテナーを渡します::

    $app['some_service'] = function ($app) {
        return new Service($app['some_other_service'], $app['some_service.config']);
    };

これがDIのサンプルになります。
``some_service`` は ``some_other_service`` に依存しており、 ``some_service.config`` を設定オプションとして利用することができます。
``some_service`` にアクセスが発生し生成されるときだけ依存関係があり、これらの定義を上書きするだけで依存関係を書き換えることができます。

.. note::

    この仕組みは共有サービスでも動作します。

保護されたクロージャー (Protected closures)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コンテナーはサービスのための工場(factory)としてクロージャーがあると理解しているので。クロージャーを読みこむとにいつも実行します。
Because the container sees closures as factories for
services, it will always execute them when reading them.

しかしながら、パラメータとしてクロージャーを保存したいときがあるでしょう。
たとえば、クロージャーを取得しあなた自身が定義した引数で実行したいような場合です。

こういった理由で Pimple は ``protect`` メソッドを使うことであなたが作成したクロージャーが実行されないようにいつも保護することができます。

::

    $app['closure_parameter'] = $app->protect(function ($a, $b) {
        return $a + $b;
    });

    // クロージャーは実行されません
    $add = $app['closure_parameter'];

    // この時点でクロージャーが実行されます
    echo $add(2, 3);

保護されたクロージャーはコンテナーにアクセスすることがdけいないということに注意してください。

コアサービス (Core services)
-----------------------------

Silex は利用したり置き換えることができるサービスの範囲を定義しています。
これらの大部分はさわりたいと思わないでしょう。

* **リクエスト (request)**: 現在のリクエストオブジェクトを保持しており,
  このオブジェクトは `Request
  <http://api.symfony.com/2.0/Symfony/Component/HttpFoundation/Request.html>`_
  のインスタンスです。
  ``GET`` 、 ``POST`` やさらに多くのパラメーターにアクセスすることができます!

  利用例::

    $id = $app['request']->get('id');

これはリクエストが実行されているときにだけ利用可能です。
コントローラー、　before、 afterフィルターそしてエラーハンドラーの内部からのみアクセスすることができます。

* **オートローダー (autoloader)**: このサービスは `UniversalClassLoader
  <http://api.symfony.com/2.0/Symfony/Component/ClassLoader/UniversalClassLoader.html>`_
  によって提供されています。
  接頭辞や名前空間を登録することができます。

  利用例 (Twigのクラスのオートロードの設定)::

    $app['autoloader']->registerPrefix('Twig_', $app['twig.class_path']);

* **routes**: 内部で利用されている `RouteCollection
  <http://api.symfony.com/2.0/Symfony/Component/Routing/RouteCollection.html>`_
  。
  ルーティングの追加、修正、読み込みを行うことができます。

* **controllers**: 内部で利用されている ``Silex\ControllerCollection`` 。
  詳細については *Internals* の章を参照してください。

* **dispatcher**: 内部で利用されている `EventDispatcher
  <http://api.symfony.com/2.0/Symfony/Component/EventDispatcher/EventDispatcher.html>`_
  。　Symfony2 におけるコアシステムであり Silex でもほんの少しだけ利用されています。

* **resolver**: 内部で利用されている `ControllerResolver
  <http://api.symfony.com/2.0/Symfony/Component/HttpKernel/Controller/ControllerResolver.html>`_
  。　正しい引数でコントローラーが実行されるように注意を払ってくれています。

* **kernel**: 内部で利用されている `HttpKernel
  <http://api.symfony.com/2.0/Symfony/Component/HttpKernel/HttpKernel.html>`_
  。　HttpKernel は Symfony2 の心臓部分であり、入力として Request を受け取り、出力として Response を返します。

* **request_context**: リクエストのコンテクストとは Router と UrlGenerator で利用されるリクエストを簡易化したものです。

.. note::

    これらすべての Silex のコアサービスは共有されています。

コアのパラメーター
---------------

* **request.http_port** (オプション): HTTPSでないURLのための標準のポートを上書きできます。
  このパラメータで現在利用しているポートを指定することができます。

  標準は 80 番です。

  このパラメーターは ``UrlGeneratorExtension`` で利用されます。

* **request.https_port** (オプション): HTTPSのURLのための標準のポートを上書きできます。
  もし現在のリクエストが HTTPS であれば、このパラメータで現在利用しているポートを指定することができます。

  標準は 443 番です。

  このパラメーターは ``UrlGeneratorExtension`` で利用されます。
