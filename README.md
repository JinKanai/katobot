# カトボット
- 加藤さんの珠玉の名言をtocaroに自動投稿するボット

## ディレクトリ構成
```$xslt
├── KatoQuotes.txt
├── README.md
├── functions
│   ├── functions.iml
│   ├── http_client.py
│   ├── main.py
│   ├── quotes_provider_by_dynamodb.py
│   ├── quotes_provider_by_dynamodb.pyc
│   ├── quotes_provider_by_file.py
│   ├── requirements.txt
│   └── tocaro_handler.py
├── requirements.txt
├── template.yml
├── throw2dynamodb.py
└── venv
```

## 事前準備
TBW

## 動作確認
TBW

## デプロイ
```$xslt
$ sam build
```
```$xslt
sam package --s3-bucket sam-cli-test.tdaws.ctcs --output-template-file packaged.yml
```
```$xslt
sam deploy --template-file ./packaged.yml --stack-name katobot --region ap-northeast-1 --capabilities CAPABILITY_IAM
```
