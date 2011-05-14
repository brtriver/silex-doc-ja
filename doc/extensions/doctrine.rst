DoctrineExtension
=================

*DoctrineExtension* を使うことでデータベースへアクセスするための `Doctrine DBAL
<http://www.doctrine-project.org/projects/dbal>`_ を利用することができます。

.. note::

    Doctrine DBAL だけで ORM サービスは提供 **されません**

パラメーター
---------------

* **db.options**: Doctrine DBAL のオプションを指定する配列

  以下のオプションが利用できます:

  * **driver**: 利用するデータベースドライバ。 標準では ``pdo_mysql`` です。
    次のどれかを指定できます: ``pdo_mysql``、 ``pdo_sqlite``、 ``pdo_pgsql``、
    ``pdo_oci``、 ``oci8``、 ``ibm_db2``、 ``pdo_ibm``、 ``pdo_sqlsrv``.

  * **dbname**: 接続先のデータベース名。

  * **host**: 接続先のホスト名。 標準は localhost。

  * **user**: 接続先のデータベースのユーザー名。　標準は root。

  * **password**: 接続先のデータベースのパスワード。

  * **path**: ``pdo_sqlite`` だけに必要な項目で SQLite のデータベースのパスを指定。

  これらのオプションの詳細については `Doctrine DBAL 設定についてのドキュメント <http://www.doctrine-project.org/docs/dbal/2.0/en/reference/configuration.html>`_ を参照してください。

* **db.dbal.class_path** (オプション): Doctrine DBAL を配置したパス。

* **db.common.class_path** (オプション): Doctrine Common を配置したパス。

サービス
--------

* **db**: データベースコネクション、　``Doctrine\DBAL\Connection``のインスタンス。

* **db.config**: Doctrine のための設定オブジェクト。　標準は空の ``Doctrine\DBAL\Configuration`` 。

* **db.event_manager**: Doctrine のためのイベントマネージャー。

登録
-----------

*Doctrine DBAL* が　``vendor/doctrine-dbal``　に、そして　*Doctrine Common*　が ``vendor/doctrine-common`` にコピーされているかを確認してください。

::

    $app->register(new Silex\Extension\DoctrineExtension(), array(
        'db.options'            => array(
            'driver'    => 'pdo_sqlite',
            'path'      => __DIR__.'/app.db',
        ),
        'db.dbal.class_path'    => __DIR__.'/vendor/doctrine-dbal/lib',
        'db.common.class_path'  => __DIR__.'/vendor/doctrine-common/lib',
    ));

使い方
-------

Doctrine のエクションテンションで ``db`` サービスを使うことができます。以下が使い方のサンプルです。::

    $app->get('/blog/show/{id}', function ($id) use ($app) {
        $sql = "SELECT * FROM posts WHERE id = ?";
        $post = $app['db']->fetchAssoc($sql, array((int) $id));

        return  "<h1>{$post['title']}</h1>".
                "<p>{$post['body']}</p>";
    });

より詳細については、　`Doctrine DBAL documentation
<http://www.doctrine-project.org/docs/dbal/2.0/en/>`_
を見てください。
