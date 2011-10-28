SwiftmailerServiceProvider
==========================

*SwiftmailerServiceProvider* は `Swift Mailer<http://swiftmailer.org>` ライブラリを使用した
メール送信のサービスを提供します。

``mailer`` サービスを使用し、簡単にメールを送信することができます。
デフォルトでは、SMTP プロトコルでのメール送信を試みます。

パラメーター
----------

* **swiftmailer.options**: デフォルトの SMTP 送信の設定のための
  オプションです。

  次のオプションを指定することができます:

  * **host**: SMTP ホスト名, デフォルトは 'localhost' です。
  * **port**: SMTP ポート, デフォルトは 25 番です。
  * **username**: SMTP ユーザ名, デフォルトは空文字列です。
  * **password**: SMTP パスワード, デフォルトは空文字列です。
  * **encryption**: SMTP 暗号, デフォルトは null です。
  * **auth_mode**: SMTP 認証方法, デフォルトは null です。

* **swiftmailer.class_path** (optional): Swift Mailer のライブラリを
  格納しているパス。

サービス
--------

* **mailer**: メイラーのインスタンスです。

  Example usage::

    $message = \Swift_Message::newInstance();

    // ...

    $app['mailer']->send($message);

* **swiftmailer.transport**: メール送信のトランスポートです。
  デフォルトは、 ``Swift_Transport_EsmtpTransport`` 。

* **swiftmailer.transport.buffer**: トランスポートで使用される
  ストリームバッファ。

* **swiftmailer.transport.authhandler**: トランスポートで使用される
  認証ハンドラー。 CRAM-MD5, login, plaintext をデフォルトで使用します。

* **swiftmailer.transport.eventdispatcher**: Swiftmailer で使用される
  内部のイベントディスパッチャー。

登録
-----------

``vendor/swiftmailer`` ディレクトリーに *Swift Mailer* のコピーを配置してください。
``/lib/classes`` へのクラスパスを指定してください。

::

    $app->register(new Silex\Provider\SwiftmailerServiceProvider(), array(
        'swiftmailer.class_path'  => __DIR__.'/vendor/swiftmailer/lib/classes',
    ));

.. note::

    Swift Mailer は ``silex.phar`` ファイルにはコンパイルされていません。
    使用する際には、Swift Mailer をアプリケーションに自分で追加してください。

使用方法
-----

Swiftmaielr プロバイダーは、 ``mailer`` サービスを提供します。

::

    $app->post('/feedback', function () use ($app) {
        $request = $app['request'];

        $message = \Swift_Message::newInstance()
            ->setSubject('[YourSite] Feedback')
            ->setFrom(array('noreply@yoursite.com'))
            ->setTo(array('feedback@yoursite.com'))
            ->setBody($request->get('message'));

        $app['mailer']->send($message);

        return new Response('Thank you for your feedback!', 201);
    });

詳細は、 `Swift Mailer documentation
<http://swiftmailer.org>`_を参照してください.
