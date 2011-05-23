Japanese Documentation for Silex, a simple Web Framework
===========================================================

[Silex][id] is a simple Web Framework.

## Translation
we will translate documentations to Japanese.

## in Japanese
このリポジトリはSilexのドキュメントを日本語に翻訳するための作業リポジトリです。
ご協力いただけるかたは翻訳したものをプルリクエストしてください。

## 準備

Silex のリポジトリをサブモジュール化しているので初期化とupdateを行う.

    $ git submodule init
    $ git submodule update

## 差分の確認方法

submodule化したSilex.gitのdocへのコミット履歴を確認して差分を更新します。


1.Silex.gitの更新を取得

    $ git pull

2.Silex.gitに移動

    $ cd Silex.git

3.翻訳作業を最後に同期した日時以降の更新内容を確認

    $ git log -p --after=2011-05-14 doc/
    (注) ここでafterに渡す年月日は以下の最終作業更新日を指定すること。

4.差分の日本語翻訳作業を行う

5.README.md の最終行の年月日を作業を追えた年月日に書き換える

6.commit し push

    $ git add .
    $ git commit -m "updated: xxxxx"
    $ git push origin master

## 作業が完了している本家コミットの年月日
2011-05-22

[id]: http://silex-project.org/