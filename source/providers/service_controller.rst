ServiceControllerServiceProvider
================================

Silexのアプリケーションが大きくると、コントローラのグループ化を行って、洗練させたくなるでしょう。Silexでは、DI(dependency injection)と遅延ロードの力をフルに発揮させることによって、少しの手間だけでコントローラークラスの枠を超えて、コントローラをサービスとして生成することができます。

.. ::todo Link above to controller classes cookbook

なんでこれが必要なのか
----------------------------

- サービスロケーションを超えたDependency Injection

  この方法を使えば、
  あなたのコントローラにとって実際に必要な依存性だけを注入しながらも、
  コントローラと依存関係の読み込みを遅延させている間、  コントロールを完全に転換させることが出来ます。
  依存関係が明確に定義できているので、コントローラーから隔離してテストしやすいように簡単に依存関係をモック化できます。

- フレームワークからの独立

  この方法を使用すれば、
  あなたのコントローラーの、使用しているフレームワークへの依存性を減らす事ができます。
  注意深く作成されたコントローラは多数のフレームワークで再利用可能になるでしょう。
  依存性を注意深く管理し続けることで、コントローラを簡 単にちょっとした手間で、Silex, Symfony, Drupalとの互換性を持たせることが出来ます。

パラメータ
------------

現在は ``ServiceControllerServiceProvider`` にパラメータはありません。

サービス
--------

特別なサービスは提供されません。
``ServiceControllerServiceProvider`` は単に、既存の **resolever** を拡張します。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\ServiceControllerServiceProvider());

使用方法
----------

ブログAPIの少しだけ不自然な例で、
``/posts.json`` ルーティングがサービスとして定義されたコントローラを使うように変更したいと思います。

.. code-block:: php

    use Silex\Application;
    use Demo\Repository\PostRepository;

    $app = new Application();

    $app['posts.repository'] = $app->share(function() {
        return new PostRepository;
    });

    $app->get('/posts.json', function() use ($app) {
        return $app->json($app['posts.repository']->findAll());
    });

コントローラをサービスに書き換える方法はとてもシンプルで、
普通のPHPオブジェクトに、　``PostRepository`` を依存性として注入するようにし、 ``indexJsonAction`` メソッドをリクエストを扱えるようにするために、実装するだけです。

下の例では示されていませんが、タイプヒンティングとパラメータの名前付けによって、
普通のSilexのルーティングと同じようにあなたの欲しいパラメータが取得できます。

もし、あなたがTDD/BDDのファンなら（そして、そうあるべきです！）、
このコントローラが責務や依存性の面から見て、well-definedであり、テストが容易であることに気づくと思います。

さらに、内部的な依存関係は、
``Symfony\Component\HttpFoundation\JsonResponse`` 、
だけだということにも気づくと思います。
これは、このコントローラは容易に、フルスタックなSymfonyや、
他のアプリケーション、
`Symfony/HttpFoundation
<http://symfony.com/doc/master/components/http_foundation/introduction.html>`_　の ``Response`` オブジェクトの扱い方を知っている他のフレームワーク
で使用可能であるということを意味します。

.. code-block:: php

    namespace Demo\Controller;

    use Demo\Repository\PostRepository;
    use Symfony\Component\HttpFoundation\JsonResponse;

    class PostController
    {
        protected $repo;

        public function __construct(PostRepository $repo)
        {
            $this->repo = $repo;
        }

        public function indexJsonAction()
        {
            return new JsonResponse($this->repo->findAll());
        }
    }

最後に、あなたのコントローラをアプリケーション中のサービスとしてルーティング付きで定義してください。ルーティング定義の際の文法は ``サービス名：メソッド名`` です。

.. code-block:: php

    $app['posts.controller'] = $app->share(function() use ($app) {
        return new PostController($app['posts.repository']);
    });

    $app->get('/posts.json', "posts.controller:indexJsonAction");
