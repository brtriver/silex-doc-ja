コントローラーの組織化 (Organizing Controllers)
=================================================

コントローラーが多くなりすぎてしまった場合、コントローラーを意味的にグループ化したいことがあります。 ::

    // blog用のコントローラーを定義
    $blog = $app['controllers_factory'];
    $blog->get('/', function () {
        return 'Blog home page';
    });
    // ...

    // forum用のコントローラーを定義
    $forum = $app['controllers_factory'];
    $forum->get('/', function () {
        return 'Forum home page';
    });

    // "global" コントローラーを定義
    $app->get('/', function () {
        return 'Main home page';
    });

    $app->mount('/blog', $blog);
    $app->mount('/forum', $forum);

.. note::

    ``$app['controllers_factory']`` は使われた場合、 ``ControllerCollection`` の新しいインスタンスを返すファクトリーです。

``mount()`` は全てのルーティングに対し与えられた接頭辞を付け加え、メインアプリケーションに組み込みます。なので、 ``/`` はメインのホームページに、 ``/blog/`` はブログのホームページに、 ``/forum/`` はフォーラムのホームページにルーティングされます。

.. caution::

    ``/blog`` 以下にルーティングコレクションをマウントする場合、 ``/blog`` というURLでルーティングを定義することは不可能です。一番短い可能なURLは
    ``/blog/`` です。

.. note::

    ``get()`` や、 ``match()`` や、その他のHTTPメソッドをアプリケーションで呼ぶ際、実際には ``ControllerCollection`` のデフォルトインスタンス( ``$app['controllers']`` に保存されています。)を呼び出しています。

コントローラー分割の、他のメリットとしては、複数のコントローラーに対しての設定を、簡単に適用できるようになることが挙げられます。以下はミドルウェアの章から持ってきた、バックエンドコレクションに対して、コントローラーが扱う全ルートにセキュリティ設定を施す方法の例です。 ::

    $backend = $app['controllers_factory'];

    // ensure that all controllers require logged-in users
    $backend->before($mustBeLogged);

.. tip::

    可読性向上のため、コントローラーコレクションを複数ファイルに分割することが可能です。 ::

        // blog.php
        $blog = $app['controllers_factory'];
        $blog->get('/', function () { return 'Blog home page'; });

        return $blog;

        // app.php
        $app->mount('/blog', include 'blog.php');

    ファイルをrequireする代わりに、 :ref:`コントローラプロバイダ <controller-providers>` を作成することもできます。
