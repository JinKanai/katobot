deploy:
	sam build
	sam package --s3-bucket $(S3_BUCKET) --output-template-file packaged.yml
	sam deploy --template-file ./packaged.yml --stack-name cfn-katobot --region ap-northeast-1 --capabilities CAPABILITY_IAM

postkun:
	pip install git+https://github.com/jinkanai/postkun.git@feature/init -t functions -U
	rm -rf functions/postkun-*

