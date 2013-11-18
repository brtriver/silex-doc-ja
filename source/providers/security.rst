SecurityServiceProvider
=======================

*SecurityServiceProvider* は、アプリケーションの認証と認可を管理します。

パラメータ
-------------

* **security.hide_user_not_found** (オプション): ユーザーが見つからなかった場合に例外を投げるか否かを設定します。 標準ではtrueです。


サービス
--------

* **security**: securityプロバイダへの主なアクセス源。現在のユーザーのトークンを入手したい場合は、これを使ってください。

* **security.authentication_manager**: `AuthenticationProviderManager
  <http://api.symfony.com/master/Symfony/Component/Security/Core/Authentication/AuthenticationProviderManager.html>`_ のインスタンス。認証を担当しています。

* **security.access_manager**: `AccessDecisionManager
  <http://api.symfony.com/master/Symfony/Component/Security/Core/Authorization/AccessDecisionManager.html>`_ のインスタンス。認可を担当しています。

* **security.session_strategy**: 認証に使われるセッションの戦略を決定します。(標準では、migration strategyです。)。

* **security.user_checker**: 認証の後にユーザーフラグをチェックするかどうかを決定します。

* **security.last_error**: リクエストが与えられた際に発生した最後の認証エラーを返します。

* **security.encoder_factory**: ユーザーパスワードのエンコード方法を指定します。(標準ではすべてのユーザーに対して、digestアルゴリズムを適用します。)

* **security.encoder.digest**: 全てのユーザーに対して使用する標準のエンコードを指定します。

.. note::

    サービスプロバイダーは内部で使用されている他のたくさんのサービスの振舞を決定します。しかし、その内部の振舞をカスタマイズする必要性はあまりないでしょう。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\SecurityServiceProvider(), array(
        'security.firewalls' => // 詳しくは下で
    ));

.. note::

    Symfony Securityコンポーネントは"fat" Silexに付属し、標準サイズのSilexには付属しません。
    もしComposerを使用している場合には、 ``composer.json`` ファイルに依存関係を記述してください。

    .. code-block:: json

        "require": {
            "symfony/security": "~2.3"
        }

.. caution::

    セキュリティ機能はアプリケーションが起動した後でのみ使用可能です。
    よって、リクエストの処理外でセキュリティ機能を使いたい場合は、最初に  ``boot()`` を忘れずに呼びましょう。 ::

        $application->boot();

.. caution::

    もし認証されたユーザーに対するフォームを使用するなら、 ``SessionServiceProvider`` を有効にする必要があります。

使用方法
----------

Symfony Securityコンポーネントは強力です。それらについて詳しく知りたい場合は `Symfony2 Security documentation
<http://symfony.com/doc/2.3/book/security.html>`_ を読んでください。

.. tip::

    securityの設定が期待するものと異なる振舞になってしまったら、ログ処理(Monologエクステンションのインスタンスとともに)を有効にしましょう。 そうすることで、Securityコンポーネントは、たくさんの有益な情報を記録してくれます。

以下はいくつかの通常の使い方レシピのリストです。

現在のユーザーへのアクセス
~~~~~~~~~~~~~~~~~~~~~~~~~~

現在のユーザー情報はトークンに保存されています。これは ``security`` サービスを通してアクセス可能です。 ::

    $token = $app['security']->getToken();

ユーザー情報が何もなかった場合、トークンは ``null`` になります。
ユーザーが既知であった場合、 ``getUser()`` を呼ぶことでユーザーを取得できます。 ::

    if (null !== $token) {
        $user = $token->getUser();
    }

ユーザーは ``__toString()`` メソッドや `UserInterface
<http://api.symfony.com/master/Symfony/Component/Security/Core/User/UserInterface.html>`_ のインスタンスを通して文字列やオブジェクトになれます。

