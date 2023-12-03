# カトボット
- 加藤さんの珠玉の名言をチャットアプリに自動投稿するボット

## ディレクトリ構成
```$xslt
├── README.md ... 本ファイル
├── functions ... Lmabda関数の本体とそこから利用されるモジュール
│   ├── functions.iml ... IntelliJIdeaのモジュール定義（なくてもいいファイル）
│   ├── main.py ... Lambda関数の本体
│   ├── quotes_provider_by_dynamodb.py ... DynamoDBを取り扱うモジュール
│   └── requirements.txt ... Lamndaへのデプロイ時に必要なモジュールたち。今は空
├── tools ... DynamoDBにデータを入れるとか、そういうツールたち
│   ├── throw2dynamodb.py ... KatobotQuotes.csvをDynamoDBに入れるためのツール
│   └── KatoQuotes.csv ... 名言のもと。S3から持ってくる
├── tests ... Lmabda関数の本体とそこから利用されるモジュール。今は空
├── requirements.txt ... 本アプリで必要になるpipパッケージ
├── template.yml ... SAMの定義ファイル
```

## 事前準備
1. DynamoDB/Lambda/CloudWatchEventsへのアクセス権を持ったAWSアクセスキーを用意（もしくはロールを設定したEC2インスタンスを用意）
1. 上記のアクセス権のあるマシンにこのリポジトリをクローンしてディレクトリに移動
1. Python仮想環境を作成して中に入ってから`pip install -r requirements.txt`を実行
1. DynamoDBに適当な名前でテーブルを作成。プライマリパーティションキーは`id`（数値）にする。
1. 上で作ったテーブル名を環境変数`DYNAMODB_TABLE`に記載
1. toolsディレクトリに移動
1. `aws s3 cp s3://<KatoQuotes.csv> .` を実行
    > KatoQuotes.csvのバケット名はxxに確認してください。
1. `throw2dynamodb.py`を実行して、DynamoDBのテーブルに名言が入っていることを確認
1. functionsディレクトリに移動
1. `quotes_provider_by_dynamodb.py`を実行して、名言が１つ表示されれば動作OK。DynamoDB上で、表示された名言のisSaidフラグがTrueになっていることも確認しておくとなおよし。
1. クローンしたトップディレクトリに移動
1. `make postkun` を実行してチャットアプリ投稿用のパッケージをインストール

## 注意点
- 発言フラグ（DynamoDB上ではisSaidカラム）は、CSVでは0/1(string)で設定されてますが、DynamoDB上では以下の形をとります。ちょっとややこしいですが、治すのめんどくさかったのでこのまま放置します^^
    - 未発言・・・false(boolean)
    - quotes_provider_by_dynamodb.pyから取得されたもの（一度発言されたもの）・・・True(boolean)
    - 100個の名言が出尽してフラグをフラッシュしたとき・・・False(boolean)

## デプロイ
- SAM CLIを使ってデプロイする場合は以下を参考にしてください。
```$xslt
sam build
```
```$xslt
sam package --s3-bucket sam-cli-test.tdaws.ctcs --output-template-file packaged.yml
```
```$xslt
sam deploy --template-file ./packaged.yml --stack-name katobot --region ap-northeast-1 --capabilities CAPABILITY_IAM
```
- SAM CLIを使わない場合は、functionsディレクトリ以下のファイルをなんとかしてLambdaに配置してください。ロールもがんばって設定してください。
