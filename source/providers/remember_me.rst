RememberMeServiceProvider
=========================

*RememberMeServiceProvider* は "Remember-Me" という認証を 
*SecurityServiceProvider* に追加します。


パラメータ
----------

無し

サービス
--------

無し

.. note::

    サービスプロバイダは内部で使用するための他のサービスをたくさん定義します。しかし、それらをカスタマイズする必要がある場合はあまりありません。

登録
-----------

このサービスプロバイダーを登録する前に、
*SecurityServiceProvider* を登録する必要があります。 ::

    $app->register(new Silex\Provider\SecurityServiceProvider());
    $app->register(new Silex\Provider\RememberMeServiceProvider());

    $app['security.firewalls'] = array(
        'my-firewall' => array(
            'pattern'     => '^/secure$',
            'form'        => true,
            'logout'      => true,
            'remember_me' => array(
                'key'                => 'Choose_A_Unique_Random_Key',
                'always_remember_me' => true,
                /* Other options */
            ),
            'users' => array( /* ... */ ),
        ),
    );

オプション
-----------

* **key**: トークン生成に使用するための秘密鍵(値にはランダムな文字列を使用すべきです。)

* **name**: クッキー名 (標準では、 ``REMEMBERME`` です。)

* **lifetime**: クッキーライフタイム (標準では、 ``31536000`` ~ 1年です。).

* **path**: クッキーのパス (標準では、 ``/`` です。)

* **domain**: クッキードメイン (標準では、 ``null`` = リクエストドメインです。)

* **secure**: クッキーがセキュアかどうか (標準では、 ``false`` です。)

* **httponly**: クッキーがHTTPのみかどうか (標準では、 ``true`` です。)

* **always_remember_me**: remember meを有効にするかどうか (標準では、 ``false`` です。)

* **remember_me_parameter**: remember_meをログイン時に有効にするためのリクエストパラメーターの名前
  ログインフォームにチェックボックスを追加するためのものです。より詳しい情報については、 `Symfonyクックブック <http://symfony.com/doc/current/cookbook/security/remember_me.html>`_ を参照してください。 (標準では、 ``_remember_me`` です。)
