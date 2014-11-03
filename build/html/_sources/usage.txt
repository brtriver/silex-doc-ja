使用方法 (Usage)
====================

この章では Silex の使い方について説明します。

インストール (Installation)
----------------------------------

早くSilexを始めたい場合はSilexをアーカイブとして `download`_ して展開してください。そうすると以下の様なディレクトリ構造が得られるはずです。

.. code-block:: text

    ├── composer.json
    ├── composer.lock
    ├── vendor
    │   └── ...
    └── web
        └── index.php

Silexをもっと柔軟に使いたい場合は、 Composer_ を用います。
まず以下の様な ``composer.json`` を作ってください。

.. code-block:: json

    {
        "require": {
            "silex/silex": "~1.1"
        }
    }

その後に、 Composer_ を実行すればSilexと、それに関する全ての依存パッケージがインストールされます。

.. code-block:: bash

    $ curl -s http://getcomposer.org/installer | php
    $ php composer.phar install

.. tip::

    デフォルトでは、SilexはSymfonyの安定版のコンポーネントに依存しています。
    それらのmasterバージョンを使用したい場合は、 ``composer.json`` に、
    ``"minimum-stability": "dev"`` と付け加えてください。

アップグレード (Upgrading)
-------------------------------

Silexを最新版にアップグレードするには、以下の ``update`` コマンドを実行してください。

.. code-block:: bash

    $ php composer.phar update


ブートストラップ (Bootstrap)
-------------------------------

Silexを使うのに必要なのは ``vendor/autoload.php`` をrequireし、 ``Silex\Application`` のインスタンスを生成することだけです。
コントローラ定義の後に、 ``run`` メソッドをアプリケーション上で呼んでください。 ::

    // web/index.php

    require_once __DIR__.'/../vendor/autoload.php';

    $app = new Silex\Application();

    // 定義をここに書きます。

    $app->run();

その後にWebサーバーの設定が必要となります。（詳しくは、 :doc:`Webサーバーの章 <web_servers>` を見てください。).

.. tip::

    ウェブサイトを開発中のときは、デバッグしやすくするためにデバッグモードを有効にすることもできます。 ::

        $app['debug'] = true;

.. tip::

    もしアプリケーションを$ipというアドレスを持つプロキシサーバーを通して動作させたい場合は Silex が `X-Forwarded-For` ヘッダーを信頼するようにしたいでしょう。
    その場合は次のようにアプリケーションを実行させる必要があります。 ::

        use Symfony\Component\HttpFoundation\Request;

        Request::setTrustedProxies(array($ip));
        $app->run();

ルーティング (Routing)
-------------------------------

Silex ではルーティングと、そのルーティングに一致したときに実行されるコントローラーを定義します。

ルーティングのパターンは次のような構成になっています。

* *パターン (Pattern)*: ルーティングパターンであり、リソースへのパスを定義します。
  パターンは可変部分を含むことができ、正規表現を使った必須項目を設定することもできます。

* *メソッド (Method)*: HTTPメソッド( ``GET``, ``POST``, ``PUT`` ``DELETE`` )のうち、どれかを指定します。  これはリソースとの相互作用を表しています。 
  一般的には、 ``GET`` と ``POST`` だけが利用されますが、他のメソッドも使うことが可能です。

コントローラーはクロージャーを次のように使うことで定義できます。 ::

    function () {
        // do something
    }

クロージャーは定義の外部から状態を取り込むことができる無名関数のことです。
これはグローバル変数とは異なります、なぜなら外部の状態はグローバルである必要がないからです。
たとえば、メソッドの中にクロージャーを定義することができ、メソッドのローカル変数を取り込むことができます。

.. note::

    スコープを取り込まないクロージャーはラムダのようだと言われます。
    なぜなら PHP の無名関数はすべて ``Closure`` クラスのインスタンスであり、区別することができないからです。

クロージャーの戻り値はページのコンテンツになります。

クラスメソッドを利用してコントローラを定義する方法もあります。
``ClassName::methodName`` でのスタティックな呼び出し構文も利用可能です。

