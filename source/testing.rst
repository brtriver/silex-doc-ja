テスト (Testing)
====================

Silex は Symfony2 のさらにその上に構築されているフレームワークです。
つまり機能テストを書き易いということです。機能テストというのはあなたの書いたコードが正しく動いているかどうかを保証するために自動的にソフトウェアのテストを行う仕組みのことです。
疑似ブラウザを使ったユーザーインターフェースを通してユーザーが行うであろう動きを擬似的に再現することができます。

なぜ
-----

ソフトウェアのテストに慣れてないのであれば、このようなテストがなぜ必要なのかと思われるかもしれません。
アプリケーションに修正を加えるた場合は必ずテストを行わなければなりません。
修正後にもすべてのページにおいて正しく動作することを確認しなければならないということです。
機能テストを行うことで時間短縮にもなります。なぜなら、たった1つのコマンドであなたの代わりに数秒でテストすることができるからです。

機能テスト、単体テストそしてテストの自動化についてもっと知りたい場合は、 `PHPUnit 
<https://github.com/sebastianbergmann/phpunit>`_
のページと `Bulat Shakirzyanov さんのクリーンなコードについてのスライド 
<http://www.slideshare.net/avalanche123/clean-code-5609451>`_
をチェックしてみてください。

PHPUnit
-------

`PHPUnit <https://github.com/sebastianbergmann/phpunit>`_
はデファクトスタンダードなPHPのためのテストフレームワークです。単体テストのために作られたものですが、単体テストだけでなく機能テストも書くことができます。
新しいクラスを用意することでテストを書くことができます。そしてこの用意するクラスは ``PHPUnit_Framework_TestCase`` を継承するようにします。
テストケースのメソッド名の先頭には ``test`` を付ける必要があります。 ::

    class ContactFormTest extends PHPUnit_Framework_TestCase
    {
        public function testInitialPage()
        {
            ...
        }
    }

テストケースでは、あなたがテスト対象に期待する状態についてのアサーションを書いておきます。
今回は問い合わせフォームをテストする場合を想定しているので、ページが正しく読み込まれ、表示されたコンテンツにフォームが含まれているかを確認しています。 ::

        public function testInitialPage()
        {
            $statusCode = ...
            $pageContent = ...

            $this->assertEquals(200, $statusCode);
            $this->assertContains('Contact us', $pageContent);
            $this->assertContains('<form', $pageContent);
        }

アサーションの一覧は PHPUnit のドキュメントにある `PHPUnit 用のテストの書き方
<https://phpunit.de/manual/current/en/writing-tests-for-phpunit.html>`_
の章で確認することができます。

Web テストケース
----------------

Symfony2 は WebTestCase クラスという機能テストを書くために利用することができるクラスを提供してくれています。
Silex のために用意したバージョンは ``Silex\WebTestCase`` であり、このクラスを継承することでテストを書くことができます。 :: 

    use Silex\WebTestCase;

    class ContactFormTest extends WebTestCase
    {
        ...
    }


.. note::

    アプリケーションのテストを行い易くするために、 次のような :doc:`usage` にある "アプリケーションの再利用性" の部分に従うようにしましょう。

.. note::

    もしSymfony2 ``WebTestCase`` クラスを使いたければ、プロジェクトにおいて明示的に依存関係をインストールしなければなりません。
    そのためには ``composer.json`` に以下のように記述する必要があります。:

    .. code-block:: json

        "require-dev": {
            "symfony/browser-kit": ">=2.3,<2.4-dev",
            "symfony/css-selector": ">=2.3,<2.4-dev"
        }

WebTestCase のために、 ``createApplication`` メソッドを実装することになるでしょう。このメソッドはアプリケーションを返却します。
次のようなコードになります。 ::

        public function createApplication()
        {
            return require __DIR__.'/path/to/app.php';
        }

ここで決して ``require_once`` を **使わない** という点に注意してください。なぜなら、このメソッドは各テストの前に実行されるからです。

