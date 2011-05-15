SessionExtension
================

*SessionExtension* を使うことで永続的にリクエスト間でデータを保存するためのサービスを提供することができます。

パラメーター
------------

* **session.storage.options**: ``session.storage`` サービスのコンストラクタに渡すオプションの配列。

  標準の ``NativeSessionStorage`` の場合、使用可能なオプションは以下の通りです:

  * **name**: Cookie の名前 (標準は _SESS)
  * **id**: セッション ID (標準は null)
  * **lifetime**: Cookie のライフタイム
  * **path**: Cookie のパス
  * **domain**: Cookie のドメイン
  * **secure**: Cookie のセキュア設定 (HTTPS)
  * **httponly**: Cookie が httpオンリーかどうかの設定

  しかしながら、これらの全てはオプションです。　セッションはブラウザを開いている間保持されます。
  これを上書きするためには、 ``lifetime`` オプションを設定します。

  However, all of these are optional. Sessions last as long as the browser
  is open. To override this, set the ``lifetime`` option.


サービス
--------

* **session**: Symfony2　の `Session 
  <http://api.symfony.com/2.0/Symfony/Component/HttpFoundation/Session.html>`_ のインスタンス。

* **session.storage**: セッションデータの永続化のために利用されるサービス。 標準は `NativeSessionStorage    <http://api.symfony.com/2.0/Symfony/Component/HttpFoundation/SessionStorage/NativeSessionStorage.html>`_


登録
-----------

::

    $app->register(new Silex\Extension\SessionExtension());

使い方
-------

セッションのエクステンションは ``session`` サービスを提供します。以下にユーザーを認証しそのユーザーのためにセッションを作成するサンプルです::

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
