ウェブサーバーの設定
=======================

Apache
------

もしApacheを使うなら、 ``mod_rewrite`` を有効にして、以下の ``.htaccess`` ファイルを使ってください。

.. code-block:: apache

    <IfModule mod_rewrite.c>
        Options -MultiViews

        RewriteEngine On
        #RewriteBase /path/to/app
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteRule ^ index.php [QSA,L]
    </IfModule>

.. note::

    もし、あなたのサイトがウェブルートレベルでない場合は、 ``RewriteBase`` 文のコメントを外し、あなたのディレクトリへのパスをウェブルートからの相対パスで記述してください。

Apache 2.2.16以降を使っているなら `FallbackResource directive`_ が使えるので、.htaccessが以下のように簡単にできます。

.. code-block:: apache

    FallbackResource /index.php

.. note::

    もしあなたのサイトがウェブルートレベルでない場合、、あなたのディレクトリへのパスをウェブルートからの相対パスで記述してください。

nginx
-----

もしnginxを使っているなら、存在しないリソースを ``index.php`` へフォワードするためにvhostを設定してください。

.. code-block:: nginx

    server {
        #サイトルートはアプリのブートスクリプトへリダイレクトされます
        location = / {
            try_files @site @site;
        }

        #他の全てのロケーションは、まずファイルを試し、存在しなければフロントコントローラをあたります
        location / {
            try_files $uri $uri/ @site;
        }

        #もし、フロントコントローラを持つphpファイルが存在しなければ404を返します。
        location ~ \.php$ {
            return 404;
        }

        location @site {
            fastcgi_pass   unix:/var/run/php-fpm/www.sock;
            include fastcgi_params;
            fastcgi_param  SCRIPT_FILENAME $document_root/index.php;
            #https経由の際にはコメントを解除してください。
            #fastcgi_param HTTPS on;
        }
    }

IIS
---

もしWindowsからInternet Information Servicesを使っているなら、次のサンプルの ``web.config`` ファイルを使ってください。

.. code-block:: xml

    <?xml version="1.0"?>
    <configuration>
        <system.webServer>
            <defaultDocument>
                <files>
                    <clear />
                    <add value="index.php" />
                </files>
            </defaultDocument>
            <rewrite>
                <rules>
                    <rule name="Silex Front Controller" stopProcessing="true">
                        <match url="^(.*)$" ignoreCase="false" />
                        <conditions logicalGrouping="MatchAll">
                            <add input="{REQUEST_FILENAME}" matchType="IsFile" ignoreCase="false" negate="true" />
                        </conditions>
                        <action type="Rewrite" url="index.php" appendQueryString="true" />
                    </rule>
                </rules>
            </rewrite>
        </system.webServer>
    </configuration>

Lighttpd
--------

もしlighttpdを使っているなら、以下のサンプルの ``simple-vhost`` をスターティングポイントに使ってください。

.. code-block:: lighttpd

    server.document-root = "/path/to/app"

    url.rewrite-once = (
        # 静的ファイルの設定
        "^/assets/.+" => "$0",
        "^/favicon\.ico$" => "$0",

        "^(/[^\?]*)(\?.*)?" => "/index.php$1$2"
    )

.. _FallbackResource directive: http://www.adayinthelifeof.nl/2012/01/21/apaches-fallbackresource-your-new-htaccess-command/

PHP 5.4
-------

PHP 5.4 のビルトインサーバーを開発用に使いたい場合は設定なしでSilexを使用することができます。しかし、静的ファイルを提供したい場合はフロントコントローラがfalseを返すようにしてください。 ::

    // web/index.php

    $filename = __DIR__.preg_replace('#(\?.*)$#', '', $_SERVER['REQUEST_URI']);
    if (php_sapi_name() === 'cli-server' && is_file($filename)) {
        return false;
    }

    $app = require __DIR__.'/../src/app.php';
    $app->run();


フロントコントローラが ``web/index.php`` にあるとすると、サーバーを以下のコマンドラインで立ち上げることができます。:

.. code-block:: text

    $ php -S localhost:8080 -t web web/index.php

アプリケーションは ``http://localhost:8080`` で起動します。

.. note::

    このサーバーは開発のみに使用してください。プロダクション環境で使用するべきは **ありません** 。
