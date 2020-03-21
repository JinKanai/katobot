# カトボット
- 加藤さんの珠玉の名言をtocaroに自動投稿するボット

## ディレクトリ構成
```$xslt
├── KatoQuotes.csv 名言のもと。発言済みか否かの0/1フラグ付き。1が発言済み
├── README.md 本ファイル
├── functions Lmabda関数の本体とそこから利用されるモジュール
│   ├── functions.iml IntelliJIdeaのモジュール定義（なくてもいいファイル）
│   ├── http_client.py HTTPアクセス用のモジュール
│   ├── main.py Lambda関数の本体
│   ├── quotes_provider_by_dynamodb.py DynamoDBを取り扱うモジュール
│   ├── requirements.txt Lamndaへのデプロイ時に必要なモジュールたち（今は空）
│   └── tocaro_handler.py tocaroのメッセージを組み立てるモジュール
├── requirements.txt 本アプリで必要になるモジュール
├── template.yml SAMの定義ファイル
├── throw2dynamodb.py KatobotQuotes.csvをDynamoDBに入れるためのツール
```

## 事前準備
1. DynamoDB/Lambda/Cloudwatch eventへのアクセス権を持ったAWSアクセスキーを用意（もしくはロールを設定したインスタンスにクローン）
1. Python仮想環境を作成のち中にはいって`pip install -r requirements.txt`を実行
1. DynamoDBに適当な名前でテーブルを作成
1. 上で作ったテーブル名を環境変数`DYNAMODB_TABLE`に記載
1. throw2dynamodb.pyを実行して、DynamoDBのテーブルに名言が入っていることを確認
1. quotes_provider_by_dynamodb.pyを実行して、名言が１つ表示されれば動作OK。DynamoDB上で、表示された名言のisSaidフラグがTrueになっていることも確認しておくとなおよし。

## 注意点
- 発言フラグ（DynamoDB上ではisSaidカラム）は、CSVでは0/1(string)で設定されてますが、DynamoDB上では以下の形をとります。ちょっとややこしいですが、治すのめんどくさかったのでこのまま放置します^^
    - 未発言・・・0(int)
    - DynamoDBに登録時点で発言済み・・・1(int)
    - quotes_provider_by_dynamodb.pyから取得されたもの・・・True(boolean)
- ややこしいことに、100個の名言が出尽くしたあと全名言のフラグを未発言状態にフラッシュするのですが、その時に入る値はFalse(boolean)です。気が向いたら直します・・・

## デプロイ
- SAM CLIを使ってデプロイする場合は以下を参考にしてください。
```$xslt
$ sam build
```
```$xslt
sam package --s3-bucket sam-cli-test.tdaws.ctcs --output-template-file packaged.yml
```
```$xslt
sam deploy --template-file ./packaged.yml --stack-name katobot --region ap-northeast-1 --capabilities CAPABILITY_IAM
```
- SAM CLIを使わない場合は、functionsディレクトリ以下のファイルをなんとかしてLambdaに配置してください。ロールもがんばって設定してください。
