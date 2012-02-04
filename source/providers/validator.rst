ValidatorServiceProvider
==========================

*ValidatorServiceProvider* はデータをバリデーションするためのサービスを提供します。
*FormServiceProvider* と一緒に利用するととても便利です。
しかし、このプロバイダーは単独で利用することも可能です。

パラメーター
------------

* **validator.class_path** (オプション): Symfony2 Validator コンポーネントへのパス

サービス
--------

* **validator**: `Validator
  <http://api.symfony.com/2.0/Symfony/Component/Validator/Validator.html>`_ のインスタンス。

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

Symfony2 Validator　バリデーターのコピーを ``vendor/symfony/src`` にあることを確認してください。
Symfony2 全体を vendor ディレクトリにコピーするだけです::

    $app->register(new Silex\Provider\ValidatorServiceProvider(), array(
        'validator.class_path'    => __DIR__.'/vendor/symfony/src',
    ));

使い方
-------

Validator プロバイダーは ``validator`` サービスを提供しまうs。

値のバリデーション
~~~~~~~~~~~~~~~~~~~

直接 ``validateValue`` バリデーターメソッドを使うことで値の検証が行えます::

    use Symfony\Component\Validator\Constraints;

    $app->get('/validate-url', function () use ($app) {
        $violations = $app['validator']->validateValue($app['request']->get('url'), new Constraints\Url());
        return $violations;
    });


この使い方は他に比べて制限的です。

オブジェクトのプロパティのバリデーション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

もしクラスにバリデーションを追加したいなら、 *Services* よりも下層に静的な ``loadValidatorMetadata`` メソッドを書くことで実装することができます。
こうすることでオブジェクトのパラメーターに制約を定義することができます。
また、 getter メソッドとしても動作します::

    use Symfony\Component\Validator\Mapping\ClassMetadata;
    use Symfony\Component\Validator\Constraints;

    class Post
    {
        public $title;
        public $body;

        static public function loadValidatorMetadata(ClassMetadata $metadata)
        {
            $metadata->addPropertyConstraint('title', new Constraints\NotNull());
            $metadata->addPropertyConstraint('title', new Constraints\NotBlank());
            $metadata->addPropertyConstraint('body', new Constraints\MinLength(array('limit' => 10)));
        }
    }

    $app->post('/posts/new', function () use ($app) {
        $post = new Post();
        $post->title = $app['request']->get('title');
        $post->body = $app['request']->get('body');

        $violations = $app['validator']->validate($post);
        return $violations;
    });

これらのバリデーションをあなた自身で表示するように操作しなければならならないでしょう。
しかし、 *ValidatorServiceProvider* を使っている *FormServiceProvider* を使うことができます。

詳細については、 `Symfony2 Validation のドキュメント
<http://symfony.com/doc/2.0/book/validation.html>`_ を参照してください。
