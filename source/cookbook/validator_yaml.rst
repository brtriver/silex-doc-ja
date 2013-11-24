YAMLを使用してバリデーションを設定
==================================

シンプルであることはSilexは心臓部であるので、YAMLファイルをバリデーションに使うための独創的な方法はありません。しかし、不可能ではありませんので方法を見てみましょう。

まず、YAMLコンポーネントをインストールします。 ``composer.json`` ファイルで以下のように依存関係を宣言してください。

.. code-block:: json

    "require": {
        "symfony/yaml": "~2.3"
    }

次にバリデーションサービスに、あなたのクラスメタデータではなくYAMLファイルをロードするために ``StaticMethodLoader`` を使用しないことを伝えてください。 ::

    $app->register(new ValidatorServiceProvider());

    $app['validator.mapping.class_metadata_factory'] = new Symfony\Component\Validator\Mapping\ClassMetadataFactory(
        new Symfony\Component\Validator\Mapping\Loader\YamlFileLoader(__DIR__.'/validation.yml')
    );

これで、全てのスタティックメソッドの使い方を置き換え、バリデーションルールを ``validation.yml`` に記述することができるようになります。

.. code-block:: yaml

    # validation.yml
    Post:
      properties:
        title:
          - NotNull: ~
          - NotBlank: ~
        body:
          - Min: 100
