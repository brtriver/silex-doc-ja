FormExtensionを使用したフォームのCSRF保護の無効化
==========================================================

*FormExtension* はSymfony2 Form componentの機能を使って、あなたのアプリケーションでフォームを作成するためのサービスを提供してくれます。
標準では、 *FormExtenion* はクロスサイトリクエストフォージェリを防ぐためにCSRFプロテクションを使用します。クロスサイトリクエストフォージェリは
悪意のあるユーザがあなたの正当なユーザになることを試み、送信するつもりでないデータを送信させようとする攻撃手法です。

CSRFプロテクションやCSRFトークンについての詳細は `Symfony2 Book
<http://symfony.com/doc/current/book/forms.html#csrf-protection>`_ にあります。

いくつかのケースで（htmlメールにフォームを埋め込みたい場合など）、これを無効化したい場合があります。
一番簡単な方法は ``createBuilder()`` メソッドを使ってフォームビルダーに詳細なオプションを設定する方法です。

例
-----

.. code-block:: php

    $form = $app['form.factory']->createBuilder('form', null, array('csrf_protection' => false));

これによって、全てのフォームはCSRFプロテクションが無効になった状態で送信されます。

さらに
-------

この詳細な例は、``createBuilder()`` メソッドの ``$options`` パラメータ
によって ``csrf_protection`` を変更するための方法を示唆しています。

これはSymfony2の ``getDefaultOptions()`` メソッドを、あなたのformクラスで使うのと同じくらいシンプルです。 
`詳細はこちらを参照してください
<http://symfony.com/doc/current/book/forms.html#book-form-creating-form-classes>`_ 。
