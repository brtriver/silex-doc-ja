PdoSessionStorageでセッションをデータベースで管理する
=========================================================

デフォルトでは、 :doc:`SessionServiceProvider </providers/session>` がSymfony2 NativeFileSessionStorageを使ってセッション情報をファイルに記述します。

中・大規模ウェブサイトでは、セッション情報をファイルではなく、データベースで管理したいでしょう。なぜならデータベースは複数のウェブサーバー環境に容易にスケール可能だからです。

Symfony2の `NativeSessionStorage
<http://api.symfony.com/master/Symfony/Component/HttpFoundation/Session/Storage/NativeSessionStorage.html>`_
は複数のストレージハンドラを持っています。そのうちの一つである
`PdoSessionHandler
<http://api.symfony.com/master/Symfony/Component/HttpFoundation/Session/Storage/Handler/PdoSessionHandler.html>`_ 
は、セッションの保存にPDOを使用します。
これを使うためには、次に示す例のようにアプリケーション中の ``session.storage.handler`` サービスを置き換えます。 

専用のPDO サービスの使用
----------------------------

.. code-block:: php

    use Symfony\Component\HttpFoundation\Session\Storage\Handler\PdoSessionHandler;

    $app->register(new Silex\Provider\SessionServiceProvider());

    $app['pdo.dsn'] = 'mysql:dbname=mydatabase';
    $app['pdo.user'] = 'myuser';
    $app['pdo.password'] = 'mypassword';

    $app['session.db_options'] = array(
        'db_table'      => 'session',
        'db_id_col'     => 'session_id',
        'db_data_col'   => 'session_value',
        'db_time_col'   => 'session_time',
    );

    $app['pdo'] = function () use ($app) {
        return new PDO(
            $app['pdo.dsn'],
            $app['pdo.user'],
            $app['pdo.password']
        );
    };

    $app['session.storage.handler'] = function () use ($app) {
        return new PdoSessionHandler(
            $app['pdo'],
            $app['session.db_options'],
            $app['session.storage.options']
        );
    };

DoctrineServiceProviderの使用
---------------------------------

:doc:`DoctrineServiceProvider </providers/doctrine>` を使うなら、別のDBコネクションを生成する必要はありません。単に、 ``getWrappedConnection`` メソッドを渡すだけで大丈夫です。

.. code-block:: php

    use Symfony\Component\HttpFoundation\Session\Storage\Handler\PdoSessionHandler;

    $app->register(new Silex\Provider\SessionServiceProvider());

    $app['session.db_options'] = array(
        'db_table'      => 'session',
        'db_id_col'     => 'session_id',
        'db_data_col'   => 'session_value',
        'db_time_col'   => 'session_time',
    );

    $app['session.storage.handler'] = function () use ($app) {
        return new PdoSessionHandler(
            $app['db']->getWrappedConnection(),
            $app['session.db_options'],
            $app['session.storage.options']
        );
    };

データベースの構造
------------------

PdoSessionStorageを使用するには3カラムで構成されるデータベーステーブルが必要です。:

* ``session_id``: ID column (VARCHAR(255) or larger)
* ``session_value``: Value column (TEXT or CLOB)
* ``session_time``: Time column (INTEGER)

セッションテーブルを作成するためのSQLステートメントの例は
`Symfony2 cookbook
<http://symfony.com/doc/current/cookbook/configuration/pdo_session_storage.html#example-sql-statements>`_ にあります。


commit: fc8bbb623f33ce448c8bf1d4a95aa26360032de1
original: https://github.com/silexphp/Silex/blob/master/doc/cookbook/session_storage.rst
