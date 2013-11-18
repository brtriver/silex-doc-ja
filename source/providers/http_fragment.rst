HttpFragmentServiceProvider
===========================

*HttpFragmentServiceProvider* はテンプレート中のHTMLを断片化するための
サブフレームワーク機能を提供します。

.. warning::

    このサービス・プロバイダーはSymfony 2.4以上でのみ動作します。

パラメータ
-------------

* **fragment.path**: ESIおよびHInclude URLsのために生成されたURLに使うためのパス (標準では ``/_fragment`` )。

* **uri_signer.secret**: URI  signerサービスで使うためのsecret (HInclude rendererで使用します)。

* **fragment.renderers.hinclude.global_template**: HInclude rendererを使用した際の標準のコンテンツに使用するための、コンテンツかTwigテンプレート。

サービス
----------

* **fragment.handler**: `FragmentHandler
  <http://api.symfony.com/master/Symfony/Component/HttpKernel/Fragment/FragmentHandler.html>`_ のインスタンス

* **fragment.renderers**: fragment renderersの配列 (標準では、inline と ESI と HInclude renderers が初期設定されています。)。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\HttpFragmentServiceProvider());

使用方法
------------

.. note::

  このセクションでは、テンプレートとしてTwigを使用しているものとします。

一つのリクエスト/コントローラー/テンプレートからページを構築する代わりに、
フラグメントフレームワークは **fragments** を利用して、複数のコントローラ/サブリクエスト/サブテンプレートを使ってページを構築する機能を提供してくれます。

"sub-pages" をインクルードするにはTwigの ``render()`` 関数を使いましょう。

.. code-block:: jinja

    ページのメインコンテンツ

    {{ render('/foo') }}

    メインコンテンツの残り

``render()`` は ``/foo`` URLにあるコンテンツで置き換えられます。(内部的には、サブリクエストがSilexによってハンドリングされてサブページがレンダリングされます。)

サブリクエストを内部で作成する代わりに、ESI(この場合、サブリクエストはリバースプロクシによってハンドリングされます。)や、HInclude strategies(この場合サブリクエストはウェブブラウザーによってハンドリングされます。)を使用することもできます。 

.. code-block:: jinja

    {{ render(url('route_name')) }}

    {{ render_esi(url('route_name')) }}

    {{ render_hinclude(url('route_name')) }}
