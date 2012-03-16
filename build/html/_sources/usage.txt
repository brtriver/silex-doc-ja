使用方法
=========

この章では Silex の使い方について説明します。

Bootstrap
---------

Silex をインクルードするために必要なことは ``silex.phar`` ファイルを require し、 ``Silex\Application`` のインスタンスを作成するだけです。
あなたのコントローラーを定義したあとに、 ``run`` メソッドをアプリケーション上で呼んでください。

::

    require_once __DIR__.'/silex.phar';

    $app = new Silex\Application();

    // コントローラーの処理内容を定義する

    $app->run();

もうひとつあなたがやらなければならないことは、サーバーの設定を行うことです。
もし Apache を使っていて ``.htaccess`` を利用することができるのならば次のように設定してください。

.. code-block:: apache

    <IfModule mod_rewrite.c>
        Options -MultiViews

        RewriteEngine On
        #RewriteBase /path/to/app
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteRule ^ index.php [L]
    </IfModule>

.. note::

    もし、 Silex を配置するディレクトリが Web のドキュメントルートでない場合は、 ``RewriteBase`` のコメントを外し
    Web のドキュメントルートからの相対パスであなたのディレクトリ構造に合わせたパスを指定するようにしてください。

.. tip::

    ウェブサイトを開発中のときは、デバッグしやすくするためにデバッグモードを有効にすることもできます::

        $app['debug'] = true;

.. tip::

    もしアプリケーションをプロキシサーバーを通して動作させたい場合は Silex が `X-Forwarded-For*` ヘッダーを信頼するようにしたいでしょう。
    その場合は次のようにアプリケーションを実行させる必要があります::

        use Symfony\Component\HttpFoundation\Request;

        Request::trustProxyData();
        $request = Request::createFromGlobals();
        $app->run();

ルーティング (Routing)
-----------------------

Silex ではルーティングと、そのルーティングに一致したときに実行されるコントローラーを定義します

ルーティングのパターンは次のような構成になっています:

* *パターン (Pattern)*: ルーティングパターンでリソースへのパスを定義します。
  パターンは可変部分を含むことができ、可変部分において正規表現を使った必須項目を設定することができます。

* *メソッド (Method)*: 以下の HTTP メソッド のどれかを指定します: ``GET``, ``POST``, ``PUT``
  ``DELETE`` です。これはリソースとの相互作用を表しています。 
  一般的には、 ``GET`` と ``POST`` だけが利用されますが、他のメソッドも使うことが可能です。

コントローラーはクロージャーを次のように使うことで定義できます::

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

GET ルーティングの例
~~~~~~~~~~~~~~~~~~~~~~

ここに ``GET`` ルーティングを定義した例があります::

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

さて、ブログの個々の記事を閲覧するためのもう1つ別のコントローラーを用意してみましょう::

    $app->get('/blog/show/{id}', function (Silex\Application $app, $id) use ($blogPosts) {
        if (!isset($blogPosts[$id])) {
            $app->abort(404, "Post $id does not exist.");
        }

        $post = $blogPosts[$id];

        return  "<h1>{$post['title']}</h1>".
                "<p>{$post['body']}</p>";
    });

ルーティングはクロージャーに渡される ``{id}`` という変数を定義しています。 

POST された値がなかったとき、より早い段階でリクエストを停止するために ``abort()`` を使います。実際には例外を投げていますが、どのように扱っているかは後ほど説明します。

POST ルーティングの例
~~~~~~~~~~~~~~~~~~~~~~~

POSTルーティングはリソースの生成を意味します。
この例となるのがフィードバック形式です。
ここでは ``mail`` 関数を使ってメールを送信してみます。

::

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
リクエストは `Request
<http://api.symfony.com/master/Symfony/Component/HttpFoundation/Request.html>`_ のインスタンスであり,
リクエストの ``get`` メソッドを使うことで変数を取得することができます。

文字列を返す代わりに `Response
<http://api.symfony.com/master/Symfony/Component/HttpFoundation/Response.html>`_ のインスタンスを返しています。
また、 HTTP のステータスコードを設定することもでき、今回の場合であれば ``201 Created`` が設定されています。

