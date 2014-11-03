ValidatorServiceProvider
==========================

*ValidatorServiceProvider* はデータをバリデーションするためのサービスを提供します。
*FormServiceProvider* と一緒に利用するととても便利です。
しかし、このプロバイダーは単独で利用することも可能です。

パラメーター
------------

無し

サービス
--------

* **validator**: `Validator
  <http://api.symfony.com/master/Symfony/Component/Validator/Validator.html>`_ のインスタンス。

* **validator.mapping.class_metadata_factory**: メタデータ読み込みのためのファクトリー。
  バリデーション制約情報をクラスから読み込むことができます。
  標準では StaticMethodLoader--ClassMetadataFactory 。

  これを利用することでデータクラスに静的な ``loadValidatorMetadata`` を定義できるということです。
  このメソッドは ClassMetadata を引数として取ります。
  そして ClassMetadata インスタンス上に制約を設定することができるようになります。

* **validator.validator_factory**: ConstraintValidators のためのファクトリー。
  標準は ``ConstraintValidatorFactory`` 。
  ほとんどが Validator の内部で利用されます。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\ValidatorServiceProvider());

.. note::

    Symfony Validator Componentは"fat" Silexに付属し、標準サイズのSilexには付属しません。
    もしComposerを使用している場合には、 ``composer.json`` ファイルに依存関係を記述してください。

    .. code-block:: json

        "require": {
            "symfony/validator": "~2.3"
        }

使い方
-------

Validator プロバイダーは ``validator`` サービスを提供します。

値のバリデーション
~~~~~~~~~~~~~~~~~~~

直接 ``validateValue`` バリデーターメソッドを使うことで値の検証が行えます。 ::

    use Symfony\Component\Validator\Constraints as Assert;

    $app->get('/validate/{email}', function ($email) use ($app) {
        $errors = $app['validator']->validateValue($email, new Assert\Email());

        if (count($errors) > 0) {
            return (string) $errors;
        } else {
            return 'The email is valid';
        }
    });

連想配列のバリデーション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

連想配列のバリデーションは複数の制約を持つ値のバリデーションに似ています。 ::

    use Symfony\Component\Validator\Constraints as Assert;

    $book = array(
        'title' => 'My Book',
        'author' => array(
            'first_name' => 'Fabien',
            'last_name'  => 'Potencier',
        ),
    );

    $constraint = new Assert\Collection(array(
        'title' => new Assert\Length(array('min' => 10)),
        'author' => new Assert\Collection(array(
            'first_name' => array(new Assert\NotBlank(), new Assert\Length(array('min' => 10))),
            'last_name'  => new Assert\Length(array('min' => 10)),
        )),
    ));
    $errors = $app['validator']->validateValue($book, $constraint);

    if (count($errors) > 0) {
        foreach ($errors as $error) {
            echo $error->getPropertyPath().' '.$error->getMessage()."\n";
        }
    } else {
        echo 'The book is valid';
    }

オブジェクトのバリデーション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

もしクラスにバリデーションを追加したいなら、クラスのプロパティやゲッターに対する制約を定義し、 ``validate`` メソッドをコールできます。 ::

    use Symfony\Component\Validator\Constraints as Assert;

    class Book
    {
        public $title;
        public $author;
    }

    class Author
    {
        public $first_name;
        public $last_name;
    }

    $author = new Author();
    $author->first_name = 'Fabien';
    $author->last_name = 'Potencier';

    $book = new Book();
    $book->title = 'My Book';
    $book->author = $author;

    $metadata = $app['validator.mapping.class_metadata_factory']->getMetadataFor('Author');
    $metadata->addPropertyConstraint('first_name', new Assert\NotBlank());
    $metadata->addPropertyConstraint('first_name', new Assert\Length(array('min' => 10)));
    $metadata->addPropertyConstraint('last_name', new Assert\Length(array('min' => 10)));

    $metadata = $app['validator.mapping.class_metadata_factory']->getMetadataFor('Book');
    $metadata->addPropertyConstraint('title', new Assert\Length(array('min' => 10)));
    $metadata->addPropertyConstraint('author', new Assert\Valid());

    $errors = $app['validator']->validate($book);

    if (count($errors) > 0) {
        foreach ($errors as $error) {
            echo $error->getPropertyPath().' '.$error->getMessage()."\n";
        }
    } else {
        echo 'The author is valid';
    }

クラスに対する制約を静的な ``loadValidatorMetadata`` メソッドとしてあなたのクラスに追加することで宣言することも出来ます。 ::

    use Symfony\Component\Validator\Mapping\ClassMetadata;
    use Symfony\Component\Validator\Constraints as Assert;

    class Book
    {
        public $title;
        public $author;

        static public function loadValidatorMetadata(ClassMetadata $metadata)
        {
            $metadata->addPropertyConstraint('title', new Assert\Length(array('min' => 10)));
            $metadata->addPropertyConstraint('author', new Assert\Valid());
        }
    }

    class Author
    {
        public $first_name;
        public $last_name;

        static public function loadValidatorMetadata(ClassMetadata $metadata)
        {
            $metadata->addPropertyConstraint('first_name', new Assert\NotBlank());
            $metadata->addPropertyConstraint('first_name', new Assert\Length(array('min' => 10)));
            $metadata->addPropertyConstraint('last_name', new Assert\Length(array('min' => 10)));
        }
    }

    $app->get('/validate/{email}', function ($email) use ($app) {
        $author = new Author();
        $author->first_name = 'Fabien';
        $author->last_name = 'Potencier';

        $book = new Book();
        $book->title = 'My Book';
        $book->author = $author;

        $errors = $app['validator']->validate($book);

        if (count($errors) > 0) {
            foreach ($errors as $error) {
                echo $error->getPropertyPath().' '.$error->getMessage()."\n";
            }
        } else {
            echo 'The author is valid';
        }
    });

.. note::

    ゲッターへ制約を与えるには ``addGetterConstraint()`` を使ってください。クラス自身に制約を与えるには ``addConstraint()`` を使ってください。

翻訳
~~~~~~

エラーメッセージを翻訳可能にするためには、translator providerを使い、 ``validators`` にメッセージを登録してください。 ::

    $app['translator.domains'] = array(
        'validators' => array(
            'fr' => array(
                'This value should be a valid number.' => 'Cette valeur doit être un nombre.',
            ),
        ),
    );

詳細については、 `Symfony2 Validation のドキュメント
<http://symfony.com/doc/2.0/book/validation.html>`_ を参照してください。


commit: 6d03fe4107485fca92f6d6da9152f190b8a1e52a
original: https://github.com/silexphp/Silex/blob/master/doc/providers/validator.rst