HTTP認証を使用したパスのセキュリティ対策
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``/admin/`` 以下の安全なURLへの、HTTPのベーシック認証を用いた設定は下のように行えます。 ::

    $app['security.firewalls'] = array(
        'admin' => array(
            'pattern' => '^/admin',
            'http' => true,
            'users' => array(
                // 元のパスワードはfooです。
                'admin' => array('ROLE_ADMIN', '5FZ2Z8QIkA7UTZ4BYkoC+GsReLf569mSKDsfods6LYQ8t+a8EW9oaircfMpmaLbPBh4FOBiiFyLfuZmTSUwzZg=='),
            ),
        ),
    );

``pattern`` は正規表現で記述します。(これは `RequestMatcher
<http://api.symfony.com/master/Symfony/Component/HttpFoundation/RequestMatcher.html>`_ のインスタンスでも代用できます。)
``http`` 設定はHTTPベーシック認証を使うかどうか、 ``users`` は許可されたユーザーがどのようなものかを定義します。

全てのユーザーは次の情報によって定義されます。

* ロールか各ユーザーのロールの配列(ロールは ``ROLE_`` から始まる任意の文字列です。)

* ユーザーのエンコードされたパスワード

.. caution::

    全てのユーザーは少なくともひとつのロールを持っている必要があります。

エクステンションの標準設定ではエンコードされたパスワードが強制されます。
パスワードからエンコードされたパスワードを生成するには、 ``security.encoder_factory`` サービスを使用してください。 ::

    // UserInterfaceインスタンス用のエンコーダーを探す
    $encoder = $app['security.encoder_factory']->getEncoder($user);

    // fooというパスワードに対してエンコードを行なう。
    $password = $encoder->encodePassword('foo', $user->getSalt());

ユーザーが認証されたとき、ユーザーは `User <http://api.symfony.com/master/Symfony/Component/Security/Core/User/User.html>`_ のインスタンスとしてトークンに保存されます。

フォームのセキュリティ対策
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

認証済みユーザーへのフォームは先ほどの物と近い設定で行えます。
``http`` 設定の代わりに ``form`` を設定し、パラメータを二つ設定してください。

* **login_path**: ユーザーが認証を受けていない状態で、認証が必要な領域にアクセスしてきたときにリダイレクトされる、ログイン情報を入力できるようなページへのパス

* **check_path**: Symfonyがユーザーの認証情報をバリデーションするためのチェックURL

/admin/以下の、フォームを持つ全てのURLを安全にするための例を見てみましょう。 ::

    $app['security.firewalls'] = array(
        'admin' => array(
            'pattern' => '^/admin/',
            'form' => array('login_path' => '/login', 'check_path' => '/admin/login_check'),
            'users' => array(
                'admin' => array('ROLE_ADMIN', '5FZ2Z8QIkA7UTZ4BYkoC+GsReLf569mSKDsfods6LYQ8t+a8EW9oaircfMpmaLbPBh4FOBiiFyLfuZmTSUwzZg=='),
            ),
        ),
    );

次のルールに、常に注意していてください。

* ``login_path`` にはセキュリティが設定されている領域の **外側** へのパスを設定してください。(仮にセキュリティが設定されている領域でも、 ``anonymous`` 認証メカニズムが有効になっている必要があります。 -- 詳しくは下で扱います。)

* ``check_path`` にはセキュリティが設定されている領域の **内側** へのパスを設定してください。

ログインフォームが動作するようにするためには、以下の様なコントローラーを作成してください。 ::

    use Symfony\Component\HttpFoundation\Request;

    $app->get('/login', function(Request $request) use ($app) {
        return $app['twig']->render('login.html', array(
            'error'         => $app['security.last_error']($request),
            'last_username' => $app['session']->get('_security.last_username'),
        ));
    });

認証エラーが発生した場合、
``error`` と ``last_username`` 変数には最後の認証エラーと最後にユーザーによって入力されたユーザーの名前が格納されます。

対応するテンプレートを作ります。:

