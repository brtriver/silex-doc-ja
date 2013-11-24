プロジェクトへの貢献
===========================

私たちは Silex のコードへの貢献をオープンにしています。
もしバグを見つけたり、エクステンションで貢献したいと思ったなら次の手順に従ってください。

* `Silex のリポジトリ <https://github.com/silexphp/Silex>`_ を github からフォークしてください。

* 機能を追加したり、バグフィックスを行ってください。

* 追加した作業へのテストを行ってください。これは未来のバージョンが意図せず動かなくなってしまわないようにするために重要な作業です。

* 場合によっては、ドキュメントを追加してください。

* 適切な `target branch` に、 `プルリクエスト <https://help.github.com/articles/creating-a-pull-request>`_ を送ってください。

もし大きな変更をおこなったり、何かしらの議論を必要とする場合は、
`メーリングリスト
<http://groups.google.com/group/silex-php>`_
に参加してください。

.. note::

    あなたが貢献してくれるコードはすべて MIT ライセンス になります。
    (原文)　Any code you contribute must be licensed under the MIT
    License.

ターゲットブランチ
=====================

Silexへプルリクエストを行う前に、どのブランチに投稿するかを決定する必要があります。まず、このセクションを注意深く読んでください。

Silex は二つの: `1.0` and `master` (`1.1`)という有効なブランチを持っています。

* **1.0**: バグの修正と、ドキュメントの修正は1.0 branchに行ってください。1.0 は定期的にマスターにマージされます。 1.0 branchでのSymfony2のバージョンは2.1, 2.2, 2.3です。

* **1.1**: 全ての新しい機能は1.1branchに行ってください。変更は前方互換性を破壊してはいけません。 1.1branchでのSymfony2のバージョンは2.3です。


ドキュメントの作成
=====================

ドキュメントは `reStructuredText
<http://docutils.sourceforge.net/rst.html>`_ で記述され、 `sphinx
<http://sphinx-doc.org>`_ で生成されています。

.. code-block:: bash

    $ cd doc
    $ sphinx-build -b html . build