.. note::

    Silexは、常に ``Response`` を内部で使用し、 文字列を ``200 OK`` の HTTP のステータスコードと一緒にレスポンスに変換します。 

他のメソッド 
~~~~~~~~~~~~~

ほとんどの HTTP メソッドのためのコントローラーを作ることが可能です。 ただ次の中のメソッドから1つを利用すれば良いだけです::
``get``, ``post``, ``put``, ``delete``. 
また、 ``match`` メソッドを利用することもでき、この場合はすべてのメソッドに一致します。

::

    $app->match('/blog', function () {
        ...
    });

``method`` メソッドを使うことで許可するメソッドを制限することができます::

    $app->match('/blog', function () {
        ...
    })
    ->method('PATCH');

.. note::

    ルーティングがどのような順番で定義されたかはとても重要です。
    最初に一致したルーティングが利用されるからです。そのため、汎用的なルーティングは一番下に定義するようにしてください。

ルーティング変数 (Route variables)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


前に説明したように、次のようにルーティングにおいて変数を定義することができます::

    $app->get('/blog/show/{id}', function ($id) {
        ...
    });

2つ以上の変数部分を定義することもできますし、変数部分の名前がクロージャーの引数に一致渡すようにしてください。

::

    $app->get('/blog/show/{postId}/{commentId}', function ($postId, $commentId) {
        ...
    });

説明していませんでしたが、次のように引数の順番を入れ替えることだってできます。::

    $app->get('/blog/show/{postId}/{commentId}', function ($commentId, $postId) {
        ...
    });

現在のリクエストとアプリケーションオブジェクトを次のように利用することもできます::

    $app->get('/blog/show/{id}', function (Application $app, Request $request, $id) {
        ...
    });

.. note::

    アプリケーションとリクエストオブジェクトについてですが、 Silex は変数名ではなく、タイプヒンティングに基づいて注入します::

        $app->get('/blog/show/{id}', function (Application $foo, Request $bar, $id) {
            ...
        });


ルーティングで取得される変数の変換
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コントローラーにルーティングで取得した変数を注入する前に、変換処理を行うことができます::

    $app->get('/user/{id}', function ($id) {
        // ...
    })->convert('id', function ($id) { return (int) $id; });

たとえば、ルーティングで取得した変数をオブジェクトに変換し異なるコントローラー間で再利用性を高めたい場合などに便利です::

    $userProvider = function ($id) {
        return new User($id);
    };

    $app->get('/user/{user}', function (User $user) {
        // ...
    })->convert('user', $userProvider);

    $app->get('/user/{user}/edit', function (User $user) {
        // ...
    })->convert('user', $userProvider);

変換処理のコールバックは ``Request`` を第2引数として受け取ることができます::

    $callback = function ($post, Request $request) {
        return new Post($request->attributes->get('slug'));
    };

    $app->get('/blog/{id}/{slug}', function (Post $post) {
        // ...
    })->convert('post', $callback);

必須項目
~~~~~~~~~~~~

特定のパターンのみ一致させたい場合があるでしょう。そのときは正規表現を ``Controller`` オブジェクトの ``assert`` メソッドを呼ぶことで必須項目を定義することができます。
そしてこの ``Controller`` オブジェクトはルーティングメソッドによって返されます。

次のコードは ``\id+`` で数値に一致するようにしているので ``id`` 引数が数字になるようにチェックしています。

    $app->get('/blog/show/{id}', function ($id) {
    ...
    })
    ->assert('id', '\d+');

チェーン(chain) で呼び出すこともできます::

    $app->get('/blog/show/{postId}/{commentId}', function ($postId, $commentId) {
        ...
    })
    ->assert('postId', '\d+')
    ->assert('commentId', '\d+');

デフォルト値
~~~~~~~~~~~~~~

``Controller`` オブジェクトの ``value`` メソッドを呼ぶことで、どんなルーティングの値でもデフォルト値を定義することができます。

::

    $app->get('/{pageName}', function ($pageName) {
        ...
    })
    ->value('pageName', 'index');

この例では、 ``/`` をルーティングに一致させています。そしてその際は、 ``pageName`` 変数は ``index`` になります。

