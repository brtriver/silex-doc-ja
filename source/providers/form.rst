FormServiceProvider
===================

*FormServiceProvider* はSymfony2 Form コンポーネントを使ったフォーム作成のためのサービスを提供します。

パラメータ
----------

* **form.secret**: この秘密の値は特定のページでのCSRFトークンとして生成され、バリデーションされます。この値を静的かつランダムに生成された値にすることはフォームのハイジャック対策として重要です。デフォルトでは ``md5(__DIR__)`` になっています。


サービス
--------

* **form.factory**: フォームを作成する際に用いる `FormFactory
  <http://api.symfony.com/master/Symfony/Component/Form/FormFactory.html>`_ のインスタンス。

* **form.csrf_provider**: `CsrfProviderInterface
  <http://api.symfony.com/master/Symfony/Component/Form/Extension/Csrf/CsrfProvider/CsrfProviderInterface.html>`_ を実装したクラスのインスタンス。
  デフォルトは `DefaultCsrfProvider
  <http://api.symfony.com/master/Symfony/Component/Form/Extension/Csrf/CsrfProvider/DefaultCsrfProvider.html>`_。

登録
-----------

.. code-block:: php

    use Silex\Provider\FormServiceProvider;

    $app->register(new FormServiceProvider());

.. note::

    もし、独自のフォームレイアウトを作成したくないのであれば、デフォルトのものを使用するとよいでしょう。しかしデフォルトレイアウトを使用するためには :doc:`translation provider
    <translation>` の登録が必要です。

    フォームのバリデーションが欲しいなら、 :doc:`Validator provider <validator>` の登録も行ってください。

.. note::

    Symfony Form Component と、それの全ての依存関係(オプションや必須を含む) はは"fat" Silexに付属し、標準サイズのSilexには付属しません。
    もしComposerを使用している場合には、 ``composer.json`` ファイルに依存関係を記述してください。

    .. code-block:: json

        "require": {
            "symfony/form": "~2.3"
        }

    バリデーションエクステンションも使用したい場合、それらの依存関係として ``symfony/config`` と ```symfony/translation`` が必要です。

    .. code-block:: json

        "require": {
            "symfony/validator": "~2.3",
            "symfony/config": "~2.3",
            "symfony/translation": "~2.3"
        }

    Symfony FormコンポーネントはPHP intl エクステンションに依存しています。
    もし持っていなかったら、Symfony Localeコンポーネントをインストールして置換してください。

    .. code-block:: json

        "require": {
            "symfony/locale": "~2.3"
        }

    Twigテンプレートでフォームを使用したい場合はSymfony Twig Bridgeをインストールしてください。

    .. code-block:: json

        "require": {
            "symfony/twig-bridge": "~2.3"
        }

使用方法
--------

FormServiceProviderは ``form.factory`` サービスを提供します。以下は使用例です。 ::

    $app->match('/form', function (Request $request) use ($app) {
        // フォームの初回表示時用のデフォルトデータ
        $data = array(
            'name' => 'Your name',
            'email' => 'Your email',
        );

        $form = $app['form.factory']->createBuilder('form', $data)
            ->add('name')
            ->add('email')
            ->add('gender', 'choice', array(
                'choices' => array(1 => 'male', 2 => 'female'),
                'expanded' => true,
            ))
            ->getForm();

        $form->handleRequest($request);

        if ($form->isValid()) {
            $data = $form->getData();

            // データを使った何らかの処理

            // どこかへのリダイレクト
            return $app->redirect('...');
        }

        // フォームの表示
        return $app['twig']->render('index.twig', array('form' => $form->createView()));
    });

以下が ``index.twig`` フォームテンプレートです。( ``symfony/twig-
bridge`` が必要です。)

.. code-block:: jinja

    <form action="#" method="post">
        {{ form_widget(form) }}

        <input type="submit" name="submit" />
    </form>

もしvalidator providerを使用している場合は、フォームの各フィールドに対して制約を与えることでバリデーションを行なうことができます。 ::

    use Symfony\Component\Validator\Constraints as Assert;

    $app->register(new Silex\Provider\ValidatorServiceProvider());
    $app->register(new Silex\Provider\TranslationServiceProvider(), array(
        'translator.messages' => array(),
    ));

    $form = $app['form.factory']->createBuilder('form')
        ->add('name', 'text', array(
            'constraints' => array(new Assert\NotBlank(), new Assert\Length(array('min' => 5)))
        ))
        ->add('email', 'text', array(
            'constraints' => new Assert\Email()
        ))
        ->add('gender', 'choice', array(
            'choices' => array(1 => 'male', 2 => 'female'),
            'expanded' => true,
            'constraints' => new Assert\Choice(array(1, 2)),
        ))
        ->getForm();

``form.extensions`` を拡張することでフォームエクステンションを登録することができます。 ::

    $app['form.extensions'] = $app->share($app->extend('form.extensions', function ($extensions) use ($app) {
        $extensions[] = new YourTopFormExtension();

        return $extensions;
    }));


``form.type.extensions`` を拡張することでフォームタイプエクステンションを登録することができます。 ::

    $app['form.type.extensions'] = $app->share($app->extend('form.type.extensions', function ($extensions) use ($app) {
        $extensions[] = new YourFormTypeExtension();

        return $extensions;
    }));

``form.type.guessers`` を拡張することでフォームタイプ推測器を登録することができます。 ::

    $app['form.type.guessers'] = $app->share($app->extend('form.type.guessers', function ($guessers) use ($app) {
        $guessers[] = new YourFormTypeGuesser();

        return $guessers;
    }));

トレイト
--------

``Silex\Application\FormTrait`` は以下のショートカットを追加します。

* **form**: フォームビルダーインスタンスを生成します。

.. code-block:: php

    $app->form($data);

より詳しい情報については、 `Symfony2 Forms ドキュメント
<http://symfony.com/doc/2.3/book/forms.html>`_ を参照してください.