.. code-block:: jinja

    <form action="{{ path('admin_login_check') }}" method="post">
        {{ error }}
        <input type="text" name="_username" value="{{ last_username }}" />
        <input type="password" name="_password" value="" />
        <input type="submit" />
    </form>

.. note::

    ``admin_login_check`` ルーティングはSilexによって自動的に定義され、 ``check_path`` の値によってルートの名前が導出されます。(全ての ``/`` は ``_`` に置換され、最後の ""/""は除去されます。)

複数のファイアーウォールの定義
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1プロジェクトに対して複数のファイアーウォールを定義することができます。

複数のファイアーウォールの設定は、ウェブサイトのパーツやユーザー(ウェブサイトのAPIではHTTPベーシック認証、管理エリアではフォームのセキュア設定を行なうなど)ごとに、
別々の認証方式を設定したい場合に便利です。

ログインフォーム以外の全てのURLに対してセキュリティ設定を行うのは以下のようにすれば簡単です。 ::

    $app['security.firewalls'] = array(
        'login' => array(
            'pattern' => '^/login$',
        ),
        'secured' => array(
            'pattern' => '^.*$',
            'form' => array('login_path' => '/login', 'check_path' => '/login_check'),
            'users' => array(
                'admin' => array('ROLE_ADMIN', '5FZ2Z8QIkA7UTZ4BYkoC+GsReLf569mSKDsfods6LYQ8t+a8EW9oaircfMpmaLbPBh4FOBiiFyLfuZmTSUwzZg=='),
            ),
        ),
    );

ファイアウォールの設定は最初にマッチしたものが優先されます。上の例では、　``/login`` というページはセキュリティ設定がなされず（認証設定が存在しない）、その他のページではセキュリティ設定が行われます。

.. tip::
    
    全ての登録された認証は ``security`` フラグを使ったON/OFFの切り替えが可能です。 ::

        $app['security.firewalls'] = array(
            'api' => array(
                'pattern' => '^/api',
                'security' => $app['debug'] ? false : true,
                'wsse' => true,

                // ...
            ),
        );

ログアウトの追加
~~~~~~~~~~~~~~~~~~~~

フォーム用の認証を使用している際には、 ``logout`` 設定を追加すれば、ユーザーをログアウトさせることができます。
このとき ``logout_path`` はファイアーウォールの ``pattern`` にマッチする必要があります。 ::

    $app['security.firewalls'] = array(
        'secured' => array(
            'pattern' => '^/admin/',
            'form' => array('login_path' => '/login', 'check_path' => '/admin/login_check'),
            'logout' => array('logout_path' => '/admin/logout'),

            // ...
        ),
    );

ルーティングは設定したパスに基づいて（全ての ``/``が ``_`` に置換され、最後の ``/`` は除去される）自動生成されます。:

.. code-block:: jinja

    <a href="{{ path('admin_logout') }}">Logout</a>

アノニマスユーザーの許可
~~~~~~~~~~~~~~~~~~~~~~~~

ウェブサイトの一部分だけにセキュリティが設定を施す場合、ユーザー情報はセキュリティ設定がなされていない領域では利用可能ではありません。
そのような領域でもユーザー情報にアクセス可能にするためには、
``anonymous`` 認証メカニズムを有効にしてください。 ::

    $app['security.firewalls'] = array(
        'unsecured' => array(
            'anonymous' => true,

            // ...
        ),
    );

アノニマス設定を行うことで、常にユーザー情報にアクセス可能になります。
もし、ユーザーが認証を受けていなかった場合、ユーザー情報として ``anon.`` という文字列が返却されます。

ユーザーのロールチェック
~~~~~~~~~~~~~~~~~~~~~~~~~

ユーザーに対してロールが与えられているかを確認するためには、 
``isGranted()`` メソッドを使ってください。 ::

    if ($app['security']->isGranted('ROLE_ADMIN')) {
        // ...
    }

Twigテンプレートでも同様の確認が行えます。