GET ルーティングの例 (Example GET route)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ここに ``GET`` ルーティングを定義した例があります。 ::

    $blogPosts = array(
        1 => array(
            'date'      => '2011-03-29',
            'author'    => 'igorw',
            'title'     => 'Using Silex',
            'body'      => '...',
        ),
    );

    $app->get('/blog', function () use ($blogPosts) {
        $output = '';
        foreach ($blogPosts as $post) {
            $output .= $post['title'];
            $output .= '<br />';
        }

        return $output;
    });

``/blog`` へアクセスすると 投稿されたブログのタイトルの一覧が返されます。
ここで使われている ``use`` はこの文脈では別のものであることを意味します。
外部スコープから $blogPosts 変数を取り込むということをクロージャーに知らせています。
``use`` を使うことでクロージャー内で渡した変数を使うことができるようになります。

動的ルーティング (Dynamic routing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

さて、ブログの個々の記事を閲覧するためのもう1つ別のコントローラーを用意してみましょう。 ::

    $app->get('/blog/{id}', function (Silex\Application $app, $id) use ($blogPosts) {
        if (!isset($blogPosts[$id])) {
            $app->abort(404, "Post $id does not exist.");
        }

        $post = $blogPosts[$id];

        return  "<h1>{$post['title']}</h1>".
                "<p>{$post['body']}</p>";
    });


ルーティングはクロージャーに渡される ``{id}`` という変数を定義しています。 

なお、タイプヒンティングのおかげで、 ``Application`` は、 Silex によって自動的にクロージャに注入されています。

POST された値がなかったとき、より早い段階でリクエストを停止するために ``abort()`` を使います。実際には例外を投げていますが、どのように扱うかは後ほど説明します。

POST ルーティングの例 (Example POST route)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

POSTルーティングはリソースの生成を意味します。
この例となるのがフィードバック用のフォームです。
ここでは ``mail`` 関数を使ってメールを送信してみます。 ::

    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;

    $app->post('/feedback', function (Request $request) {
        $message = $request->get('message');
        mail('feedback@yoursite.com', '[YourSite] Feedback', $message);

        return new Response('Thank you for your feedback!', 201);
    });

とても素直な実装になっています。

.. note::

    ``mail()`` 関数を使用する代わりに、 :doc:`SwiftmailerServiceProvider <providers/swiftmailer>` も使用できます。

タイプヒンティングのおかげで、 ``request`` は、 Silex によって自動的にクロージャに注入されています。
リクエストは Request_
のインスタンスです。このことによって、HTTPステータスコードを設定することが可能になります。今回の例では``201　Created`` に設定されます。


リクエストの ``get`` メソッドを使うことで変数を取得することができます。

文字列を返す代わりに Response_ のインスタンスを返しています。
また、 HTTP のステータスコードを設定することもでき、今回の場合であれば ``201 Created`` が設定されています。

.. note::

    Silexは、常に Response_ を内部で使用し、 文字列を ``200 OK`` の HTTP のステータスコードと一緒にレスポンスオブジェクトに変換します。 

他のメソッド (Other methods)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

アプリケーションの中で、 ``get``, ``post``, ``put``, ``delete`` といったメソッドを呼び出せば、ほとんどの HTTP メソッドのためのコントローラーを作ることが可能です。 ::

    $app->put('/blog/{id}', function ($id) {
        ...
    });

    $app->delete('/blog/{id}', function ($id) {
        ...
    });

.. tip::
    
    ほとんどのウェブブラウザのフォームは、その他のHTTPメソッドを直接サポートしていません。GETやPOST以外のメソッドを使いたい場合は、 ``_method`` という名前を持つ特別なフォームフィールドを使うことができます。このフォームフィールドを使うときには、フォームの ``method`` 属性をPOSTに設定する必要があります。 ::

        <form action="/my/target/route/" method="post">
            ...
            <input type="hidden" id="_method" name="_method" value="PUT" />
        </form>

    Symfonyコンポーネント2.2以上を使用している場合は、明示的にメソッドのオーバーライドを可能にする必要があります。 ::

        use Symfony\Component\HttpFoundation\Request;

        Request::enableHttpMethodParameterOverride();
        $app->run();

また、 ``match`` メソッドを利用することもでき、この場合はすべてのメソッドに一致します。
この性質は、 ``method`` メソッドを用いることで制限することができます。 ::

    $app->match('/blog', function () {
        ...
    });

    $app->match('/blog', function () {
        ...
    })
    ->method('PATCH');

    $app->match('/blog', function () {
        ...
    })
    ->method('PUT|POST');

.. note::

    ルーティングがどのような順番で定義されたかはとても重要です。
    最初に一致したルーティングが利用されるからです。そのため、より汎用的なルーティングはより下の方に定義するようにしてください。

ルーティング変数 (Route variables)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


前に説明したように、次のようにルーティングにおいて変数を定義することができます.
 ::

    $app->get('/blog/{id}', function ($id) {
        ...
    });

ルーティングの変数部分の名前がクロージャーの引数に一致するようにすれば、2つ以上の変数部分を定義することが可能です。 ::

    $app->get('/blog/{postId}/{commentId}', function ($postId, $commentId) {
        ...
    });

説明していませんでしたが、次のように引数の順番を入れ替えることだってできます。 ::

    $app->get('/blog/{postId}/{commentId}', function ($commentId, $postId) {
        ...
    });

現在のリクエストとアプリケーションオブジェクトを次のように利用することもできます。 ::

    $app->get('/blog/show/{id}', function (Application $app, Request $request, $id) {
        ...
    });

.. note::

    アプリケーションとリクエストオブジェクトについてですが、 Silex は変数名ではなく、タイプヒンティングに基づいて注入します。 ::

        $app->get('/blog/{id}', function (Application $foo, Request $bar, $id) {
            ...
        });

ルーティングで取得される変数の変換　(Route variables converters)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コントローラーにルーティングで取得した変数を注入する前に、変換処理をはさむことができます。 ::

    $app->get('/user/{id}', function ($id) {
        // ...
    })->convert('id', function ($id) { return (int) $id; });

たとえば、ルーティングで取得した変数をオブジェクトに変換し、異なるコントローラー間で再利用性を高めたい場合などに便利です。 ::

    $userProvider = function ($id) {
        return new User($id);
    };

    $app->get('/user/{user}', function (User $user) {
        // ...
    })->convert('user', $userProvider);

    $app->get('/user/{user}/edit', function (User $user) {
        // ...
    })->convert('user', $userProvider);

変換処理のコールバックは Request_ を第2引数として受け取ることができます。 ::

    $callback = function ($post, Request $request) {
        return new Post($request->attributes->get('slug'));
    };

    $app->get('/blog/{id}/{slug}', function (Post $post) {
        // ...
    })->convert('post', $callback);

変換処理はサービスとしても定義できます。例として、以下の様なDoctrine ObjectManagerによるユーザーコンバーターが挙げられます。 ::

    use Doctrine\Common\Persistence\ObjectManager
    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    class UserConverter
    {
        private $om;

        public function __construct(ObjectManager $om)
        {
            $this->om = $om;
        }

        public function convert($id)
        {
            if (null === $user = $this->om->find('User', (int) $id)) {
                throw new NotFoundHttpException(sprintf('User %d does not exist', $id));
            }

            return $user;
        }
    }

このサービスはアプリケーションで登録されることはなく、コンバートメソッドはコンバーターとして使われます。 ::

    $app['converter.user'] = function () {
        return new UserConverter();
    };

    $app->get('/user/{user}', function (User $user) {
        // ...
    })->convert('user', 'converter.user:convert');

必須項目 (Requirements)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

特定のパターンのみ一致させたい場合があるでしょう。そのときはルーティングメソッドによって返される ``Controller`` オブジェクトの ``assert`` メソッドを呼ぶことで正規表現による必須項目を定義することができます。

次の例では ``id`` という引数が数値になるように ``\d+`` でチェックしています。 ::

    $app->get('/blog/{id}', function ($id) {
        ...
    })
    ->assert('id', '\d+');

チェーン(chain)で呼び出すこともできます。 ::

    $app->get('/blog/{postId}/{commentId}', function ($postId, $commentId) {
        ...
    })
    ->assert('postId', '\d+')
    ->assert('commentId', '\d+');

デフォルト値 (Default values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Controller`` オブジェクトの ``value`` メソッドを呼ぶことで、どんなルーティングの値でもデフォルト値を定義することができます。 ::

    $app->get('/{pageName}', function ($pageName) {
        ...
    })
    ->value('pageName', 'index');

この例では、 ``/`` をルーティングに一致させています。そしてその際は、 ``pageName`` 変数は ``index`` になります。

名前付きルーティング (Named routes)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

プロバイダーの中には名前付きルーティングを使うことができるものがあります (``UrlGeneratorProvider`` など)。
デフォルトでは、 Silex はあなたの代わりにルーティング名を生成してくれます。しかし、これらは利用されません。
ルーティングメソッドによって返される ``Controller`` オブジェクトの ``bind`` メソッドを呼び出すことでルーティングに名前を付けることができます。 ::

    $app->get('/', function () {
        ...
    })
    ->bind('homepage');

    $app->get('/blog/{id}', function ($id) {
        ...
    })
    ->bind('blog_post');


.. note::

    使おうとしているプロバイダーが ``RouteCollection`` を利用しているときのみ名前ルーティングは意味があります。

クラス内コントローラ (Controllers in classes)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

無名関数を使いたくない場合、コントローラをメソッドとして定義することが出来ます。
これは ``ControllerClass::methodName`` という文法によって実現されます。このときコントローラオブジェクトの生成を遅延させることが可能です。 ::

    $app->get('/', 'Acme\\Foo::bar');

    use Silex\Application;
    use Symfony\Component\HttpFoundation\Request;

    namespace Acme
    {
        class Foo
        {
            public function bar(Request $request, Application $app)
            {
                ...
            }
        }
    }

この例は レスポンスを得るために、 ``Igorw\Foo`` というクラスを要求に応じて読み込み、インスタンスを生成した後に、 ``bar`` メソッドを呼び出します。このとき、 ``$request`` と ``$app`` をクロージャに注入するために Request_ と ``Silex\Application`` というタイプヒンティングが使用可能です。

こうすることで、Silexとあなたのコントローラの分離度が強まるため、 :doc:`コントローラをサービスとして定義することが出来ます。 <providers/service_controller>`.

全体の設定 (Global Configuration)
----------------------------------------------

あるコントローラの設定を全てのコントローラに対して適用したい場合（例えば、コンバーター、ミドルウェア、必須項目、デフォルト値など）、 全てのコントローラを保持する ``$app['controllers']`` に対して設定を行うことができます。 ::

    $app['controllers']
        ->value('id', '1')
        ->assert('id', '\d+')
        ->requireHttps()
        ->method('get')
        ->convert('id', function () { /* ... */ })
        ->before(function () { /* ... */ })
    ;

これらの設定は全ての登録済みコントローラに適用され、また新しいコントローラのデフォルト設定にもなります。

.. note::

    全体の設定は、オリジナルの全体への設定を持つコントローラプロバイダーには適用されません。
    詳しくは、 :doc:`コントローラの組織化<organizing_controllers>` を読んでください。

.. warning::

    コンバーターは **全ての** 登録済みコントローラに対して実行されます。

エラーハンドリング (Error handlers)
---------------------------------------------------

コードのどこかで例外が発生した際に、ユーザーにエラーページのようなものを表示したいことがあるでしょう。
これらエラーハンドラーがやることなのです。
ログ処理のような処理を追加してエラーハンドリングを使うことができます。

エラーハンドラーを登録するために、 ``Exception`` を引数に持ち、レスポンスを返してくれる ``error`` メソッドにクロージャーを渡します。 ::

    use Symfony\Component\HttpFoundation\Response;

    $app->error(function (\Exception $e, $code) {
        return new Response('We are sorry, but something went terribly wrong.');
    });

``$code`` 引数を使うことで詳細なエラーを確認することができます。そしてエラーの種類で処理を変えることができます。 ::

    use Symfony\Component\HttpFoundation\Response;

    $app->error(function (\Exception $e, $code) {
        switch ($code) {
            case 404:
                $message = 'The requested page could not be found.';
                break;
            default:
                $message = 'We are sorry, but something went terribly wrong.';
        }

        return new Response($message);
    });

.. note::

    Silexはレスポンスのステータスコードが例外に沿うような適切な物にセットされることを保証するので、例外が生じた場合、レスポンスでのステータスコードの設定が働きません。ステータスコードをオーバーライドしたい場合は（適切な理由が無い限りそうすべきではありませんが）、 ``X-Status-Code`` ヘッダをセットしてください。 ::

        return new Response('Error', 404 /* 無視されます */, array('X-Status-Code' => 200));

クロージャの引数に対し詳細なタイプヒンティングをセットすることで、エラーハンドラの適用範囲を特定の例外クラスに対してのみに制限することができます。 ::

    $app->error(function (\LogicException $e, $code) {
        // このハンドラーは\LogicExceptionと、そのサブクラスのみを扱います。
    });

ログ処理を行いたいなら、このためにエラーハンドラーを分けて使うことができます。
レスポンスのエラーハンドラーの前にロギング処理を登録しなければならないということに注意してください。
なぜならレスポンスが返されてしまうと、後続のハンドラーは無視されてしまうからです。

.. note::

    Silex にはエラーのログ処理を行うための Monolog_
    プロバイダーも付いてきます。
    詳しくは *Providers* の章を参照してください。

.. tip::

    Silex には、デフォルトのエラーハンドラーが付いており、 **debug** を true にすることで、スタックトレースを含む詳細なエラーメッセージを表示します。 false の際には、シンプルなエラーメッセージを表示します。
    ``error()`` メソッドを通して登録したエラーハンドラーは常に優先されますが、デバッグモードが有効の際に表示する便利なエラーも次のようにすれば大丈夫です。 ::

        use Symfony\Component\HttpFoundation\Response;

        $app->error(function (\Exception $e, $code) use ($app) {
            if ($app['debug']) {
                return;
            }

            // エラーのハンドリングと、レスポンスを返す処理
        });

より早い段階でリクエストを破棄するために ``abort`` を使うときにもエラーハンドラーは呼ばれます。 ::

    $app->get('/blog/{id}', function (Silex\Application $app, $id) use ($blogPosts) {
        if (!isset($blogPosts[$id])) {
            $app->abort(404, "Post $id does not exist.");
        }

        return new Response(...);
    });

リダイレクト (Redirects)
---------------------------

リダイレクトレスポンスを返すことでどんなページにもリダイレクトすることができます。このリダイレクト処理のレスポンスは ``redirect`` メソッドで作成することができます。 ::

    $app->get('/', function () use ($app) {
        return $app->redirect('/hello');
    });

この例では ``/`` から ``/hello`` にリダイレクトします。

フォワード (Forwards)
---------------------------

(リダイレクト時に発生するような)ブラウザの往復無しで、他のコントローラにレンダリングを移譲したい場合、内部的なサブリクエストを用いることが出来ます。 ::

    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpKernel\HttpKernelInterface;

    $app->get('/', function () use ($app) {
        // /helloへのリダイレクト
        $subRequest = Request::create('/hello', 'GET');

        return $app->handle($subRequest, HttpKernelInterface::SUB_REQUEST);
    });

.. tip::
    ``UrlGeneratorProvider`` を使っている場合、URIを生成することが出来ます。 ::

        $request = Request::create($app['url_generator']->generate('hello'), 'GET');

他にも心に留めておく必要があることはいくつかあります。ほとんどの場合、現在のマスタリクエストに対し、複数のサブリクエストを発行したいでしょう。例えば、クッキー、サーバ情報、セッションなどです。それらについては :doc:`サブリクエストの作り方 <cookbook/sub_requests>` を読んでください。

JSON
----

JSONデータを返したければ、 ``json`` ヘルパーメソッドを使うことが出来ます。
ヘルパーメソッドに対し、単にデータ、ステータスコード、ヘッダを渡せばレスポンスのためのJSONが生成されます。 ::

    $app->get('/users/{id}', function ($id) use ($app) {
        $user = getUser($id);

        if (!$user) {
            $error = array('message' => 'The user was not found.');
            return $app->json($error, 404);
        }

        return $app->json($user);
    });


ストリーミング (Streaming)
-------------------------------

ストリーミングのレスポンスを作成することができます。 これは送信されるデータをバッファリングできないときに重要です。 ::

    $app->get('/images/{file}', function ($file) use ($app) {
        if (!file_exists(__DIR__.'/images/'.$file)) {
            return $app->abort(404, 'The image was not found.');
        }

        $stream = function () use ($file) {
            readfile($file);
        };

        return $app->stream($stream, 200, array('Content-Type' => 'image/png'));
    });

大きいかたまり(チャンク)で送信したい場合は、 ``ob_fluch`` と ``flush`` を全てのチャンクの後で呼んでください。 ::

    $stream = function () {
        $fh = fopen('http://www.example.com/', 'rb');
        while (!feof($fh)) {
          echo fread($fh, 1024);
          ob_flush();
          flush();
        }
        fclose($fh);
    };

ファイル送信 (Sending a file)
------------------------------------

もしファイルを返したければ、 ``sendFile`` というヘルパーメソッドが使えます。これによって、公に利用可能でないかもしれないファイルを返すことが容易になります。単にファイルパスとステータスコードとヘッダとコンテンツの位置をヘルパーメソッドに渡すと、 ``BinaryFileResponse`` に基づいたレスポンスが生成されます。 ::

    $app->get('/files/{path}', function ($path) use ($app) {
        if (!file_exists('/base/path/' . $path)) {
            $app->abort(404);
        }

        return $app->sendFile('/base/path/' . $path);
    });

値を返す前に、レスポンスを更にカスタマイズするには、　`Symfony\Component\HttpFoundation\BinaryFileResponse
<http://api.symfony.com/master/Symfony/Component/HttpFoundation/BinaryFileResponse.html>`_ のAPIドキュメントを調べてみてください。 ::

    return $app
        ->sendFile('/base/path/' . $path)
        ->setContentDisposition(ResponseHeaderBag::DISPOSITION_ATTACHMENT, 'pic.jpg')
    ;

.. note::

    この機能を使用するためにはHttpFoundation 2.2以上が必要です。

トレイト (Traits)
------------------------

Silexではショートカットメソッドを定義するトレイトを使用可能です。

.. caution::

    この機能を使用するためには、PHP 5.4以上が必要です。

ほとんど全ての標準で組み込まれているサービスプロバイダーは、いくつかの対応するトレイトを持っています。それらを使うためには、使いたいトレイトを含んだ独自のアプリケーションクラスを定義してください。 ::

    use Silex\Application;

    class MyApplication extends Application
    {
        use Application\TwigTrait;
        use Application\SecurityTrait;
        use Application\FormTrait;
        use Application\UrlGeneratorTrait;
        use Application\SwiftmailerTrait;
        use Application\MonologTrait;
        use Application\TranslationTrait;
    }

ルーティングクラスを定義し、対応するトレイトを使用することも可能です。 ::

    use Silex\Route;

    class MyRoute extends Route
    {
        use Route\SecurityTrait;
    }

新しく定義したルーティングクラスを使うためには ``$app['route_class']``
をオーバーライドしてください。 ::

    $app['route_class'] = 'MyRoute';

追加されるメソッドについて学ぶには、それぞれのプロバイダについての章を読んでください。


セキュリティ (Security)
-------------------------------

アプリケーションを攻撃から防御する方法を確認しておきましょう。

エスケープ処理 (Escaping)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ルーティング変数や、リクエストから受け取るされる GET/POST の変数など、ユーザーが入力した値を出力するときはいつでも、正しくエスケープ処理を行う必要があります。
そうすることでクロスサイトスクリプティング(XSS)を防ぐことができます。

* **HTML のエスケープ処理**: HTML のエスケープ処理のために PHP は ``htmlspecialchars`` 関数 を用意してくれています。
  Silex ではこの関数へのショートカットとして ``escape`` メソッドを次のように使うことができます。 ::

      $app->get('/name', function (Silex\Application $app) {
          $name = $app['request']->get('name');
          return "You provided the name {$app->escape($name)}.";
      });

  もし Twig テンプレートを使うのであれば、 Twig が用意してくれているエスケープのための記述を使ったり、自動エスケープ機能を使うべきです。

* **JSON のエスケープ処理**: もし JSON フォーマットのデータをアプリケーションをで提供するなら、 Silexの ``json`` 関数を使うべきです。 ::

      $app->get('/name.json', function (Silex\Application $app) {
          $name = $app['request']->get('name');
          return $app->json(array('name' => $name));
      });

.. _download: http://silex.sensiolabs.org/download
.. _Composer: http://getcomposer.org/
.. _Request: http://api.symfony.com/master/Symfony/Component/HttpFoundation/Request.html
.. _Response: http://api.symfony.com/master/Symfony/Component/HttpFoundation/Response.html
.. _Monolog: https://github.com/Seldaek/monolog

commit: fc8bbb623f33ce448c8bf1d4a95aa26360032de1
original: https://github.com/silexphp/Silex/blob/master/doc/usage.rst
