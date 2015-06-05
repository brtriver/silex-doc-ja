SerializerServiceProvider
===========================

*SerializerServiceProvider* オブジェクトをシリアライズするためのサービスを提供します。

Parameters
----------

無し

Services
--------

* **serializer**: `Symfony\\Component\\Serializer\\Serializer
  <http://api.symfony.com/master/Symfony/Component/Serializer/Serializer.html>`_ のインスタンスです。

* **serializer.encoders**: `Symfony\\Component\\Serializer\\Encoder\\JsonEncoder
  <http://api.symfony.com/master/Symfony/Component/Serializer/Encoder/JsonEncoder.html>`_
  と `Symfony\\Component\\Serializer\\Encoder\\XmlEncoder
  <http://api.symfony.com/master/Symfony/Component/Serializer/Encoder/XmlEncoder.html>`_ 。

* **serializer.normalizers**: `Symfony\\Component\\Serializer\\Normalizer\\CustomNormalizer
  <http://api.symfony.com/master/Symfony/Component/Serializer/Normalizer/CustomNormalizer.html>`_
  と `Symfony\\Component\\Serializer\\Normalizer\\GetSetMethodNormalizer
  <http://api.symfony.com/master/Symfony/Component/Serializer/Normalizer/GetSetMethodNormalizer.html>`_ 。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\SerializerServiceProvider());

.. note::

    *SerializerServiceProvider* は Symfony の `Serializer Component
    <http://symfony.com/doc/current/components/serializer.html>`_ に依存しており、 
    "全部入り" Silex のアーカイブには含まれますが、通常版には含まれません。
    そのため依存関係を追加してください:

    .. code-block:: bash

        composer require symfony/serializer

使い方
---------

``SerializerServiceProvider`` プロバイダーは ``serializer`` サービスを提供します。:

.. code-block:: php

    use Silex\Application;
    use Silex\Provider\SerializerServiceProvider;
    use Symfony\Component\HttpFoundation\Response;

    $app = new Application();

    $app->register(new SerializerServiceProvider());

    // アサートメソッド経由で、シリアライザーが扱えるコンテンツタイプのみを受け入れる
    $app->get("/pages/{id}.{_format}", function ($id) use ($app) {
        // Pageオブジェクトを返すページリポジトリサービスがあるとします。
        // また返されたオブジェクトはゲッターとセッターを持っているとします。
        $page = $app['page_repository']->find($id);
        $format = $app['request']->getRequestFormat();

        if (!$page instanceof Page) {
            $app->abort("No page found for id: $id");
        }

        return new Response($app['serializer']->serialize($page, $format), 200, array(
            "Content-Type" => $app['request']->getMimeType($format)
        ));
    })->assert("_format", "xml|json")
      ->assert("id", "\d+");
    
commit: a8ab1f8bac91246f420d9ba0b151bf1f77c38f0a
original: https://github.com/silexphp/Silex/blob/master/doc/providers/serializer.rst
