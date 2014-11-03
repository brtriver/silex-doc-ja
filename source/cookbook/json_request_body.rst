JSONリクエストの受け入れ
=============================

レストフルなAPIを構築する際には、JSONエンコードされたリクエストボディを許容する必要があります。ブログ記事の生成APIでの例をご紹介します。


Example API
-----------

この例では、ブログ記事の生成APIをご紹介します。
以下は、私達の要求項目です。

リクエスト
~~~~~~~~~~~~~

リクエストでは、ブログ記事をJSONオブジェクトとして送信します。
また、 ``Content-Type`` ヘッダを使用します。

.. code-block:: text

    POST /blog/posts
    Accept: application/json
    Content-Type: application/json
    Content-Length: 57

    {"title":"Hello World!","body":"This is my first post!"}

レスポンス
~~~~~~~~~~~~~~

サーバーはステータスコードといて201を返し、記事が作成されたということを伝えてくれます。
また、 ``Content-Type`` によってレスポンスがJSONであるということも教えてくれます。

.. code-block:: text

    HTTP/1.1 201 Created
    Content-Type: application/json
    Content-Length: 65
    Connection: close

    {"id":"1","title":"Hello World!","body":"This is my first post!"}

リクエストボディのパース
--------------------------

``Content-Type`` ヘッダが ``application/json`` で始まる場合、リクエストボディはJSONとしてのみパースされるべきです。
全てのリクエストに対して、この処理を行いたい場合、一番簡単な解は前処理アプリケーションミドルウェアを使用することです。

シンプルに ``json_decode`` をリクエストの内容に対して、適用します。その後、 ``$request`` オブジェクトの内容を置換します。 ::

    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\ParameterBag;

    $app->before(function (Request $request) {
        if (0 === strpos($request->headers->get('Content-Type'), 'application/json')) {
            $data = json_decode($request->getContent(), true);
            $request->request->replace(is_array($data) ? $data : array());
        }
    });

コントローラーの実装
-------------------------

コントローラーはリクエストデータに基づきブログ記事を生成し、 ``id`` を含んだJSONで記述されている記事のオブジェクトを返却します。 ::

    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;

    $app->post('/blog/posts', function (Request $request) use ($app) {
        $post = array(
            'title' => $request->request->get('title'),
            'body'  => $request->request->get('body'),
        );

        $post['id'] = createPost($post);

        return $app->json($post, 201);
    });

手動テスト
------------

作成したAPIを手動テストするためには、HTTPリクエストを送信することができる ``curl`` コマンドラインユーティリティを使うことができます。

.. code-block:: bash

    $ curl http://blog.lo/blog/posts -d '{"title":"Hello World!","body":"This is my first post!"}' -H 'Content-Type: application/json'
    {"id":"1","title":"Hello World!","body":"This is my first post!"}


commit: 34fe312a89e1cbc1d696bba419b2466305b55316
original: https://github.com/silexphp/Silex/blob/master/doc/cookbook/json_request_body.rst
