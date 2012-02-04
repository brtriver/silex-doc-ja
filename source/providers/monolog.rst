MonologServiceProvider
==========================

*MonologServiceProvider* を使うことで Jordi Boggiano さんの
`Monolog <https://github.com/Seldaek/monolog>`_ ライブラリを通して標準のログ機能を提供します。

リクエストやエラーを記録しアプリケーションにデバッグを記録するようになります。
そのため ``var_dump`` をもう使う必要はなくなります。
これからはさらに一歩進んで ``tail -f`` コマンドを使うことができるようになります。

パラメーター
------------

* **monolog.logfile**: ログファイルの場所。

* **monolog.class_path** (オプション): Monolog ライブラリを設置したパス。

* **monolog.level** (オプション): ``DEBUG`` に標準で記録するログのレベル。
  ``Logger::DEBUG``, ``Logger::INFO``, ``Logger::WARNING``, ``Logger::ERROR`` のどれかを指定します。 
  ``DEBUG`` はどんなものでも記録します。 ``INFO`` は ``DEBUG`` 意外のものを記録します。  

* **monolog.name** (オプション): Monolog チャンネルの名前。　標準は ``myapp`` 。

サービス
--------

* **monolog**: monolog のログインスタンス。

  利用方法::

    $app['monolog']->addDebug('Testing the Monolog logging.');

* **monolog.configure**: 引数としてロガーを取る保護されたクロージャー。標準の振る舞いを使いたくない場合は上書きすることができます。

登録
-----------

``vendor/monolog`` ディレクトリに *Monolog* のコピーを置いていることを確認してください::

    $app->register(new Silex\Provider\MonologServiceProvider(), array(
        'monolog.logfile'       => __DIR__.'/development.log',
        'monolog.class_path'    => __DIR__.'/vendor/monolog/src',
    ));

.. note::

    Monolog は ``silex.phar`` ファイルの中にコンパイルされていません。自分自身でアプリケーションに Monolog のコピーを追加する必要があります。

Usage
-----

MonologServiceProvider は ``monolog`` サービスを提供します。
このサービスはどんなエラーレベルも ``addDebug()``,``addInfo()``, ``addWarning()`` そして ``addError()`` を通してログを追加することができます::

    use Symfony\Component\HttpFoundation\Response;

    $app->post('/user', function () use ($app) {
        // ...

        $app['monolog']->addInfo(sprintf("User '%s' registered.", $username));

        return new Response('', 201);
    });

より詳しい情報については、    `Monolog ドキュメント
<https://github.com/Seldaek/monolog>`_ を参照してください.
