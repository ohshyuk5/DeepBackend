server {
	        listen 80;
		        server_name 192.249.19.248;

			        location {
					                proxy_pass http://0:8080/;
							        }
}
