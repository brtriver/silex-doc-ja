TranslationServiceProvider
=====================

*TranslationServiceProvider* は複数の異なる言語にアプリケーションを翻訳するためのサービスを提供します。

パラメーター
------------

* **translator.messages**: メッセージとロケールのマッピングした配列。　このパラメーターは全ての言語の翻訳されたデータを含む。

* **locale** (オプション): 翻訳のための使用するロケール。 リクエストパラメーターに基づいて設定するようになるでしょう。　標準は ``en`` です。

* **locale_fallback** (オプション): 翻訳のための使用する代替のためのロケール。　現在のロケールが設定されていないときに利用されます。

* **translation.class_path** (オプション): Symfony2 の Translation コンポーネントを配置したパス。

サービス
--------

* **translator**: 翻訳のために利用される `Translator
  <http://api.symfony.com/2.0/Symfony/Component/Translation/Translator.html>`_
  のインスタンス。

* **translator.loader**: 翻訳の　
  `LoaderInterface 
  <http://api.symfony.com/2.0/Symfony/Component/Translation/Loader/LoaderInterface.html>`_
  を実装したインスタンス、 標準は  
  `ArrayLoader
  <http://api.symfony.com/2.0/Symfony/Component/Translation/Loader/ArrayLoader.html>`_ 。

* **translator.message_selector**: `MessageSelector
  <http://api.symfony.com/2.0/Symfony/Component/Translation/MessageSelector.html>`_ のインスタンス。

登録
-----------

Symfony2 Translation コンポーネントのコピーがが ``vendor/symfony/src`` に配置されていることを確認してください。
一番簡単な方法は Symfony2 全体を　vendor 内に置いてしまうことです::

    $app->register(new Silex\ServiceProvider\TranslationServiceProvider(), array(
        'locale_fallback'           => 'en',
        'translation.class_path'    => __DIR__.'/vendor/symfony/src',
    ));

使い方
--------

Translation プロバイダーは ``translator`` サービスを提供し、 ``translator.messages`` パラメーターを利用します::

    $app['translator.messages'] = array(
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
    );

    $app->before(function () use ($app) {
        if ($locale = $app['request']->get('locale')) {
            $app['locale'] = $locale;
        }
    });

    $app->get('/{locale}/{message}/{name}', function ($message, $name) use ($app) {
        return $app['translator']->trans($message, array('%name%' => $name));
    });

上のサンプルは次のようなルーティングにおいて示すような結果になるでしょう:

* ``/en/hello/igor`` は ``Hello igor`` を返す。
                     
* ``/de/hello/igor`` は ``Hallo igor`` を返す。
                     
* ``/fr/hello/igor`` は ``Bonjour igor`` を返す。
                     
* ``/it/hello/igor`` は ``Hello igor`` を返す。 (代替設定のため).

レシピ
-------

YAMLで言語ファイル
~~~~~~~~~~~~~~~~~~~~~~~~~

PHPファイルで翻訳ファイルを用意することは不便でしょう。
このレシピで外部に用意したYAMLファイルから翻訳データを読み込む方法について説明します。

まず最初に Symfony2 にある ``Config`` と ``Yaml`` コンポーネントが必要です。
オートローダーでこれらのコンポーネントが登録されるようにします。
そのために Symfony2 全体のリポジトリを ``vendor/symfony`` ディレクトリにクローンしてしまいます::

    $app['autoloader']->registerNamespace('Symfony', __DIR__.'/vendor/symfony/src');


次に、YAMLファイルで言語のマッピングを作らなければなりません。マッピングファイルは ``locals/en.yml`` を使います。
マッピングは以下のようなファイルで用意するだけです:

.. code-block:: yaml

    hello: Hello %name%
    goodbye: Goodbye %name%

この作業をあなたが使いたい全ての言語ファイル分用意します。そして、　ファイルに言語をマッピングするために ``translator.messages`` を設定します::

    $app['translator.messages'] = array(
        'en' => __DIR__.'/locales/en.yml',
        'de' => __DIR__.'/locales/de.yml',
        'fr' => __DIR__.'/locales/fr.yml',
    );

最後に ``ArrayLoader`` の代わりに ``YamlFileLoader`` を使うために ``translator.loader`` を上書きします。::

    $app['translator.loader'] = new Symfony\Component\Translation\Loader\YamlFileLoader();

これで YAML ファイルから翻訳データを読み込むことができます。
