TwigExtension
=============

*TwigExtension* を利用すれば `Twig
<http://www.twig-project.org/>` テンプレートエンジンを使うことができます。

設定パラメータ
----------

* **twig.path**: twigのテンプレートファイルが入っているディレクトリへのパスです。

* **twig.templates** (オプション):このオプションを設定すると``twig.path``を設定する必要はなくなります。テンプレート名とテンプレート内容の連想配列で設定します。テンプレートをインラインで書きたい場合に使用します。

* **twig.options** (オプション): twigオプションの連想配列です。詳細な設定内容はtwigのドキュメントを参照してください。

* **twig.class_path** (オプション): twigのライブラリが入っているディレクトリへのパスです。

サービス
--------

* **twig**: ``Twig_Environment``のインスタンスです。twigと連携するのに使います。

* **twig.configure**: Twig environmentを引数に取る保護されたクロージャです。カスタムグローバル変数を追加するのに使います。

* **twig.loader**: ``twig.path``と``twig.templates``の設定を利用したTwigテンプレートのローダー(loader)です。ローダー(loader)を完全に置き換えることもできます。

登録
-----------

*Twig* のライブラリのコピーが ``vendor/twig`` にある場合の書き方です。

::

    $app->register(new Silex\Extension\TwigExtension(), array(
        'twig.path'       => __DIR__.'/views',
        'twig.class_path' => __DIR__.'/vendor/twig/lib',
    ));

.. note::

    Twigは``silex.phar``には含まれていません。開発者は自分でTwigライブラリのコピーをアプリケーションに組み込む必要があります。

使い方
-----

Twig extensionは``twig``サービスを提供します。

::

    $app->get('/hello/{name}', function ($name) use ($app) {
        return $app['twig']->render('hello.twig', array(
            'name' => $name,
        ));
    });

``views/hello.twig``を使って描画します。

$appは``app``という名前のグローバル変数として登録されるので、ビューから全てのサービスを利用することができます。 
例えば``$app['request']->getHost()``に（ビューから）アクセスするためには、テンプレートに下記のように書くだけです。

.. code-block:: jinja

    {{ app.request.host }}