.. tip::

    標準で、アプリケーションはブラウザから使っているときと同じように動作します。
    しかし、エラーが発生したとき、HTMLでレンダリングされたページではなく直接エラーメッセージを簡単に取得することができます。
    次のコードのように ``createApplication()`` をアプリケーションの設定で調整しておけばより簡単です。 ::

        public function createApplication()
        {
            $app = require __DIR__.'/path/to/app.php';
            $app['debug'] = true;
            $app['exception_handler']->disable();

            return $app;
        }

.. tip::

    あなたのアプリケーションでセッションを使用している場合、セッションのシミュレートを行なうためには、 ``session.test`` を ``true`` に設定する必要があります。 ::

        public function createApplication()
        {
            // ...

            $app['session.test'] = true;

            // ...
        }

WebTestCase は　``createClient`` メソッドを提供します。クライアントはブラウザのようなものであり、アプリケーションと対話することができるようになります。以下でどのように動作しているかみてみましょう。 ::

        public function testInitialPage()
        {
            $client = $this->createClient();
            $crawler = $client->request('GET', '/');

            $this->assertTrue($client->getResponse()->isOk());
            $this->assertCount(1, $crawler->filter('h1:contains("Contact us")'));
            $this->assertCount(1, $crawler->filter('form'));
            ...
        }

このコードに見慣れない用語がでてきます。 それは ``Client`` と ``Crawler`` です。

なお、 ``$this->app`` を通してアプリケーションにアクセスすることができます。

クライアント (Client)
---------------------

クライアントはブラウザを表現したものです。　画面遷移した履歴やクッキーなどを保持しておくことができます。
``request`` メソッドを使うことでテストするアプリケーションへアクセスするためのリクエストを作ることができます。

.. note::

    `Symfony2 のドキュメントにあるテストの章のクライアント
    <http://symfony.com/doc/current/book/testing.html#the-test-client>`_
    の部分でもう少し詳しく知ることができます。

クローラー (Crawler)
---------------------

クローラーを使うことでページのコンテンツを調査することができます。CSS エクスプレッションを使ってコンテンツのフィルタリング処理をしたりなど色々できます。

.. note::

    `Symfony2 のドキュメントにあるテストの章のクローラー
    <http://symfony.com/doc/current/book/testing.html#the-test-client>`_
    の部分でもう少し詳しく知ることができます。    

設定
-------------

PHPUnit を設定するためには ``phpunit.xml.dis`` ファイルを作成するという方法があります。
``tests`` フォルダーを作成し ``tests/YourApp/Tests/YourTest.php`` のようなファイルにテストを書きます。
``phpunit.xml.dist`` ファイルは次のような内容になります:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <phpunit backupGlobals="false"
             backupStaticAttributes="false"
             colors="true"
             convertErrorsToExceptions="true"
             convertNoticesToExceptions="true"
             convertWarningsToExceptions="true"
             processIsolation="false"
             stopOnFailure="false"
             syntaxCheck="false"
    >
        <testsuites>
            <testsuite name="YourApp Test Suite">
                <directory>./tests/</directory>
            </testsuite>
        </testsuites>
    </phpunit>


ファイルの自動読み込みのためのブートストラップや、コードカバレッジのレポートのためのホワイトリストを設定することもできます。

そして、 ``tests/YourApp/Tests/YourTest.php`` は次のようになります。 ::

    namespace YourApp\Tests;

    use Silex\WebTestCase;

    class YourTest extends WebTestCase
    {
        public function createApplication()
        {
            return require __DIR__.'/../../../app.php';
        }

        public function testFooBar()
        {
            ...
        }
    }

これで、 ``phpunit`` をコマンドラインから実行することで、あなたが書いたテストケースが処理されます。


commit: 8c8b6a67b70996dd85f20f24695504b9dd002914
original: https://github.com/silexphp/Silex/blob/master/doc/testing.rst
