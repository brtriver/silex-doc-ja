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

``Silex\Application``　のエイリアスとして ``Application`` が利用できます。

もうひとつあなたがやらなければならないことは、サーバーの設定を行うことです。
もしApacheを使っていて ``.htaccess`` を利用することができるのならば次のように設定してください。

.. code-block:: apache

    <IfModule mod_rewrite.c>
        Options -MultiViews

        RewriteEngine On
        #RewriteBase /path/to/app
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteRule ^(.*)$ index.php [QSA,L]
    </IfModule>

.. note::

　　　　もし、 Silex を配置するディレクトリが Webのドキュメントルートでない場合は、　``RewriteBase`` のコメントを外し
    Webのドキュメントルートからの相対パスであなたのディレクトリ構造に合わせたパスを指定するようにしてください。

ルーティング (Routing)
-----------------------

Silex ではルーティングと、そのルーティングに一致したときに実行されるコントローラーを定義します

ルーティングのパターンは次のような構成になっています:

* *パターン (Pattern)*: ルーティングパターンでリソースへのパスを定義します。
  パターンは可変部分を含むことができ、可変部分において正規表現を使った必須項目を設定することができます。

* *メソッド (Method)*: 以下の HTTPメソッド のどれかを指定します: ``GET``, ``POST``, ``PUT``
  ``DELETE``. これはリソースとの相互作用を表しています。 
  一般的には、 ``GET`` と ``POST`` だけが利用されますが、他のメソッドも使うことが可能です。

コントローラーはクロージャーを次のように使うことで定義できます::

    function () {
        // do something
    }

クロージャーは定義の外部から状態を取り込むことができる無名関数のことです。
これはグローバル変数とは異なります、なぜなら外部の状態はグローバルなものではないからです。
たとえば、メソッドの中にクロージャーを定義することができ、メソッドのローカル変数を取り込むことができます。

.. note::

    スコープを取り込まないクロージャーはラムダのようだと言われます。
    なぜならPHPの無名関数はすべて ``Closure`` クラスのインスタンスであり、区別することができないからです。

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

    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    $app->get('/blog/show/{id}', function ($id) use ($blogPosts) {
        if (!isset($blogPosts[$id])) {
            throw new NotFoundHttpException();
        }

        $post = $blogPosts[$id];

        return  "<h1>{$post['title']}</h1>".
                "<p>{$post['body']}</p>";
    });

ルーティングはクロージャーに渡される ``{id}`` という変数を定義しています。 

見てわかるように、 もし記事が存在しない場合は ``NotFoundHttpException`` を投げます。
後ほど、どのようにハンドリングしているかを説明します。

POST ルーティングの例
~~~~~~~~~~~~~~~~~~~~~~~

POSTルーティングはリソースの生成を意味します。
この例となるのがフィードバック形式です。
ここでは `Swift Mailer
<http://swiftmailer.org/>`_ を使うので ``Swift Mailer`` のコピーが　``vendor/swiftmailer``　に置かれているとします。

::

    require_once __DIR__.'/vendor/swiftmailer/lib/swift_required.php';

    use Symfony\Component\HttpFoundation\Response;

    $app->post('/feedback', function () use ($app) {
        $request = $app['request'];

        $message = \Swift_Message::newInstance()
            ->setSubject('[YourSite] Feedback')
            ->setFrom(array('noreply@yoursite.com'))
            ->setTo(array('feedback@yoursite.com'))
            ->setBody($request->get('message'));

        $transport = \Swift_MailTransport::newInstance();
        $mailer = \Swift_Mailer::newInstance($transport);
        $mailer->send($message);

        return new Response('Thank you for your feedback!', 201);
    });

かなり単純な方法です。 Swift Mailer ライブラリをインクルードしメッセージを作成しそれを送信しています。

ここで ``request``サービスは 配列のキーを使って取得しています。
サービスのことについてもっと知りたいのであれば、 *Services* の章を参照してください。
リクエストは `Request
<http://api.symfony.com/2.0/Symfony/Component/HttpFoundation/Request.html>`_ のインスタンスであり,
リクエストの ``get`` メソッドを使うことで変数を取得することができます。

文字列を返す代わりに `Response
<http://api.symfony.com/2.0/Symfony/Component/HttpFoundation/Response.html>`_ のインスタンスを返すことができます。
また、HTTPのステータスコードを設定することもでき、今回の場合であれば ``201 Created`` が設定されています。

.. note::

    Silexはいつも ``Response`` を内部で利用し、 HTTPのステータスコードを ``200 OK`` で、文字列を レスポンスのインスタンスに変換しています。 