.. code-block:: jinja

    {% if is_granted('ROLE_ADMIN') %}
        <a href="/secured?_switch_user=fabien">Switch to Fabien</a>
    {% endif %}

ユーザーが認証されているかどうか（さらにアノニマスユーザーでない）は ``IS_AUTHENTICATED_FULLY`` という特別なロールを確認してください。:

.. code-block:: jinja

    {% if is_granted('IS_AUTHENTICATED_FULLY') %}
        <a href="{{ path('logout') }}">Logout</a>
    {% else %}
        <a href="{{ path('login') }}">Login</a>
    {% endif %}

もちろん、上記のコードを動かすためには  ``login`` ルートが定義されている必要があります。

.. tip::

    ``getRoles()`` メソッドをユーザーのロール確認に使用しないでください。

.. caution::

    ``isGranted()`` は(セキュリティが設定されていない領域であるなどの理由で)
    認証情報が利用可能でない場合、例外を投げます。


ユーザーの擬装
~~~~~~~~~~~~~~~~~~~~

もし、(ユーザーのクレデンシャル抜きに)別のユーザーに切り替えることを許可したい場合、
``switch_user`` 認証方式を有効にしてください。 ::

    $app['security.firewalls'] = array(
        'unsecured' => array(
            'switch_user' => array('parameter' => '_switch_user', 'role' => 'ROLE_ALLOWED_TO_SWITCH'),

            // ...
        ),
    );


この操作によって、
``ROLE_ALLOWED_TO_SWITCH`` というロールを持っているユーザーとしてログインした時に、
全てのURLに ``_switch_user`` というクエリパラメータを送ることで、
他のユーザーへ切り替えることができるようになります。

.. code-block:: jinja

    {% if is_granted('ROLE_ALLOWED_TO_SWITCH') %}
        <a href="?_switch_user=fabien">Switch to user Fabien</a>
    {% endif %}


擬装されているユーザーかどうかは ``ROLE_PREVIOUS_ADMIN`` というロールを持っているかどうか調べれば判断できます。 これは、ユーザーをメインアカウントに戻す操作を行なう場合に便利です。

.. code-block:: jinja

    {% if is_granted('ROLE_PREVIOUS_ADMIN') %}
        You are an admin but you've switched to another user,
        <a href="?_switch_user=_exit"> exit</a> the switch.
    {% endif %}

ロールの上下関係の定義
~~~~~~~~~~~~~~~~~~~~~~~~~

ロールの上下関係の定義によって、ユーザーに、複数のロールを自動的に追加することが可能になります。 ::

    $app['security.role_hierarchy'] = array(
        'ROLE_ADMIN' => array('ROLE_USER', 'ROLE_ALLOWED_TO_SWITCH'),
    );

上記の設定を行えば、 ``ROLE_ADMIN`` を持つ全てのユーザーに ``ROLE_USER`` と ``ROLE_ALLOWED_TO_SWITCH`` のロールを与えることが出来ます。

アクセスルールの設定
~~~~~~~~~~~~~~~~~~~~~

ロールはユーザーグループによってウェブサイトの振舞を変更するのにとても良い仕組みです。さらにアクセスルールの設定によって、いくつかの領域を更にセキュアにすることが出来ます。 ::

    $app['security.access_rules'] = array(
        array('^/admin', 'ROLE_ADMIN', 'https'),
        array('^.*$', 'ROLE_USER'),
    );

上記の設定を行えば、ユーザーは ``/admin`` 領域にアクセスするのに ``ROLE_ADMIN`` を持つことが必要になり、 その他の領域にアクセスするのには ``ROLE_USER`` を持っていることが必要となります。
さらに管理領域ではHTTPSでないとアクセスできないようになっています。(HTTPSでない場合、自動的にリダイレクトされます。)

.. note::
    
    最初の引数は `RequestMatcher
    <http://api.symfony.com/master/Symfony/Component/HttpFoundation/RequestMatcher.html>`_
    のインスタンスである必要があります。

