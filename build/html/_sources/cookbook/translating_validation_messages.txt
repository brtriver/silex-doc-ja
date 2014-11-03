バリデーションメッセージの翻訳
===============================

Symfony2 バリデータを使っている場合、バリデーションメッセージのローカライズがしばしば必要になります。
そのためには、トランスレーターを登録し、翻訳されたリソースを指定する必要があります。 ::

    $app->register(new Silex\Provider\TranslationServiceProvider(), array(
        'locale' => 'sr_Latn',
        'translator.domains' => array(),
    ));

    $app->before(function () use ($app) {
        $app['translator']->addLoader('xlf', new Symfony\Component\Translation\Loader\XliffFileLoader());
        $app['translator']->addResource('xlf', __DIR__.'/vendor/symfony/validator/Symfony/Component/Validator/Resources/translations/validators/validators.sr_Latn.xlf', 'sr_Latn', 'validators');
    });

Symfony2 ``xlf`` ファイルから翻訳されたメッセージをロードするための処理は以上の記述で全てです。


commit: 3f981d561df312cb008375df78e38e27fcf1cadd
original: https://github.com/silexphp/Silex/blob/master/doc/cookbook/translating_validation_messages.rst
