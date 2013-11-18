内部の仕組み
============

この章では Silex 内部での処理ついて説明します。

Silex
-----

アプリケーション (Application)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

アプリケーションは Silex の中心となるインターフェースです。
Symfony2 の `HttpKernelInterface
<http://api.symfony.com/master/Symfony/Component/HttpKernel/HttpKernelInterface.html>`_,
を実装しています。
そのため、 `Request
<http://api.symfony.com/master/Symfony/Component/HttpFoundation/Request.html>`_
を ``handle`` メソッドに渡すことで `Response
<http://api.symfony.com/master/Symfony/Component/HttpFoundation/Response.html>`_
が返されます.

これは ``Pimple`` サービスコンテナを拡張して実現されています。
そのため、内部から扱うのと同じぐらい外部からでも柔軟性をもって利用することができます。
つまりどのサービスも置き換えることができ、それらを読み込むことができます。

アプリケーションは Symfony2 `HttpKernel
<http://api.symfony.com/master/Symfony/Component/HttpKernel/HttpKernel.html>`_ イベントをフックするために `EventDispatcher
<http://api.symfony.com/master/Symfony/Component/EventDispatcher/EventDispatcher.html>`_
を使っています。
イベントディスパッチャーのおかげで ``Request`` を取得し文字列のレスポンスを ``Response`` オブジェクトに変換したり例外をハンドリングしたりすることができます。
この他にも before/after ミドルウェアやエラーなどの独自のイベントを通知するためにイベントディスパッチャーを使っています。

コントローラー (Controller)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symfony2 の `ルーティング (Route)
<http://api.symfony.com/master/Symfony/Component/Routing/Route.html>`_
は本当に強力な機能です。

ルーティングに名前が付けることができ、そのルーティング名でURLを生成することができます。
URL の可変部分を必須項目にすることもできます。
すばらしいインターフェースを通してこれらの設定を行えるようにするために、(``get``, ``post`` メソッドなどから呼び出される) ``match`` メソッド  は ``Controller`` のインスタンスを返してくれます。
そして、この ``Controller`` がルーティングを包み込んでいます。

コントローラーコレクション (ControllerCollection)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`ルーティングコレクション (RouteCollection)
<http://api.symfony.com/master/Symfony/Component/Routing/RouteCollection.html>`_
を見えるようにした目的の1つは変更できるようにするためでした。その結果、プロバイダーで要素をルーティングコレクションに追加できるようになりました。
この試みはルーティングが自分たちの名前を全くしらないということが本当のところです。
名前は ``RouteCollection`` の前後関係においてのみ意味を持っていて、その名前は変えることができません。

この試みを解決するために、私たちはルーティングのための中間の準備領域を用意することを思いつきました。
``ControllerCollection`` は ``flush`` が呼ばれるまでコントローラーを保持しています。
そして ``flush`` が呼ばれた時点でルーティングを ``ルーティングコレクション (RouteCollection)`` に追加します。
そしてコントローラーは凍結(freeze)されます。
これが意味することは凍結されるとルーティング名を変更することはできず、もし変更しようとすると例外を投げるということです。

あいにく flush 以外の良い方法が思いつきませんでした。なぜなら flush を呼ぶということに曖昧さがないからです。
アプリケーションは flush を自動で呼び出しますが、リクエストが処理される前に ``ControllerCollection`` を読みたいのなら、あなた自身で flush を呼ぶ必要があります。

``Application`` には ``ControllerCollection`` を flush するための ``flush`` というショートカットメソッドが用意されています。

.. tip::

    ``RouteCollection`` のインスタンスを自分で生成する代わりに、
    ``$app['controllers_factory']`` ファクトリーを使いましょう。

Symfony2
--------

以下の Symfony2 コンポーネントが Silex　で利用されています:

* **HttpFoundation**: ``Request`` と ``Response`` のため.

* **HttpKernel**: なぜなら中枢部分が必要だから

* **Routing**: 定義したルーティングと一致するかどうかを確認するため

* **EventDispatcher**: HttpKernelにフックするため

より多くの情報を知りたい場合は、 `Symfony のサイトをチェックしてみてください
<http://symfony.com/>`_.
