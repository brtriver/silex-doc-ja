TwigServiceProvider
=======================

*TwigServiceProvider* を利用すれば `Twig
<http://twig.sensiolabs.org/>`_ テンプレートエンジンを使うことができます。

設定パラメータ
--------------

* **twig.path** (オプション): twig のテンプレートファイルが入っているディレクトリへのパスです(パスの配列を指定することもできます)。

* **twig.templates** (オプション): テンプレートの名前とテンプレートのコンテンツの連想配列です。 テンプレートをインラインで定義したいときに利用できます。

* **twig.options** (オプション): twig オプションの連想配列です。詳細な設定内容は `twig の公式ドキュメント <http://twig.sensiolabs.org/doc/api.html#environment-options>`_ を参照してください。

* **twig.form.templates** (オプション): フォームのレンダリングに使うテンプレートの配列  ( ``FormServiceProvider`` が有効なときのみ、使用可能です)。

サービス
--------

* **twig**: ``Twig_Environment`` のインスタンスです。twigと連携するのに使います。

* **twig.loader**: ``twig.path`` と ``twig.templates`` の設定を利用したTwigテンプレートのローダー(loader)です。ローダー(loader)を完全に置き換えることもできます。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\TwigServiceProvider(), array(
        'twig.path' => __DIR__.'/views',
    ));

.. note::

    Twigは"fat" Silexに付属し、標準サイズのSilexには付属しません。
    もしComposerを使用している場合には、依存関係を追加してください。

    .. code-block:: bash

        composer require twig/twig

Symfony2コンポーネントとの連携
-------------------------------

SymfonyはTwig bridgeを提供します。これによって、いくつかのSymfony2コンポーネントとTwigの連携が可能になります。依存関係を追加してください。

.. code-block:: bash

    composer require symfony/twig-bridge

こうすることで ``TwigServiceProvider`` は追加で以下の機能を提供するようになります。

* **UrlGeneratorServiceProvider**: ``UrlGeneratorServiceProvider`` を使っているのなら、 ``path()`` や ``url()`` 関数にアクセスできるようになります。詳しくは `Symfony2 Routing ドキュメント
  <http://symfony.com/doc/current/book/routing.html#generating-urls-from-a-template>`_ を読んでください。

* **TranslationServiceProvider**: ``TranslationServiceProvider`` を使っているのなら、翻訳のために Twigテンプレートの中で ``trans()`` と
  ``transchoice()`` 関数が使えるようになります。詳しくは `Symfony2 Translation ドキュメント <http://symfony.com/doc/current/book/translation.html#twig-templates>`_ を読んでください。

* **FormServiceProvider**: ``FormServiceProvider`` を使っているのなら、テンプレート中のフォームに対するヘルパーセットが使えるようになります。詳しくは `Symfony2 Forms リファレンス <http://symfony.com/doc/current/reference/forms/twig_reference.html>`_ を読んでください。

* **SecurityServiceProvider**: ``SecurityServiceProvider`` を使っているのなら、 ``is_granted()`` 関数がテンプレート中で使えるようになります。詳しくは `Symfony2 Security ドキュメント <http://symfony.com/doc/current/book/security.html#access-control-in-templates>`_ を読んでください。

使い方
------

Twig extension は ``twig`` サービスを提供します。 ::

    $app->get('/hello/{name}', function ($name) use ($app) {
        return $app['twig']->render('hello.twig', array(
            'name' => $name,
        ));
    });

``views/hello.twig`` を使って描画します。

どのTwigテンプレートでも、 ``app`` という変数がアプリケーションオブジェクトを参照します。
そのため、 View からはどんなサービスにもアクセスすることができます。
例えば、 ``$app['request']->getHost()`` にアクセスするためには、テンプレートに次のように書くだけです。

.. code-block:: jinja

    {{ app.request.host }}

``render`` を使うことでテンプレートから異なるコントローラーの結果をレンダリングすることもできます。

.. code-block:: jinja

    {{ render(app.request.baseUrl ~ '/sidebar') }}

    {# UrlGeneratorServiceProviderとSymfonyBridgesServiceProviderを使っていれば次のようにも書けます #}
    {{ render(url('sidebar')) }}

.. note::

    ドキュメントルートのサブディレクトリにデプロイされたときでも正常に動作するように
    ``app.request.baseUrl`` をrender関数を呼ぶ際に使用すべきです。

トレイト
---------

``Silex\Application\TwigTrait`` は以下のショートカットを追加します。

* **render**: ビューを与えられたパラメータと共にレンダリングし、レスポンスオブジェクトを返します。

.. code-block:: php

    return $app->render('index.html', ['name' => 'Fabien']);

    $response = new Response();
    $response->setTtl(10);

    return $app->render('index.html', ['name' => 'Fabien'], $response);

.. code-block:: php

    // stream a view
    use Symfony\Component\HttpFoundation\StreamedResponse;

    return $app->render('index.html', ['name' => 'Fabien'], new StreamedResponse());

カスタマイズ
-------------

使用する前であれば、 ``twig`` サービスを拡張することでTwigの環境をカスタマイズできます。 ::

    $app['twig'] = $app->extend('twig', function($twig, $app) {
        $twig->addGlobal('pi', 3.14);
        $twig->addFilter('levenshtein', new \Twig_Filter_Function('levenshtein'));

        return $twig;
    });

より詳しい情報については、 `Twig ドキュメント
<http://twig.sensiolabs.org>`_ を参照してください.


commit: fc8bbb623f33ce448c8bf1d4a95aa26360032de1
original: https://github.com/silexphp/Silex/blob/master/doc/providers/twig.rst