カスタムユーザープロバイダーの定義
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

個人のウェブサイトのadmin領域のセキュリティ設定をする際に、
ユーザーの配列を使用するのは簡単で便利です。この場合、標準のメカニズムを上書きする必要があります。

``users`` 設定は、サービスとして定義されています。このサービスは
`UserProviderInterface
<http://api.symfony.com/master/Symfony/Component/Security/Core/User/UserProviderInterface.html>`_
のインスタンスを返却します。 ::

    'users' => $app->share(function () use ($app) {
        return new UserProvider($app['db']);
    }),

以下に、ユーザープロバイダーの簡単な例を示します。
ここでは、ユーザーを保管するのにDoctrine DBALを使用しています。 ::

    use Symfony\Component\Security\Core\User\UserProviderInterface;
    use Symfony\Component\Security\Core\User\UserInterface;
    use Symfony\Component\Security\Core\User\User;
    use Symfony\Component\Security\Core\Exception\UnsupportedUserException;
    use Symfony\Component\Security\Core\Exception\UsernameNotFoundException;
    use Doctrine\DBAL\Connection;

    class UserProvider implements UserProviderInterface
    {
        private $conn;

        public function __construct(Connection $conn)
        {
            $this->conn = $conn;
        }

        public function loadUserByUsername($username)
        {
            $stmt = $this->conn->executeQuery('SELECT * FROM users WHERE username = ?', array(strtolower($username)));

            if (!$user = $stmt->fetch()) {
                throw new UsernameNotFoundException(sprintf('Username "%s" does not exist.', $username));
            }

            return new User($user['username'], $user['password'], explode(',', $user['roles']), true, true, true, true);
        }

        public function refreshUser(UserInterface $user)
        {
            if (!$user instanceof User) {
                throw new UnsupportedUserException(sprintf('Instances of "%s" are not supported.', get_class($user)));
            }

            return $this->loadUserByUsername($user->getUsername());
        }

        public function supportsClass($class)
        {
            return $class === 'Symfony\Component\Security\Core\User\User';
        }
    }

この例では、標準の ``User`` クラスのインスタンスがユーザーののために作成されます。
しかし、独自のクラスを定義することも可能です。
唯一の制約は、クラスが `UserInterface
<http://api.symfony.com/master/Symfony/Component/Security/Core/User/UserInterface.html>`_
を実装していることです。

そして、以下が、データベーススキーマと数名のサンプルユーザーデータを生成するためのコードです。 ::

    use Doctrine\DBAL\Schema\Table;

    $schema = $app['db']->getSchemaManager();
    if (!$schema->tablesExist('users')) {
        $users = new Table('users');
        $users->addColumn('id', 'integer', array('unsigned' => true, 'autoincrement' => true));
        $users->setPrimaryKey(array('id'));
        $users->addColumn('username', 'string', array('length' => 32));
        $users->addUniqueIndex(array('username'));
        $users->addColumn('password', 'string', array('length' => 255));
        $users->addColumn('roles', 'string', array('length' => 255));

        $schema->createTable($users);

        $app['db']->insert('users', array(
          'username' => 'fabien',
          'password' => '5FZ2Z8QIkA7UTZ4BYkoC+GsReLf569mSKDsfods6LYQ8t+a8EW9oaircfMpmaLbPBh4FOBiiFyLfuZmTSUwzZg==',
          'roles' => 'ROLE_USER'
        ));

        $app['db']->insert('users', array(
          'username' => 'admin',
          'password' => '5FZ2Z8QIkA7UTZ4BYkoC+GsReLf569mSKDsfods6LYQ8t+a8EW9oaircfMpmaLbPBh4FOBiiFyLfuZmTSUwzZg==',
          'roles' => 'ROLE_ADMIN'
        ));
    }

