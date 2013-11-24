サブリクエストの作成
=======================

Silexは ``HttpKernelInterface`` に基づいて構成されています。
これによって、 アプリケーションに対するリクエストをシミュレートすることができます。

これは、ページの中に異なるページを埋め込むことができることを意味します、さらに、それは、URLを変更せずに内部的にリダイレクトを行うことによってリクエストのフォワードを行えるということも意味しています。

基礎
------

``Application`` の ``handle`` メソッドを呼ぶことでサブリクエストを作成することが出来ます。
このメソッドの引数は3つです。

* ``$request``: ``Request`` クラスのインスタンスで、HTTPリクエストを表現します。

* ``$type``: ``HttpKernelInterface::MASTER_REQUEST`` または
  ``HttpKernelInterface::SUB_REQUEST`` のどちらかである必要があります。 リスナーはマスターリクエストに対してのみ実行されるので、これを ``SUB_REQUEST`` に設定することが重要です.

* ``$catch``: 例外を補足し、ステータスコード ``500`` とともにレスポンスを返却します。この引数はデフォルトで ``true`` になっています。サブリクエストのためには、基本的には ``false`` に設定したほうが好ましい場合が多いでしょう。

``handle`` を呼ぶと、 手動でサブリクエストを生成できます。以下がその例です。 ::

    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpKernel\HttpKernelInterface;

    $subRequest = Request::create('/');
    $response = $app->handle($subRequest, HttpKernelInterface::SUB_REQUEST, false);

もう少し、注意しておくべき事があります。
だいたいのケースでは、現在のマスターリクエストのいくつかの部分(クッキー、サーバー情報、セッションなどを含む)をフォワードしたいでしょう。

詳細な例を下記に示します。(``$request``
がマスターリクエストを保持しています。) ::

    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpKernel\HttpKernelInterface;

    $subRequest = Request::create('/', 'GET', array(), $request->cookies->all(), array(), $request->server->all());
    if ($request->getSession()) {
        $subRequest->setSession($request->getSession());
    }

    $response = $app->handle($subRequest, HttpKernelInterface::SUB_REQUEST, false);

クライアントに対してレスポンスをフォワードするには、単にコントローラから返却すれば大丈夫です。 ::

    use Silex\Application;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpKernel\HttpKernelInterface;

    $app->get('/foo', function (Application $app, Request $request) {
        $subRequest = Request::create('/', ...);
        $response = $app->handle($subRequest, HttpKernelInterface::SUB_REQUEST, false);

        return $response;
    });

もし、レスポンスを大きいページの内部に入れたい場合は ``Response::getContent`` を読んでください。 ::

    $header = ...;
    $footer = ...;
    $body = $response->getContent();

    return $header.$body.$footer;

Twigテンプレートによるレンダリング
---------------------------------------------

:doc:`TwigServiceProvider </providers/twig>` はTwigテンプレートで使うことが出来る ``render`` メソッドを提供します。
これによって、ページを内包させるのが便利になります。

.. code-block:: jinja

    {{ render('/sidebar') }}

詳しくは、 :doc:`TwigServiceProvider </providers/twig>` の章を読んでください。

エッジサイドインクルード (Edge Side Includes)
---------------------------------------------------

:doc:`HttpCacheServiceProvider
</providers/http_cache>` か、Varnishのようなリバースプロキシキャッシュを通して、ESIを使用することが出来ます。
これを使うとページを内包させるだけでなく、ページの一部分をキャッシュできるというメリットも生じます。

以下がESI経由でページを内包させる例です。:

.. code-block:: jinja

    <esi:include src="/sidebar" />

詳しくは、 :doc:`HttpCacheServiceProvider
</providers/http_cache>` の章を読んでください。

ベースURLに基づいたリクエストの分配
----------------------------------------------

一つ注意すべきなのはベースURLです。
もしあなたのアプリケーションがウェブサーバーのウェブルートに配置されていない場合、
``http://example.org/foo/index.php/articles/42`` のようなURLを持つことでしょう。

この場合、 ``/foo/index.php`` が、あなたのリクエストベースパスです。
Silexはルーティングプロセスでのパスプレフィックスを、 ``$request->server`` から読み取ることで解釈します。
サブリクエストでは、この挙動は問題を生じることがあります。
ベースパスをリクエストの前に付けなかった場合、リクエストはあなたがマッチさせたいベースパスを間違えて切り落としてしまうことがあるからです。

このような問題はベースパスを常にリクエストを構築する前に付けることで回避することができます。 ::

    $url = $request->getUriForPath('/');
    $subRequest = Request::create($url, 'GET', array(), $request->cookies->all(), array(), $request->server->all());

手動でサブリクエストを作成する際には、このような注意が必要です。

コンテナースコープの欠如
--------------------------------

Silexでは、とても強力なサブリクエストが使用可能であるため、制限をかける必要があります。やってしまいがちな主な制限/危険性は、Pimpleコンテナー上のスコープの欠如です。

コンテナーはSilexアプリケーションに対してグローバルです。そのため、アプリケーションオブジェクト **は** コンテナーです。 アプリケーションに対するどんなリクエストも、同じサービスの再利用で処理されます。
そのため、これらのサービスは可変（mutable）であり、マスターリクエスト中の処理はサブリクエストなどに影響を与えます。 ``request`` に依存するどんなサービスも（マスター/サブ）リクエストを受け取った時点でそれを保存し、それを使い続けます。このときリクエストが既に終了したとしても、そのリクエストを使用し続けてしまいます。

例 ::

    use Symfony\Component\HttpFoundation\Request;

    class ContentFormatNegotiator
    {
        private $request;

        public function __construct(Request $request)
        {
            $this->request = $request;
        }

        public function negotiateFormat(array $serverTypes)
        {
            $clientAcceptType = $this->request->headers->get('Accept');

            ...

            return $format;
        }
    }

この例は一見すると無害に見えます。しかし、実はあなたが
　``$request->headers->get()`` が実際に何を返すかを知る方法はありません。　なぜなら、 ``$request`` はマスターリクエストかもしれないし、サブリクエストかもしれないからです。
この場合はリクエストを ``negotiateFormat`` の引数として与えることが正解です。そうすることで、リスナーやコントローラといった現在のリクエストへの安全なアクセスが可能な場所で、それを与えることが出来ます。

以下に、もう少し一般的な、この問題に対する対処方法を示します。:

* VarnishによるESIを使う。

* リクエストを注入(inject)しない。 リスナーで代用し、リクエストを保存しなくともにアクセス可能な状態にする。

* Silexアプリケーションを注入(inject)し、そこからリクエストをフェッチする。