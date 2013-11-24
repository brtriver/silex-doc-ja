Pharファイル
===================

.. caution::

    Silex ``phar`` ファイルを使うのは廃止されています。
    Silexや、依存関係をインストールするにはComposerを代わりに使用してください。

インストール(Installing)
-----------------------------

Silexをインストールするには `phar
<http://silex.sensiolabs.org/get/silex.phar>`_ をダウンロードして、どこかに保存してください。その後、スクリプト中でrequireしてください。 ::

    <?php

    require_once __DIR__.'/silex.phar';

    $app = new Silex\Application();

    $app->get('/hello/{name}', function ($name) use ($app) {
        return 'Hello '.$app->escape($name);
    });

    $app->run();

コンソール(Console)
---------------------

Silexは最新版にアップデートするための軽量コンソールを持っています。

あなたが使っているSilexのバージョンを知るためには、 コマンドラインで ``silex.phar`` を、 ``version`` という引数付きで実行してください。

.. code-block:: text

    $ php silex.phar version
    Silex version 0a243d3 2011-04-17 14:49:31 +0200

最新版かどうか確認するためには ``check`` コマンドを使用してください。

.. code-block:: text

    $ php silex.phar check

``silex.phar`` を最新版にするためには ``update`` コマンドを使用してください。

.. code-block:: text

    $ php silex.phar update

これは自動で新しい ``silex.phar``　を ``silex.sensiolabs.org`` からダウンロードし、既存のものと置き換えます。

落とし穴（Pitfalls）
------------------------

いくつかの落とし穴があるので、よくあるものの解決方法をお見せします。

PHPの設定
~~~~~~~~~~~~~~~~~

PHPのデフォルト設定が厳しく制限されているような場合、pharに関する設定を以下のようにしてみてください。

.. code-block:: ini

    detect_unicode = Off
    phar.readonly = Off
    phar.require_hash = Off

もしSuhosinを使っている場合、追加で以下の設定も必要です。

.. code-block:: ini

    suhosin.executor.include.whitelist = phar

.. note::

    UbuntuのPHPはSuhosinです。なので、Ubuntuを使っている場合、この変更が必要です。

Pharスタブのバグ
~~~~~~~~~~~~~~~~~~

いくつかのPHPの実装ではPharをインクルードする際に、 ``PharException`` 例外が投げられるというバグがあります。
同時に ``Silex\Application`` が見つからないということも教えてくれます。
この問題を回避するためには以下のようにインクルードを行ってください。 ::

    require_once 'phar://'.__DIR__.'/silex.phar/autoload.php';

この問題の真の原因は実際には不明です。

ioncube loaderのバグ
~~~~~~~~~~~~~~~~~~~~~~~

Ioncube loader はPHPエンコードされたファイルをデコードするためのエクステンションです。
これは不運にも、古いバージョン(4.0.9以前)はpharアーカイブと一緒には、うまく動作しません。
従って、Ioncube loader を4.0.9以降にアップデートするか、php.iniの以下の行をコメントアウトして無効にする必要があります。

.. code-block:: ini

    zend_extension = /usr/lib/php5/20090626+lfs/ioncube_loader_lin_5.3.so
