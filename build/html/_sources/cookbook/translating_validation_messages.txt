バリデーションのメッセージの国際化
====================================

Symfony2 のフォームを使うときは、バリデーションのメッセージをローカライズすることはよくあることです。

ローカライズするためにトランスレータを登録し翻訳されたリソースを指定する必要があります:

::

    $app->register(new Silex\Provider\TranslationServiceProvider(), array(
        'locale' => 'sr_Latn',
        'translation.class_path' => __DIR__ . '/vendor/symfony/src',
        'translator.messages' => array()
    ));
    $app->before(function () use ($app) {
        $app['translator']->addLoader('xlf', new Symfony\Component\Translation\Loader\XliffFileLoader());
        $app['translator']->addResource('xlf', __DIR__ . '/vendor/symfony/src/Symfony/Bundle/FrameworkBundle/Resources/translations/validators.sr_Latn.xlf', 'sr_Latn', 'validators');
    });

そして、 Symfony2 の ``xlf`` ファイルから翻訳ファイルを持ってくるだけです。
