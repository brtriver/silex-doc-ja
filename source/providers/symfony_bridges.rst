SymfonyBridgesServiceProvider
=============================

*SymfonyBridgesServiceProvider* は、 Symfony2 コンポーネントとライブラリのさらなる統合を提供します。

パラメーター
----------

* **symfony_bridges.class_path** (optional): Symfony2 Bridges
  へのパス。

Twig
----

``SymfonyBridgesServiceProvider`` を有効にすると、 ``TwigServiceProvider`` は
次の追加の機能を提供します。:

* **UrlGeneratorServiceProvider**: ``UrlGeneratorServiceProvider`` を使用すれば、
  Twig の ``path`` や ``url`` ヘルパー使うことができます。
  詳細は、 `Symfony2 Routing documentation <http://symfony.com/doc/current/book/routing.html#generating-urls-from-a-template>`
  を参照してください。

* **TranslationServiceProvider**: ``TranslationServiceProvider`` を使用すれば、
  Twig テンプレート内で、翻訳のためのヘルパーである
  ``trans`` や ``translation`` ヘルパーを使うことができます。
  詳細は、
  `Symfony2 Translation documentation <http://symfony.com/doc/current/book/translation.html#twig-templates>`
  を参照してください。


* **FormServiceProvider**: ``FormServiceProvider`` を使用すれば、
  テンプレート内のフォーム作成のためのヘルパーの一式を使うことができます。
  詳細は、
  `Symfony2 Forms reference <http://symfony.com/doc/current/reference/forms/twig_reference.html>`
  を参照してください。

登録
-----------

Symfony2 Bridges のコピーを、次のいずれかにコピーしてください。
`Symfony2 <https://github.com/symfony/symfony>`_をクローンして ``vendor/symfony/src`` もしくは
`TwigBridge <https://github.com/symfony/TwigBridge>`_をクローンして ``vendor/symfony/src/Symfony/Bridge/Twig``
(後者の方がより小さいものとなります)

その後、次のようにプロバイダーを登録してください。::

    $app->register(new Silex\Provider\SymfonyBridgesServiceProvider(), array(
        'symfony_bridges.class_path'  => __DIR__.'/vendor/symfony/src',
    ));
