SerializerServiceProvider
===========================

*SerializerServiceProvider* オブジェクトをシリアライズするためのサービスを提供します。

Parameters
----------

無し

Services
--------

* **serializer**: `Symfony\Component\Serializer\Serializer
  <http://api.symfony.com/master/Symfony/Component/Serializer/Serializer.html>`_ のインスタンスです。

* **serializer.encoders**: `Symfony\Component\Serializer\Encoder\JsonEncoder
  <http://api.symfony.com/master/Symfony/Component/Serializer/Encoder/JsonEncoder.html>`_
  と `Symfony\Component\Serializer\Encoder\XmlEncoder
  <http://api.symfony.com/master/Symfony/Component/Serializer/Encoder/XmlEncoder.html>`_ 。

* **serializer.normalizers**: `Symfony\Component\Serializer\Normalizer\CustomNormalizer
  <http://api.symfony.com/master/Symfony/Component/Serializer/Normalizer/CustomNormalizer.html>`_
  と `Symfony\Component\Serializer\Normalizer\GetSetMethodNormalizer
  <http://api.symfony.com/master/Symfony/Component/Serializer/Normalizer/GetSetMethodNormalizer.html>`_ 。

登録
-----------

.. code-block:: php

    $app->register(new Silex\Provider\SerializerServiceProvider());

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
    
