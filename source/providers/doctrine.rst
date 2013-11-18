DoctrineServiceProvider
=============================

*DoctrineServiceProvider* を使うことで簡単にデータベースへアクセスするための `Doctrine DBAL
<http://www.doctrine-project.org/projects/dbal>`_ を利用することができます。

.. note::

    Doctrine DBAL だけでは ORM サービスは提供 **されません**

パラメーター
--------------

* **db.options**: Doctrine DBAL のオプションを指定する配列

  以下のオプションが利用できます:

  * **driver**: 利用するデータベースドライバ。 標準では ``pdo_mysql`` です。
    次のどれかを指定できます: ``pdo_mysql`` 、 ``pdo_sqlite`` 、 ``pdo_pgsql`` 、
    ``pdo_oci`` 、 ``oci8`` 、 ``ibm_db2`` 、 ``pdo_ibm`` 、 ``pdo_sqlsrv`` 。

  * **dbname**: 接続先のデータベース名。

  * **host**: 接続先のホスト名。 標準は localhost。

  * **user**: 接続先のデータベースのユーザー名。　標準は root。

  * **password**: 接続先のデータベースのパスワード。

  * **charset**: ``pdo_mysql`` と ``pdo_oci`` と ``oci8`` にだけ必要な項目で、データベースに接続する際に使用する文字コードを指定。

  * **path**: ``pdo_sqlite`` だけに必要な項目で SQLite のデータベースのパスを指定。

  * **port**: ``pdo_mysql`` と ``pdo_pgsql`` と ``pdo_oci/oci8`` にだけ必要な項目で、データベースに接続する際に使用するポートを指定。

  これらのオプションの詳細については `Doctrine DBAL 設定についてのドキュメント <http://www.doctrine-project.org/docs/dbal/2.0/en/reference/configuration.html>`_ を参照してください。

サービス
--------

* **db**: データベースコネクション、　``Doctrine\DBAL\Connection`` のインスタンス。

* **db.config**: Doctrine のための設定オブジェクト。　標準は空の ``Doctrine\DBAL\Configuration``  。

* **db.event_manager**: Doctrine のためのイベントマネージャー。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\DoctrineServiceProvider(), array(
        'db.options' => array(
            'driver'   => 'pdo_sqlite',
            'path'     => __DIR__.'/app.db',
        ),
    ));

.. note::

    Doctrine DBALは "fat" Silexアーカイブに付属します。レギュラーサイズのSilexには付属しません。もしComposerを使っているのならば ``composer.json`` ファイルに依存関係を記述してください。

    .. code-block:: json

        "require": {
            "doctrine/dbal": "2.2.*",
         }

使い方
---------

Doctrine プロバイダーは ``db`` サービスを提供します。以下が使い方のサンプルです。 ::

    $app->get('/blog/{id}', function ($id) use ($app) {
        $sql = "SELECT * FROM posts WHERE id = ?";
        $post = $app['db']->fetchAssoc($sql, array((int) $id));

        return  "<h1>{$post['title']}</h1>".
                "<p>{$post['body']}</p>";
    });

複数のデータベースの利用
------------------------

Doctrineプロバイダーを使うと、複数のデータベースからアクセスすることができます。
データソースを指定するためにはプロバイダーの登録から **db.options** を、 
**dbs.options** という名前の配列で置き換える必要があります。
**dbs.options** は設定の配列であり、各キーは接続名で、値はオプションの設定を含んでいなければなりません。 ::

    $app->register(new Silex\Provider\DoctrineServiceProvider(), array(
        'dbs.options' => array (
            'mysql_read' => array(
                'driver'    => 'pdo_mysql',
                'host'      => 'mysql_read.someplace.tld',
                'dbname'    => 'my_database',
                'user'      => 'my_username',
                'password'  => 'my_password',
                'charset'   => 'utf8',
            ),
            'mysql_write' => array(
                'driver'    => 'pdo_mysql',
                'host'      => 'mysql_write.someplace.tld',
                'dbname'    => 'my_database',
                'user'      => 'my_username',
                'password'  => 'my_password',
                'charset'   => 'utf8',
            ),
        ),
    ));

標準では、最初に登録された接続がデフォルトになります。つまり1つしか接続先を登録していないときと同じようにアクセスされます。さきほど書いた設定では以下の2行は同意です。 ::

    $app['db']->fetchAssoc('SELECT * FROM table');

    $app['dbs']['mysql_read']->fetchAssoc('SELECT * FROM table');

複数接続を使った例 ::

    $app->get('/blog/{id}', function ($id) use ($app) {
        $sql = "SELECT * FROM posts WHERE id = ?";
        $post = $app['dbs']['mysql_read']->fetchAssoc($sql, array((int) $id));

        $sql = "UPDATE posts SET value = ? WHERE id = ?";
        $app['dbs']['mysql_write']->executeUpdate($sql, array('newValue', (int) $id));

        return  "<h1>{$post['title']}</h1>".
                "<p>{$post['body']}</p>";
    });
 

より詳細については、 `Doctrine DBAL documentation
<http://docs.doctrine-project.org/projects/doctrine-dbal/en/latest/>`_
を見てください。