他のメソッド
~~~~~~~~~~~~~

ほとんどのHTTPメソッドのためのコントローラーを作ることが可能です。 ただ次の中のメソッドから1つを利用すれば良いだけです:
``get``, ``post``, ``put``, ``delete``. 
また、 ``match`` メソッドを利用することもでき、この場合はすべてのメソッドに一致します。

::

    $app->put('/blog', function () {
        ...
    });

.. note::

    ルーティングがどのような順番で定義されたかはとても重要です。
    最初に一致したルーティングが利用されるからです。そのため、汎用的なルーティングは一番下に定義するようにしてください。

ルーティング変数
~~~~~~~~~~~~~~~~~~


前に説明したように、次のようにルーティングにおいて変数を定義することができます::

    $app->get('/blog/show/{id}', function ($id) {
        ...
    });

2つ以上の変数部分を定義することもできますし、変数部分の名前で一致させた引数をクロージャーに渡すことができます。

::

    $app->get('/blog/show/{postId}/{commentId}', function ($postId, $commentId) {
        ...
    });

説明していませんでしたが、次のように引数の順番を入れ替えることだってできます。::

    $app->get('/blog/show/{postId}/{commentId}', function ($commentId, $postId) {
        ...
    });

ルーティングで取得される変数の変換
~~~~~~~~~~~~~~~~~~~~~~~~~~

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

次のコードは ``\id+`` で数値に一致するようにしているので ``id`` 引数が数字であることがわかります::


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

標準の値
~~~~~~~~~~~~~~

``Controller`` オブジェクトの ``value`` メソッドを呼ぶことでどんなルーティングでも標準の値を定義することができます。

::

    $app->get('/{pageName}', function ($pageName) {
        ...
    })
    ->value('pageName', 'index');

この例では ``/`` がルーティングに一致し、 そして ``pageName`` 変数は ``index`` になります。

名前ルーティング (Named routes)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

エクステンションの中には名前ルーティングを使うことができるものがあります (``UrlGenerator``など)。
標準では Silex はあなたの代わりにルーティング名を生成してくれます。しかし、これらは利用されません。
ルーティングメソッドによって返される``Controller`` オブジェクトの ``bind`` メソッドを呼び出すことでルーティングに名前を付けることができます。

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

    使おうとしているエクステンションが ``RouteCollection`` を利用しているときのみ名前ルーティングは意味があります。

前処理と後処理
------------------------

すべてのリクエストの前後でコードを走らせることが可能です。
beforeフィルターとafterフィルターを通して処理されます。利用方法はメソッドにクロージャーを渡すだけです::

    $app->before(function () {
        // set up
    });

    $app->after(function () {
        // tear down
    });

エラーハンドリング
-------------------

コードのどこかで例外が発生するとユーザーにエラーページのようなもので表示したいことがあるでしょう。
これらエラーハンドラーがやることなのです。
ログ処理のような処理を追加してエラーハンドリングを使うこともできます。

エラーハンドラーを登録するために、 ``Exception`` を引数に持ち、レスポンスを返してくれる ``error`` メソッドにクロージャーを渡します::

    use Symfony\Component\HttpFoundation\Response;

    $app->error(function (\Exception $e) {
        return new Response('We are sorry, but something went terribly wrong.', 500);
    });

``instanceof`` を使うことで特定のエラーだけを確認することもできます。そしてエラーの種類で処理を変えることができます::

    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\HttpKernel\Exception\HttpException;
    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    $app->error(function (\Exception $e) {
        if ($e instanceof NotFoundHttpException) {
            return new Response('The requested page could not be found.', 404);
        }

        $code = ($e instanceof HttpException) ? $e->getStatusCode() : 500;
        return new Response('We are sorry, but something went terribly wrong.', $code);
    });

ログ処理を行いたいなら、このためにエラーハンドラーを分けて使うことができます。
レスポンスのエラーハンドラーの前にエラーを登録しなければならないということだけに注意してください。
なぜならレスポンスが返されてしまうと、次のようなハンドラーは無視されてしまうからです。

.. note::

    Silex はエラーのログ処理を行うために `Monolog <https://github.com/Seldaek/monolog>`_
    を利用するためのエクステンションを利用することができます。
    詳しくは *Extensions* の章を参照してください。

リダイレクト
------------

リダイレクト処理のレスポンスを返すことでどんなページにもリダイレクトすることができます。このリダイレクト処理は
``redirect`` メソッドを呼ぶことで作成することができます::

    $app->get('/', function () use ($app) {
        return $app->redirect('/hello');
    });

この例では ``/`` から ``/hello`` にリダイレクトしようとします。

