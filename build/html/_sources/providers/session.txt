SessionServiceProvider
=============================

*SessionServiceProvider* を使うことで永続的にリクエスト間でデータを保存するためのサービスを使用することができるようになります。

パラメーター
------------

* **session.storage.save_path** (オプション): ``NativeFileSessionStorage`` へのパスです。 標準は ``sys_get_temp_dir()`` の値です。

* **session.storage.options**: ``session.storage`` サービスのコンストラクタに渡されたオプションの配列です。

  標準の `NativeFileSessionStorage <http://api.symfony.com/master/Symfony/Component/HttpFoundation/Session/Storage/NativeSessionStorage.html>`_ の場合の便利なオプションは以下の通りです。

  * **name**: Cookie の名前 (標準は _SESS)
  * **id**: セッション ID (標準は null)
  * **cookie_lifetime**: Cookie のライフタイム
  * **cookie_path**: Cookie のパス
  * **cookie_domain**: Cookie のドメイン
  * **cookie_secure**: Cookie のセキュア設定 (HTTPS)
  * **cookie_httponly**: Cookie が httpのみかどうかの設定

  しかしながら、これらの全てはオプションです。標準のセッションのライフタイムは 1800 秒 ( 30 分) です。
  これを上書きするためには、 ``lifetime`` オプションを設定します。

  使用可能な全てのオプションについては `PHP
  <http://php.net/session.configuration>`_ の公式ドキュメントを見てください。

* **session.test**: セッションをシミュレートするかどうか(機能テストを書く際に便利です)。

サービス
--------

* **session**: Symfony2　の `Session 
  <http://api.symfony.com/master/Symfony/Component/HttpFoundation/Session/Session.html>`_ のインスタンス。

* **session.storage**: セッションデータの永続化のために利用されるサービス。 

* **session.storage.handler**: データアクセスのために ``session.storage`` によって使用されるサービス。 標準では `NativeFileSessionHandler
  <http://api.symfony.com/master/Symfony/Component/HttpFoundation/Session/Storage/Handler/NativeFileSessionHandler.html>`_
  のストレージハンドラーに設定されています。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\SessionServiceProvider());

使い方
-------

セッションのプロバイダーは ``session`` サービスを提供します。以下はユーザーを認証しそのユーザーのためにセッションを作成するサンプルです。 ::

    use Symfony\Component\HttpFoundation\Response;

    $app->get('/login', function () use ($app) {
        $username = $app['request']->server->get('PHP_AUTH_USER', false);
        $password = $app['request']->server->get('PHP_AUTH_PW');

        if ('igor' === $username && 'password' === $password) {
            $app['session']->set('user', array('username' => $username));
            return $app->redirect('/account');
        }

        $response = new Response();
        $response->headers->set('WWW-Authenticate', sprintf('Basic realm="%s"', 'site_login'));
        $response->setStatusCode(401, 'Please sign in.');
        return $response;
    });

    $app->get('/account', function () use ($app) {
        if (null === $user = $app['session']->get('user')) {
            return $app->redirect('/login');
        }

        return "Welcome {$user['username']}!";
    });

カスタムセッションの設定
-----------------------------

もし、あなたのシステムがカスタムセッション設定を使用している場合（PHPエクステンションのredisハンドラーのようなもの）、 ``session.storage.handler`` をnullにセットすることで、NativeFileSessionHandler を無効にする必要があります。
また ``session.save_path`` の設定を行う必要があります。

.. code-block:: php

    $app['session.storage.handler'] = null;


commit: 81a08269268e5e2adb250c4a801f021face5ab4a
original: https://github.com/silexphp/Silex/blob/master/doc/providers/session.rst
