# 結晶の対称性と格子 — 図解教材

授業用の図解ページ集です。外部ライブラリを使わない静的な HTML なので、ブラウザで `index.html` を開けばオフラインでも見られます。

## ページ

| ファイル | 内容 |
|---|---|
| `index.html` | トップ（目次） |
| `symmetry-matrices.html` | 結晶座標での対称操作の行列（六方軸・菱面体軸の 3 回回転、det と trace） |
| `basis-change.html` | 基底変換 P（定義、正方格子の例、各ブラベー格子の P） |
| `crystal-systems.html` | 晶系と格子系（hP と hR、六角柱と単位胞、晶族・格子・晶系の表と結晶の例） |
| `cells.html` | 慣用セルと基本セルを重ねた立体図（回転可） |
| `basis-vectors.html` | 慣用セルと基本セルの基底ベクトルの立体図（回転可） |
| `style.css` | 全ページ共通のスタイル（明暗の表示に自動対応） |

## 編集のしかた

- **文章や表、平面の図を直す**：`src/build.py` の中の該当箇所を書き換え、リポジトリの最上位で `python3 src/build.py` を実行すると、各 HTML が作り直される。HTML を直接書き換えてもよいが、その場合は次に build.py を実行したときに上書きされる。
- **平面の図**：SVG としてページに直接書き込まれている。`src/figs/` には六角柱と単位胞の図の SVG がある。
- **立体図**：`src/3d/` の HTML（JavaScript で描画）が元。説明文や格子のデータはその中にある。

## 公開（GitHub Pages）

リポジトリを Public にしてから、Settings → Pages で Branch を `main`、フォルダを `/ (root)` にする。`.nojekyll` を置いてあるので、ファイルはそのまま配信される。
