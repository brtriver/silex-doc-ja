LocaleServiceProvider
=====================

*LocaleServiceProvider* はアプリケーションのロケールを管理します。

パラメータ
-------------

* **locale**: ユーザーのロケール。 リクエストをハンドリングする前にセットすることで、デフォルトのロケールを定義します(標準では ``en``)。 リクエストがハンドリングされると現在のルーティングの ``__locale`` リクエスト属性によって自動的にセットされます。

サービス
--------

* n/a

Registering
-----------

.. code-block:: php

    $app->register(new Silex\Provider\LocaleServiceProvider());


commit: d6243e37fcf78aadf679141ecb96b8eefed7a203
original: https://github.com/silexphp/Silex/blob/master/doc/providers/locale.rst
