エラーを例外に変換する方法
================================

Silexはリクエスト/レスポンスサイクル中に生じた例外を捕捉します。
それはPHPのerrorやnoticeでは *ありません* .
errorやnoticeを例外に変換することで、それらを捕捉することができるようになります。このレシピでは、その方法を紹介します。


なぜSilexで、これをやらないのか
-----------------------------------

Silexも理論的には、これを自動実行することが可能です。しかし、それをしない理由があります。Silexはライブラリのように振舞舞います。つまり、Silexは、いかなるグローバルな状態も乱すことがないということです。エラーハンドラーはPHPではグローバルです。なので、これを登録するかどうかはユーザーが決定することとしています。

エラーハンドラーの登録
-------------------------------

幸運にも、 ``Symfony/Debug`` パッケージが ``ErrorHandler`` クラスを持っています。
このクラスは、全てのエラーを例外に変換することで、問題を解決してくれます。例外はSilexが捕捉してくれます。

``register`` というスタティックメソッドを呼ぶことで、これを登録可能です。 ::

    use Symfony\Component\Debug\ErrorHandler;

    ErrorHandler::register();

``web/index.php`` のようなフロントコントローラで、この処理を行うことが推奨されます。

致命的なエラーのハンドリング
-------------------------------------

致命的なエラーをハンドルするために、さらにグローバルな ``ExceptionHandler`` を追加登録することができます。 ::

    use Symfony\Component\Debug\ExceptionHandler;

    ExceptionHandler::register();

プロダクション環境では、デバッグ出力をオフにしたいと思います。この設定は ``$debug`` 引数に ``false`` を渡すことで可能です。::

    use Symfony\Component\Debug\ExceptionHandler;

    ExceptionHandler::register(false);