名前ルーティング (Named routes)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

プロバイダーの中には名前ルーティングを使うことができるものがあります (``UrlGeneratorProvider`` など)。
デフォルトでは、 Silex はあなたの代わりにルーティング名を生成してくれます。しかし、これらは利用されません。
ルーティングメソッドによって返される ``Controller`` オブジェクトの ``bind`` メソッドを呼び出すことでルーティングに名前を付けることができます。

::

    $app->get('/', function () {
        ...
    })
    ->bind('homepage');

    $app->get('/blog/show/{id}', function ($id) {
        ...
    })
    ->bind('blog_post');


.. note::

    使おうとしているプロバイダーが ``RouteCollection`` を利用しているときのみ名前ルーティングは意味があります。

ルートミドルウェア (Routes middlewares)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1つ以上のルートミドルウェアを定義することができます。 そしてこのミドルウェアをあなたのアプリケーションのルーティングに追加することができます。
ルートミドルウェアは単なる "PHP callables" (たとえば クロージャー、 "ClassName::methodName" のような文字列だったり Silex のコールバック) です。
これらはルーティングが一致したときに呼び出されます。
ミドルウェアはルーティングのコールバックの前に呼び出されますが ``before`` フィルターより後です。
これは ``before`` フィルターがより優先されるからです。 - 次のセクションの ``before`` フィルターについてを見てください。

この仕組みは多くの場面で利用できます - たとえば、　"anonymous/logged user"　を制御する場合です::

    $mustBeAnonymous = function (Request $request) use ($app) {
        if ($app['session']->has('userId')) {
            return $app->redirect('/user/logout');
        }
    };

    $mustBeLogged = function (Request $request) use ($app) {
        if (!$app['session']->has('userId')) {
            return $app->redirect('/user/login');
        }
    };

    $app->get('/user/subscribe', function () {
        ...
    })
    ->middleware($mustBeAnonymous);

    $app->get('/user/login', function () {
        ...
    })
    ->middleware($mustBeAnonymous);

    $app->get('/user/my-profile', function () {
        ...
    })
    ->middleware($mustBeLogged);

複数個の ``middleware`` メソッドを1つのルーティングで呼ぶことができます。
ミドルウェアはルーティングに追加された順番で呼び出されます。

便利なことに、ルートミドルウェアはそのときのリクエストを引数として呼び出されます。

もしルーティングミドルウェアが Symfony Http レスポンスを返せば、全体のレンダリングを省略します。
そして次にミドルウェアが定義されていても呼び出しません。
ルーティングのコールバックで、 ``redirect`` メソッドを使いリダイレクトのレスポンスを返すことで他のページにリダイレクトすることができます。

ルートミドルウェアは Symfony Http レスポンスか null を返すことができます。
戻り値がそれ以外の場合は RuntimeException が投げられます。

前処理と後処理 (Before and after filters)
----------------------------------------------------------

Silex では、すべてのリクエストの前後でコードを走らせることが可能です。
``before`` フィルターと ``after`` フィルターを通して処理されます。利用方法はメソッドにクロージャーを渡すだけです::

    $app->before(function () {
        // set up
    });

    $app->after(function () {
        // tear down
    });

before フィルターは現在のリクエストにアクセスすることができます。そしてレスポンスを返却することでレンダリング全体のショートカットができます::

    $app->before(function (Request $request) {
        // redirect the user to the login screen if access to the Resource is protected
        if (...) {
            return new RedirectResponse('/login');
        }
    });

after フィルターはリクエストとレスポンスにアクセスすることができます::

    $app->after(function (Request $request, Response $response) {
        // tweak the Response
    });

.. note::

    フィルターは "マスター" のリクエストのときだけ機能します。

エラーハンドリング (Error handlers)
---------------------------------------------------

コードのどこかで例外が発生した際に、ユーザーにエラーページのようなものを表示したいことがあるでしょう。
これらエラーハンドラーがやることなのです。
ログ処理のような処理を追加してエラーハンドリングを使うこともできます。

