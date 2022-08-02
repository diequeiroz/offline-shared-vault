install: 
	brew install ssss socat
	pip install cryptography
	
setup:
	mkdir -p gen
	PASS=$$(openssl rand -hex 128) bash -c 'echo $$PASS | ssss-split -t 3 -n 5 -x -w masterkey && openssl genrsa -aes128 -out gen/masterkey.pem -passout pass:$$PASS 1024 && openssl rsa -in gen/masterkey.pem -outform PEM -passin pass:$$PASS -pubout -out gen/masterkey.pub'
	openssl genrsa -out gen/server.key 2048
	openssl req -new -key gen/server.key -x509 -days 365 -out gen/server.crt
	cat gen/server.key gen/server.crt > gen/server.pem

client:
	socat - ssl:localhost:1443,cafile=gen/server.crt

tunnel:
	ngrok tcp 1443