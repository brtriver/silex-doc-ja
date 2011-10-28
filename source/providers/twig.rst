TwigServiceProvider
=============

*TwigServiceProvider* を利用すれば `Twig
<http://twig.sensiolabs.org/>`_ テンプレートエンジンを使うことができます。

設定パラメータ
--------------

* **twig.path** (オプション): twig のテンプレートファイルが入っているディレクトリへのパスです(パスの配列でなければなりません)。

* **twig.templates** (optional): テンプレートの名前とテンプレートのコンテンツの連想配列です。 テンプレートをインラインで定義したいときに利用できます。

* **twig.options** (オプション): twig オプションの連想配列です。詳細な設定内容は twig のドキュメントを参照してください。

* **twig.class_path** (オプション): twig のライブラリが入っているディレクトリへのパスです。

サービス
--------

* **twig**: ``Twig_Environment`` のインスタンスです。twigと連携するのに使います。

* **twig.configure**: Twig environment を引数に取る保護されたクロージャです。カスタムグローバル変数を追加するのに使います。

* **twig.loader**: ``twig.path`` と ``twig.templates`` の設定を利用したTwigテンプレートのローダー(loader)です。ローダー(loader)を完全に置き換えることもできます。

登録
-----------

*Twig* のライブラリのコピーが ``vendor/twig`` にある場合の書き方です::

    $app->register(new Silex\ServiceProvider\TwigServiceProvider(), array(
        'twig.path'       => __DIR__.'/views',
        'twig.class_path' => __DIR__.'/vendor/twig/lib',
    ));

.. note::

    Twig は ``silex.phar`` には含まれていません。開発者は自分で Twig ライブラリのコピーをアプリケーションに組み込む必要があります。

使い方
------

Twig extension は ``twig`` サービスを提供します::

    $app->get('/hello/{name}', function ($name) use ($app) {
        return $app['twig']->render('hello.twig', array(
            'name' => $name,
        ));
    });

``views/hello.twig`` を使って描画します。

.. tip::
 
    TwigServiceProviderは ``app`` というグローバルに登録されます。
    そのため、 View からはどこからでもサービスにアクセスすることができます。
    たとえば、 ``$app['request']->getHost()`` にアクセスするためには、テンプレートは次のように書くだけです:
 
    .. code-block:: jinja

        {{ app.request.host }}

より詳しい情報については、 `Twig ドキュメント
<http://twig.sensiolabs.org>`_ を参照してください.