エラーハンドラーを登録するために、 ``Exception`` を引数に持ち、レスポンスを返してくれる ``error`` メソッドにクロージャーを渡します::

    use Symfony\Component\HttpFoundation\Response;

    $app->error(function (\Exception $e, $code) use ($app) {
        return new Response('We are sorry, but something went terribly wrong.', $code);
    });

``$code`` 引数を使うことで特定のエラーだけを確認することもできます。そしてエラーの種類で処理を変えることができます::

    use Symfony\Component\HttpFoundation\Response;
    $app->error(function (\Exception $e, $code) {
        switch ($code) {
            case 404:
                $message = 'The requested page could not be found.';
                break;
            default:
                $message = 'We are sorry, but something went terribly wrong.';
        }

        return new Response($message, $code);
    });

ログ処理を行いたいなら、このためにエラーハンドラーを分けて使うことができます。
レスポンスのエラーハンドラーの前にエラーを登録しなければならないということだけに注意してください。
なぜならレスポンスが返されてしまうと、次のようなハンドラーは無視されてしまうからです。

.. note::

    Silex はエラーのログ処理を行うための `Monolog <https://github.com/Seldaek/monolog>`_
    プロバイダーも付いてきます。
    詳しくは *Providers* の章を参照してください。

.. tip::

    Silex には、デフォルトのエラーハンドラーが付いており、 **debug** を true にすることで、スタックトレースを含む詳細なエラーメッセージを表示します。 false の際には、シンプルなエラーメッセージを表示します。
    ``error()`` メソッドを通して登録したエラーハンドラーは常に優先されますが、デバッグモードが有効の際に表示する便利なエラーも次のようにすれば大丈夫です::

        use Symfony\Component\HttpFoundation\Response;

        $app->error(function (\Exception $e, $code) use ($app) {
            if ($app['debug']) {
                return;
            }

            // logic to handle the error and return a Response
        });

より早い段階でリクエストを破棄するために ``abort`` を使うときにもエラーハンドラーは呼ばれます::

    $app->get('/blog/show/{id}', function (Silex\Application $app, $id) use ($blogPosts) {
        if (!isset($blogPosts[$id])) {
            $app->abort(404, "Post $id does not exist.");
        }

        return new Response(...);
    });

リダイレクト (Redirects)
---------------------------

リダイレクト処理のレスポンスを返すことでどんなページにもリダイレクトすることができます。このリダイレクト処理のレスポンスは
``redirect`` メソッドで作成することができます::

    use Silex\Application;

    $app->get('/', function (Silex\Application $app) {
        return $app->redirect('/hello');
    });

この例では ``/`` から ``/hello`` にリダイレクトします。

ストリーミング
-------------------

ストリーミングのレスポンスを作成することができます。 これは送信されるデータをバッファリングできないときに重要です。

.. code-block:: php

    $app->get('/images/{file}', function ($file) use ($app) {
        if (!file_exists(__DIR__.'/images/'.$file)) {
            return $app->abort(404, 'The image was not found.');
        }

        $stream = function () use ($file) {
            readfile($file);
        };

        return $app->stream($stream, 200, array('Content-Type' => 'image/png'));
    });

大きいかたまりで送信したい場合は、 ``ob_fluch`` と ``flush`` を呼ばなければなりません。

.. code-block:: php

    $stream = function () {
        $fh = fopen('http://www.example.com/', 'rb');
        while (!feof($fh)) {
          echo fread($fh, 1024);
          ob_flush();
          flush();
        }
        fclose($fh);
    };

セキュリティ
--------------

アプリケーションを攻撃から防御する方法を確認しておきましょう。

エスケープ処理 (Escaping)
~~~~~~~~~~~~~~~~~~~~~~~~~~

ルーティング変数や、リクエストから受け取るされる GET/POST の変数など、ユーザーが入力した値は全て、正しくエスケープ処理を行う必要があります。
そうすることでクロスサイトスクリプティング(XSS)を防ぐことができます。