.. tip::

    もしDoctrine ORMを使用していれば、Symfony bridge for Doctrine はエンティティからユーザーを読み込むためのユーザープロバイダークラスを提供します。

カスタムエンコーダーの定義
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

標準では、Silexは　``sha512`` アルゴリズムをパスワードのエンコーディングに用います。
さらに、パスワードは複数回エンコードされた後にbase64方式に変換されます。
これらの標準設定は、 ``security.encoder.digest`` サービスを上書きすることで、変更可能です。 ::

    use Symfony\Component\Security\Core\Encoder\MessageDigestPasswordEncoder;

    $app['security.encoder.digest'] = $app->share(function ($app) {
        // sha1アルゴリズムを使用
        // base64エンコードを行わない
        // 1回のみのエンコード
        return new MessageDigestPasswordEncoder('sha1', false, 1);
    });

カスタム認証プロバイダー
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symfony Securityコンポーネントは、
たくさんの利用可能な認証プロバイダーを提供します。(form, HTTP, X509, remember me, ...)新しいプロバイダーを容易することも簡単です。
新しい認証プロバイダーを登録するには、
``security.authentication_listener.factory.XXX`` （ ``XXX`` は設定で使用したい名前)というサービスを作ってください。 ::

    $app['security.authentication_listener.factory.wsse'] = $app->protect(function ($name, $options) use ($app) {
        // authenticationプロバイダーオブジェクトの定義
        $app['security.authentication_provider.'.$name.'.wsse'] = $app->share(function () use ($app) {
            return new WsseProvider($app['security.user_provider.default'], __DIR__.'/security_cache');
        });

        // authenticationリスナーオブジェクトの定義
        $app['security.authentication_listener.'.$name.'.wsse'] = $app->share(function () use ($app) {
            return new WsseListener($app['security'], $app['security.authentication_manager']);
        });

        return array(
            // authentication providerのid
            'security.authentication_provider.'.$name.'.wsse',
            // authentication listenerのid
            'security.authentication_listener.'.$name.'.wsse',
            // entry pointのid
            null,
            // スタック中のリスナーの位置
            'pre_auth'
        );
    });

このようにすれば、他のビルトインauthenticationプロバイダーと同じように設定可能です。 ::

    $app->register(new Silex\Provider\SecurityServiceProvider(), array(
        'security.firewalls' => array(
            'default' => array(
                'wsse' => true,

                // ...
            ),
        ),
    ));

``true`` の代わりにauthenticationファクトリーの振舞をカスタマイズするためのオプションの配列を定義することができます。これはauthenticationプロバイダークラスの第二引数として渡されます。(上の例を参照してください。)

この例では、authenticationプロバイダークラスをSymfony `cookbook`_ のように扱いました。

ステートレス認証
~~~~~~~~~~~~~~~~~~~~~~~~

標準では、セッションクッキーがユーザーのコンテキストを保持し続けます。
しかし、証明書やHTTP認証やWSSEなどを使用している場合、証明情報はリクエストの度に送信されます。そのようなケースでは ``stateless`` 認証フラグを ``true`` にすることで、このような保持を止めることができます。 ::

    $app['security.firewalls'] = array(
        'default' => array(
            'stateless' => true,
            'wsse' => true,

            // ...
        ),
    );

トレイト
----------

``Silex\Application\SecurityTrait`` は以下のショートカットを追加します。

* **user**: 現在のユーザーを返します。

* **encodePassword**: 与えられたパスワードをエンコードします。

.. code-block:: php

    $user = $app->user();

    $encoded = $app->encodePassword($user, 'foo');

``Silex\Route\SecurityTrait`` は以下のメソッドをコントローラに追加します。

* **secure**: 与えられたロールに応じて、コントローラを安全にします。

.. code-block:: php

    $app->get('/', function () {
        // do something but only for admins
    })->secure('ROLE_ADMIN');

.. _cookbook: http://symfony.com/doc/current/cookbook/security/custom_authentication_provider.html
