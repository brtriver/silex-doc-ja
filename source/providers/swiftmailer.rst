SwiftmailerServiceProvider
===============================

*SwiftmailerServiceProvider* は `Swift Mailer <http://swiftmailer.org>`_ ライブラリを使用した
メール送信のためのサービスを提供します。

``mailer`` サービスを使用し、簡単にメールを送信することができます。
デフォルトでは、SMTP プロトコルでのメール送信を試みます。

パラメーター
--------------

* **swiftmailer.options**: デフォルトの SMTP 送信の設定を記述した配列です。

  次のオプションを指定することができます:

  * **host**: SMTP ホスト名, デフォルトは 'localhost' です。
  * **port**: SMTP ポート, デフォルトは 25 番です。
  * **username**: SMTP ユーザ名, デフォルトは空文字列です。
  * **password**: SMTP パスワード, デフォルトは空文字列です。
  * **encryption**: SMTP 暗号, デフォルトは null です。
  * **auth_mode**: SMTP 認証方法, デフォルトは null です。

  使用例 ::

    $app['swiftmailer.options'] = array(
        'host' => 'host',
        'port' => '25',
        'username' => 'username',
        'password' => 'password',
        'encryption' => null,
        'auth_mode' => null
    );

サービス
------------

* **mailer**: メーラーのインスタンスです。

  使用例 ::

    $message = \Swift_Message::newInstance();

    // ...

    $app['mailer']->send($message);

* **swiftmailer.transport**: メール送信のトランスポートです。
  デフォルトは、 ``Swift_Transport_EsmtpTransport`` 。

* **swiftmailer.transport.buffer**: トランスポートで使用される
  ストリームバッファ。

* **swiftmailer.transport.authhandler**: トランスポートで使用される
  認証ハンドラー。 CRAM-MD5, login, plaintext をデフォルトで試します。

* **swiftmailer.transport.eventdispatcher**: Swiftmailer で使用される内部のイベントディスパッチャー。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\SwiftmailerServiceProvider());

.. note::
    SwiftMailerは"fat" Silexに付属し、標準サイズのSilexには付属しません。
    もしComposerを使用している場合には、 ``composer.json`` ファイルに依存関係を記述してください。

    .. code-block:: json

        "require": {
            "swiftmailer/swiftmailer": ">=4.1.2,<4.2-dev"
        }

使用方法
-------------

Swiftmaielr プロバイダーは、 ``mailer`` サービスを提供します。 ::

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

トレイト
---------

``Silex\Application\SwiftmailerTrait`` は以下のショートカットを追加します。

* **mail**: メールを送信します。

.. code-block:: php

    $app->mail(\Swift_Message::newInstance()
        ->setSubject('[YourSite] Feedback')
        ->setFrom(array('noreply@yoursite.com'))
        ->setTo(array('feedback@yoursite.com'))
        ->setBody($request->get('message')));

詳細は、 `Swift Mailer documentation
<http://swiftmailer.org>`_
を参照してください。
