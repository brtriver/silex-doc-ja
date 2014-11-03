MonologServiceProvider
==========================

*MonologServiceProvider* を使うことで Jordi Boggiano さんの
`Monolog <https://github.com/Seldaek/monolog>`_ ライブラリを通して標準のログ機能が使用できるようになります。

Monologを使うことで、リクエストやエラーを記録することができるようになります。
これによってプロダクション環境のアプリケーションのデバッグや監視を行えるようになります。

パラメーター
------------

* **monolog.logfile**: ログが書き込まれるファイルの場所。

* **monolog.level** (オプション): ``DEBUG`` に標準で記録するログのレベル。
  ``Logger::DEBUG``, ``Logger::INFO``, ``Logger::WARNING``, ``Logger::ERROR`` のどれかを指定します。 
  ``DEBUG`` はどんなものでも記録します。 ``INFO`` は ``DEBUG`` 以外の全てのものを記録します。  
  Logger::定数の代わりに各レベルの文字列を与えても構いません。例: "DEBUG", "INFO", "WARNING", "ERROR"。

* **monolog.name** (オプション): Monolog チャンネルの名前。　標準は ``myapp`` です。

* **monolog.exception.logger_filter** (オプション): どの例外をログに残すべきかの無名関数のフィルタ

サービス
--------

* **monolog**: monolog のログインスタンス。

  利用方法::

    $app['monolog']->addDebug('Testing the Monolog logging.');

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\MonologServiceProvider(), array(
        'monolog.logfile' => __DIR__.'/development.log',
    ));

.. note::

    Monologは"fat" Silexに付属し、標準サイズのSilexには付属しません。
    もしComposerを使用している場合には、 ``composer.json`` ファイルに依存関係を記述してください。:

    .. code-block:: json

        "require": {
            "monolog/monolog": ">=1.0.0"
        }

使用方法
-----------

MonologServiceProvider は ``monolog`` サービスを提供します。
このサービスはエラーレベルごとに、それぞれ ``addDebug()``, ``addInfo()``, ``addWarning()`` そして ``addError()`` というメソッドを通してログを追加することができます。 ::

    use Symfony\Component\HttpFoundation\Response;

    $app->post('/user', function () use ($app) {
        // ...

        $app['monolog']->addInfo(sprintf("User '%s' registered.", $username));

        return new Response('', 201);
    });

設定
-------------

使用前に、 ``monolog`` サービスを拡張することによって
好みに応じて(ハンドラの追加や変更などの)Monologの設定を変更できます。 ::

    $app['monolog'] = $app->extend('monolog', function($monolog, $app) {
        $monolog->pushHandler(...);

        return $monolog;
    };

トレイト
--------

``Silex\Application\MonologTrait`` は以下のショートカットを追加します。

* **log**: メッセージを記録します。

.. code-block:: php

    $app->log(sprintf("User '%s' registered.", $username));

より詳しい情報については、 `Monolog ドキュメント
<https://github.com/Seldaek/monolog>`_ を参照してください。

commit: 10535580b28f9a16c8e2cb5af7e5d39e8c1ca3c9
original: https://github.com/silexphp/Silex/blob/master/doc/providers/monolog.rst