セキュリティー
--------------

アプリケーションをアタックなどの攻撃から防御する方法を確認しておきましょう。

エスケープ処理
~~~~~~~~~~~~~~

(ルーティングから取得される GET/POST の変数も含め)ユーザー入力した値はどんなものであれアプリケーションを通して出力するときは、正しくエスケープ処理を行う必要があります。
そうすることでクロスサイトスクリプティング(XSS)を防ぐことができます。

* **HTMLのエスケープ処理**: HTMLのエスケープ処理のために PHP は ``htmlspecialchars`` 関数　を用意してくれています。
  Silex ではこの関数へのショートカットとして ``escape`` メソッドを次のように使うことができます::

      $app->get('/name', function () use ($app) {
          $name = $app['request']->get('name');
          return "You provided the name {$app->escape($name)}.";
      });

  もし Twigテンプレートを使うのであれば、Twigが用意してくれているエスケープのための記述を使ったり、自動エスケープ機能を使うべきです。

* **JSONのエスケープ処理**: もし JSON フォーマットのデータをアプリケーションをで提供するなら、 PHP の ``json_encode`` 関数を使います::

      use Symfony\Component\HttpFoundation\Response;

      $app->get('/name.json', function () use ($app) {
          $name = $app['request']->get('name');
          return new Response(
              json_encode(array('name' => $name)),
              200,
              array('Content-Type' => 'application/json')
          );
      });

アプリケーションの再利用
-------------------------

あなたが作成したアプリケーションをより再利用しやすくするためには、次のように ``run`` メソッドを呼ぶ代わりに ``$app`` 変数を返すようにします::

    // blog.php
    require_once __DIR__.'/silex.phar';

    $app = new Silex\Application();

    // あなたのブログアプリケーションを定義
    $app->get('/post/{id}', function ($id) { ... });

    // アプリケーションのインスタンスを返す
    return $app;

返されたアプリケーションのインスタンスは次のようにして使うことができます::

    $app = require __DIR__.'/blog.php';
    $app->run();

このパターンを利用することで、他のどのアプリケーションの中でもこのアプリケーションを簡単に "マウント" することができます。::

    $blog = require __DIR__.'/blog.php';

    $app = new Silex\Application();
    $app->mount('/blog', $blog);

    // 中心となるアプリケーションを定義

    $app->run();

これで、 すでに定義している他のルーティングに加えて ``/blog/post/{id}`` というルーティングでブログの投稿処理を行うことができるようになりました。

もし大量のアプリケーションをマウントするのであれば、毎回のリクエストでこれらすべてのアプリケーションを読み込むことによるオーバーヘッドを避けたいことがあるでしょう。
その場合は、 ``LazyApplication`` ラッパーを使うことでオーバーヘッドを避けることができます::

    $blog = new Silex\LazyApplication(__DIR__.'/blog.php');

コンソール
----------

Silex には Silex を最新バージョンにアップデートするための軽量なコンソールが用意されています。

あなたが利用している Silex のバージョンを知るためには、 ``silex.phar`` をコマンドラインから引数無しで呼び出すだけです:

.. code-block:: text

    $ php silex.phar
    Silex version 0a243d3 2011-04-17 14:49:31 +0200

最新バージョンかどうかを確認するためには、 ``check`` コマンドを実行します:

.. code-block:: text

    $ php silex.phar check

``silex.phar`` を最新バージョンに更新するためには、 ``update`` コマンドを実行します:

.. code-block::text

    $ php silex.phar update

これで自動的に新しい ``silex.phar`` を ``silex-project.org`` からダウンロードして既存のものと置き換えてくれます。

Pitfalls
--------

Silex が思ったように動かないときがあるかもしれません。そういったときのためにここによくある動かない原因についてまとめておきましょう。

PHP の設定
~~~~~~~~~~~~~~~~~

PHPのバージョンによってはPharの設定が制限されている場合があります。
その場合は、次のように設定することで解決するかもしれません:

.. code-block:: ini

    phar.readonly = Off
    phar.require_hash = Off

もし Suhosin のPHPを使っている場合は、次の設定も行っておく必要があります:

.. code-block:: ini

    suhosin.executor.include.whitelist = phar

Phar-Stub のバグ
~~~~~~~~~~~~~~~~~~~~~

インストールされているPHPのバージョンによっては Phar をインクルードしようとすると ``PharException`` が発生する場合があります。
そして ``Silex\Application`` が見つからないとも言われることもあります。
この場合は回避策として次のように書くことです:

    require_once 'phar://'.__DIR__.'/silex.phar/autoload.php';

この問題の的確な原因はまだ断定されていません。

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
