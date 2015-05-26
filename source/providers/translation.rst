TranslationServiceProvider
=============================

*TranslationServiceProvider* は複数の異なる言語にアプリケーションを翻訳するためのサービスを提供します。

パラメーター
------------

* **translator.domains** (オプション): ドメインとロケールとメッセージのマップ。このパラメータは全ての言語とドメインの翻訳データを含みます。

* **locale** (オプション): 翻訳のために使用するロケール。 リクエストパラメーターに基づいて設定するようになるでしょう。　標準は ``en`` です。

* **locale_fallbacks** (オプション): 翻訳のために使用する代替のためのロケール。　現在のロケールでメッセージが設定されていないときに利用されます。

サービス
--------

* **translator**: 翻訳のために利用される `Translator
  <http://api.symfony.com/master/Symfony/Component/Translation/Translator.html>`_
  のインスタンス。

* **translator.loader**: 翻訳の　
  `LoaderInterface 
  <http://api.symfony.com/master/Symfony/Component/Translation/Loader/LoaderInterface.html>`_
  を実装したインスタンス、 標準は  
  `ArrayLoader
  <http://api.symfony.com/master/Symfony/Component/Translation/Loader/ArrayLoader.html>`_ 。

* **translator.message_selector**: `MessageSelector
  <http://api.symfony.com/master/Symfony/Component/Translation/MessageSelector.html>`_ のインスタンス。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\LocaleServiceProvider());
    $app->register(new Silex\Provider\TranslationServiceProvider(), array(
        'locale_fallbacks' => array('en'),
    ));

.. note::

    Symfony Translation Componentは"fat" Silexに付属し、標準サイズのSilexには付属しません。
    もしComposerを使用している場合には、依存関係を追加してください。

    .. code-block:: bash

        composer require symfony/translation

使い方
----------

Translation プロバイダーは ``translator`` サービスを提供し、 ``translator.domains`` パラメーターを利用します。 ::

    $app['translator.domains'] = array(
        'messages' => array(
            'en' => array(
                'hello'     => 'Hello %name%',
                'goodbye'   => 'Goodbye %name%',
            ),
            'de' => array(
                'hello'     => 'Hallo %name%',
                'goodbye'   => 'Tschüss %name%',
            ),
            'fr' => array(
                'hello'     => 'Bonjour %name%',
                'goodbye'   => 'Au revoir %name%',
            ),
        ),
        'validators' => array(
            'fr' => array(
                'This value should be a valid number.' => 'Cette valeur doit être un nombre.',
            ),
        ),
    );

    $app->get('/{_locale}/{message}/{name}', function ($message, $name) use ($app) {
        return $app['translator']->trans($message, array('%name%' => $name));
    });

上のサンプルは次のようなルーティングにおいて示すような結果になるでしょう。

* ``/en/hello/igor`` は ``Hello igor`` を返す。
                     
* ``/de/hello/igor`` は ``Hallo igor`` を返す。
                     
* ``/fr/hello/igor`` は ``Bonjour igor`` を返す。
                     
* ``/it/hello/igor`` は ``Hello igor`` を返す。 (代替設定のため).

トレイト
--------

``Silex\Application\TranslationTrait`` は以下のショートカットを追加します。

* **trans**: 与えられたメッセージを翻訳します。

* **transChoice**:　数字によって翻訳を選ぶことにより与えられた選択メッセージを翻訳します。


.. code-block:: php

    $app->trans('Hello World');

    $app->transChoice('Hello World');

レシピ
-------

YAMLでの言語ファイル
~~~~~~~~~~~~~~~~~~~~~~~~~

PHPファイルで翻訳ファイルを用意することは不便でしょう。
このレシピで外部に用意したYAMLファイルから翻訳データを読み込む方法について説明します。

まず最初にSymfony2の ``Config`` と ``Yaml`` コンポーネントを追加します。

.. code-block:: bash

    composer require symfony/config symfony/yaml

次に、YAMLファイルで言語のマッピングを作らなければなりません。マッピングファイルは ``locals/en.yml`` のような名前を使います。
マッピングは以下のようなファイルで用意するだけです。

.. code-block:: yaml

    hello: Hello %name%
    goodbye: Goodbye %name%

そして ``translator`` に ``YamlFileLoader`` と全ての翻訳ファイルを登録します。 ::
    
    use Symfony\Component\Translation\Loader\YamlFileLoader;

    $app['translator'] = $app->extend('translator', function($translator, $app) {
        $translator->addLoader('yaml', new YamlFileLoader());

        $translator->addResource('yaml', __DIR__.'/locales/en.yml', 'en');
        $translator->addResource('yaml', __DIR__.'/locales/de.yml', 'de');
        $translator->addResource('yaml', __DIR__.'/locales/fr.yml', 'fr');

        return $translator;
    });

XLIFFに基づいた言語ファイル
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

YAMLで翻訳ファイルを作成するのと同じように、Symfony2 ``Config`` コンポーネントを追加するために、依存関係をcomposerに追加した後に、 XLIFFファイルをロケールディレクトリに配置し、トランスレーターに渡します。 ::

    $translator->addResource('xliff', __DIR__.'/locales/en.xlf', 'en');
    $translator->addResource('xliff', __DIR__.'/locales/de.xlf', 'de');
    $translator->addResource('xliff', __DIR__.'/locales/fr.xlf', 'fr');

.. note::

    XLIFFローダーはエクステンションによって既に設定されています。


Twigテンプレートでの翻訳データへのアクセス
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ロードされていれば、Twigテンプレートからtranslation service providerを利用可能です。

.. code-block:: jinja

    {{ app.translator.trans('translation_key') }}

さらに、Symfonyによって提供されているTwig bridge (詳しくはこちらを見てください。
:doc:`TwigServiceProvider </providers/twig>`), を使えば、Twig流に翻訳文字を使用することが出来ます。

.. code-block:: jinja

    {{ 'translation_key'|trans }}
    {{ 'translation_key'|transchoice }}
    {% trans %}translation_key{% endtrans %}


commit: fc8bbb623f33ce448c8bf1d4a95aa26360032de1
original: https://github.com/silexphp/Silex/blob/master/doc/providers/translation.rst
