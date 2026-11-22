# Shimayu Apps

Shimayuが開発するJREアプリ・横浜地下鉄アプリの紹介・サポートサイト。GitHub Pagesで公開する、外部依存なしの静的サイトです。

本番URL: https://shimayu13.github.io/rail-apps/

## App Store Connect登録用URL

| アプリ | マーケティング | サポート | プライバシー |
| --- | --- | --- | --- |
| JRE | https://shimayu13.github.io/rail-apps/jre/ | https://shimayu13.github.io/rail-apps/jre/support/ | https://shimayu13.github.io/rail-apps/jre/privacy/ |
| 横浜地下鉄 | https://shimayu13.github.io/rail-apps/yokohama/ | https://shimayu13.github.io/rail-apps/yokohama/support/ | https://shimayu13.github.io/rail-apps/yokohama/privacy/ |

生成したサイトの `app-store-urls.json` からも確認できます。App Store Connectへの登録は自動では変更しません。横浜アプリ内に既存のポリシーへのリンクがあるため、新しいURLを使う場合は次回アプリ更新時に変更してください。

## 編集・ビルド

Python 3.9以降のみで動作します。npm install等は不要です。

```sh
python3 tools/build.py
python3 tools/check.py
```

- `content/site.json`: 開発者名、公開先、問い合わせ用メール（初期値は空）。
- `tools/build.py`: 紹介文、FAQ、プライバシーポリシー、共通HTML。
- `assets/site.css`: レイアウトとレスポンシブ表示。
- `dist/`: HTML・CSS・画像を含む公開用生成物。GitHubでも完成したファイルを確認できるようGit管理しています。ソース変更後はビルドして、生成物も一緒にコミットします。

トップ、2アプリの紹介・サポート・ポリシー、共通サポート、Webサイトのプライバシー、404の計10ページを言語ごとに生成します（日本語・英語で計20ページ）。JavaScript、外部フォント、解析・広告スクリプト、Cookie、サーバー処理は使用しません。FAQはHTML標準のdetails要素で動作します。

## プレビュー

```sh
python3 tools/build.py --base '' --output preview
python3 -m http.server 4173 --directory preview
```

ブラウザで http://localhost:4173/ を開きます。Pages公開用は、既定値の `/rail-apps` を使ってビルドしてください。

## 公開

mainにpushすると `.github/workflows/pages.yml` がビルド・リンク検証後にGitHub Pagesへデプロイします。リポジトリのSettings → Pages → Build and deploymentでGitHub Actionsを選択します。

公開リポジトリのGitHub Pagesと標準GitHub Actionsランナーを利用します。有料プランや独自ドメインの購入は必要ありません。

## 公開内容の扱い

- Apple.comの余白・タイポグラフィ・製品中心の構成を参考にした独自デザインです。Appleのロゴ、画像、ページのコードは使用していません。
- 端末内の画面は、利用者から提供された実機スクリーンショットと、ビルド済みの実アプリをiPhoneシミュレータで撮影したPNGです。端末フレーム、Dynamic Islandと配置はCSSで表現しています。画面を生成・描き直す処理は行っていません。表示内容は撮影時点のもので、開発版と公開版が異なる場合がある旨をページ上に明記しています。
- アプリのApp Store公開URLが未確認のため、ダウンロードボタンは設置していません。確定後に追加できます。
- 問い合わせ先はこのリポジトリのIssuesです。投稿にはGitHubアカウントが必要で、内容は公開されます。個人情報を投稿しないよう注意書きを付けています。
- アプリのプライバシーポリシーは2026-11-15時点の確認対象ソースをもとに作成しています。リリース対象のバージョン、SDK、通信先、ログ設定を変更した場合は、本文とApp Store Connectの申告を併せて見直してください。
- アプリ本体のソース・APIキー・認証情報はこのリポジトリに含めません。

## 製品紹介のビジュアル

- 提供された実機画面を、発車標・列車位置・列車詳細・乗車位置の共有の説明に利用。
- ホームページの機能カードはスマートフォンで横にスクロールできます。
- アプリ紹介ページでは機能ごとに大きな画像と説明を配置。画像をタップすると元のPNGを表示します。
- Dynamic Islandは画像の加工ではなく、端末フレーム上のHTML/CSSで表示します。スクリーンショットに写らないハードウェア部分を補っています。
- アプリのアイコンは実際のIcon ComposerドキュメントからAppleのictoolで書き出したものです。
- `content/screenshots.json` と `content/icons.json` に画像の由来・SHA-256を記録しています。ビルド検証で画像の一致を確認します。

サイトの配色は `prefers-color-scheme` により端末のライト／ダーク設定に追従します。スクリーンショットも `picture` 要素で端末設定に合う元画像を選びます。画像自体の配色は改変しません。拡大リンクも表示中のモードと同じ画像を開きます。

`content/appearances.json` に9種類の画面のライト／ダーク画像の対応を定義しています。追加の17枚をそのまま利用し、JRE列車位置のライト版には既存のシミュレータ撮影を利用しています。

## English website

English pages live under `/en/` (https://shimayu13.github.io/rail-apps/en/). Every page has a link to its counterpart in the other language. Japanese URLs and App Store Connect registration URLs remain unchanged. Both languages use the same original screenshots, app icons and light/dark appearance settings. Screenshots show the Japanese app interface.

`tools/english.py` contains reviewed English copy and generates the English pages from the shared layout. Builds fail on missing translations; `tools/check.py` checks all 20 pages, language metadata and language links. When Japanese copy changes, update its English translation in the same change.

## Vercelでの公開

`index.html` はビルド時に `dist/index.html` として生成します。ソースのルートに手書きのHTMLを置く必要はありません。生成済みの `dist/` もGitHubへ登録しています。`dist/index.html` が日本語トップ、`dist/en/index.html` が英語トップです。Vercelでは配信先に合わせて再生成するため、以下の設定を使用してください。

`Shimayu13/rail-apps` をインポートし、次の設定でデプロイしてください。

- Root Directory: リポジトリ直下（空欄または `.`）。`dist` やアプリ側の旧コピーを指定しないでください。
- Framework Preset: Other
- Build Command: `python3 tools/build_vercel.py`
- Output Directory: `dist`
- Install Command: 空欄（外部依存なし）

ビルドコマンドと出力先はルートの `vercel.json` でも指定しています。既存のプロジェクトは最新コミットを再デプロイしてください。Vercelのシステム環境変数を有効にしてください。独自ドメインを明示する場合は `SITE_ORIGIN=https://your-domain.example` を設定できます。

Vercelでは `/` を起点に日本語・英語の20ページを生成します。画像や言語切り替えにGitHub Pages用の `/rail-apps` は付けません。canonical・サイトマップも本番ドメインに合わせ、WebサイトのプライバシーページにはVercelの配信について記載します。ビルド後にリンクと画像を自動検証します。

ローカルでVercel用生成を確認する例:

```sh
SITE_ORIGIN=https://rail-apps.example python3 tools/build_vercel.py
```

GitHub Pagesは既存の `python3 tools/build.py` と `python3 tools/check.py` を使用します。

## 生成済みファイルの更新

ソースの編集後は `python3 tools/build.py` と `python3 tools/check.py` を実行し、変更したソースと `dist/` の両方をコミットしてください。GitHub Actionsでも再生成し、コミット済み生成物との差分を確認します。Vercel用ビルド後にコミットする場合は、先に通常の `tools/build.py` でGitHub Pages用の生成物に戻してください。
