イントロダクション (Introduction)
====================================

Silex は PHP 5.3 以上で動作する PHPマイクロフレームワークです。  `Symfony2`_  のコンポーネントと `Pimple`_ を利用して構築されており、 `Sinatra`_ からもインスパイアされています。

マイクロフレームワークを使うことでシンプルな1ファイル構成でアプリケーションを書くことができます。
Silex には次のような目的があります。

* *簡潔*: Silex は直感的であり、使っていて楽しくなる簡潔なAPIが用意されています。

* *高い拡張性*: Silex は Pimple というマイクロサービスコンテナーを利用した拡張機能を備えています。
  Pimple によって簡単にサードパーティーのライブラリを利用できます。

* *テスト容易性*: Silex は Symfony2 の リクエストとレスポンスを抽象化しているHttpKernelコンポーネントを利用しています。
  このおかげで、アプリケーションやフレームワーク自身をテストすることが、とても簡単になっています。
  また、HTTPの仕様書を順守し適切な利用を促進します。

一言で言えば、コントローラーを定義しそれらをルーティングにマップする作業のすべてを、たった1ステップで行うことができるのです。

利用方法
-------------

.. code-block:: php

    // web/index.php

    require_once __DIR__.'/../vendor/autoload.php';

    $app = new Silex\Application();

    $app->get('/hello/{name}', function ($name) use ($app) {
        return 'Hello '.$app->escape($name);
    });

    $app->run();

フレームワークを利用するために必要なことは ``autoload.php`` をインクルードするだけです。

次に、 ``GET`` リクエストに対し、 ``/hello/{name}`` へマッチするようなルーティングを定義します。
リクエストがルーティングにマッチした場合は、所定の関数が実行され、returnされた値がクライアントに対して送信されます。

最後に、アプリケーションを実行(run)します。　結果を見るために ``hello/world`` へアクセスしてみましょう。
本当に簡単でしょ!!

Silex のインストールは Silex をダウンロードしてくるのと同じぐらい簡単です。 Silex のアーカイブファイルをダウンロードし、展開すれば完了です!

.. _Download: http://silex.sensiolabs.org/download
.. _Symfony2: http://symfony.com/
.. _Pimple: http://pimple.sensiolabs.org/
.. _Sinatra: http://www.sinatrarb.com/

commit: c119f90e6e1a7a46ba6c15d440dd80f55d4ee4ca
original: https://github.com/silexphp/Silex/blob/master/doc/intro.rst