* **HTML のエスケープ処理**: HTML のエスケープ処理のために PHP は ``htmlspecialchars`` 関数 を用意してくれています。
  Silex ではこの関数へのショートカットとして ``escape`` メソッドを次のように使うことができます::

      $app->get('/name', function (Silex\Application $app) {
          $name = $app['request']->get('name');
          return "You provided the name {$app->escape($name)}.";
      });

  もし Twig テンプレートを使うのであれば、 Twig が用意してくれているエスケープのための記述を使ったり、自動エスケープ機能を使うべきです。

* **JSON のエスケープ処理**: もし JSON フォーマットのデータをアプリケーションをで提供するなら、 PHP の ``json_encode`` 関数を使います::

      use Symfony\Component\HttpFoundation\Response;

      $app->get('/name.json', function (Silex\Application $app) {
          $name = $app['request']->get('name');
          return new Response(
              json_encode(array('name' => $name)),
              200,
              array('Content-Type' => 'application/json')
          );
      });

コンソール
----------

Silex には Silex を最新バージョンにアップデートするための軽量なコンソールが用意されています。

あなたが利用している Silex のバージョンを知るためには、コマンドラインから ``silex.phar`` を呼び出して、引数に ``version`` を指定してください:

.. code-block:: text

    $ php silex.phar version
    Silex version 0a243d3 2011-04-17 14:49:31 +0200

最新バージョンかどうかを確認するためには、 ``check`` コマンドを実行します:

.. code-block:: text

    $ php silex.phar check

``silex.phar`` を最新バージョンに更新するためには、 ``update`` コマンドを実行します:

.. code-block::text

    $ php silex.phar update

これで自動的に新しい ``silex.phar`` を ``silex.sensiolabs.org`` からダウンロードして既存のものと置き換えてくれます。

Pitfalls
--------

Silex が思ったように動かないときがあるかもしれません。そういったときのためにここによくある動かない原因についてまとめておきましょう。

PHP の設定
~~~~~~~~~~~~~~~~~

PHP のバージョンによっては Phar の設定が制限されている場合があります。
その場合は、次のように設定することで解決するかもしれません。

.. code-block:: ini

    detect_unicode = Off
    phar.readonly = Off
    phar.require_hash = Off

もし Suhosin の PHP を使っている場合は、次の設定も行っておく必要があります:

.. code-block:: ini

    suhosin.executor.include.whitelist = phar

.. note::

    Ubuntu の Suhosin が入った PHP を使う場合はこの変更が必要です。 

Phar-Stub のバグ
~~~~~~~~~~~~~~~~~~~~~

インストールされている PHP のバージョンによっては Phar をインクルードしようとすると ``PharException`` が発生する場合があります。
そして ``Silex\Application`` が見つからないとも言われることもあります。
この場合は回避策として次のように書くことです::

    require_once 'phar://'.__DIR__.'/silex.phar/autoload.php';

この問題の的確な原因はまだ断定されていません。

ioncube ローダーのバグ
~~~~~~~~~~~~~~~~~~~~~~~~
iconcube ローダーは、エンコードされた PHP ファイルをデコードすることができるエクステンションです。
残念なことに(4.0.9 より前の)古いバージョンでは phar アーカイブでは動作しません。そのため 4.0.9 より新しいバージョンにアップグレードするか php.ini ファイルでコメントアウトするか削除し無効にしなければなりません:

.. code-block:: ini

    zend_extension = /usr/lib/php5/20090626+lfs/ioncube_loader_lin_5.3.so



IIS での設定
-----------------

もし Windows から IIS を利用している場合は、次の簡単な ``web.config`` ファイルを使うことができます:

.. code-block:: xml

    <?xml version="1.0"?>
    <configuration>
        <system.webServer>
            <defaultDocument>
                <files>
                    <clear />
                    <add value="index.php" />
                </files>
            </defaultDocument>
            <rewrite>
                <rules>
                    <rule name="Silex Front Controller" stopProcessing="true">
                        <match url="^(.*)$" ignoreCase="false" />
                        <conditions logicalGrouping="MatchAll">
                            <add input="{REQUEST_FILENAME}" matchType="IsFile" ignoreCase="false" negate="true" />
                        </conditions>
                        <action type="Rewrite" url="index.php" appendQueryString="true" />
                    </rule>
                </rules>
            </rewrite>
        </system.webServer>
    </configuration>
