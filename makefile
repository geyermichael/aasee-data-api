run-app:
	@echo "Starting application..." 
	@docker compose up -d 
	@echo "MySQL is starting in the background. This will take some time." && sleep 20
	@echo "If the connection failed, please try run 'make app-prod-init'.\n\n"
	
	@docker exec -it aasee-app bash -c "python app/db/create_db.py"
	
	@docker run --rm -it --name mysql-bash \
    	-v "$(PWD)"/temp:/usr/src/temp \
    	--network aasee-data-api_dse-network \
    	--platform "linux/x86_64" mysql:5.7 \
    	bash -c "mysql -h aasee-db -u root -paasee-db-password aasee_database < /usr/src/temp/dump.sql"
	
	@echo "Application running."
	@echo "See the API docs: http://0.0.0.0:8000/docs"
	
stop-app:
	@echo "Stopping application...\n"
	@docker compose down --volumes
		
app-prod-init:
	@docker exec -it aasee-app bash -c "python app/db/create_db.py"
	
	@docker run --rm -it --name mysql-bash \
    	-v "$(PWD)"/temp:/usr/src/temp \
    	--network aasee-data-api_dse-network \
    	--platform "linux/x86_64" mysql:5.7 \
    	bash -c "mysql -h aasee-db -u root -paasee-db-password aasee_database < /usr/src/temp/dump.sql"	

run-app-dev:
	@echo "Starting application for development..." 
			
	@docker run --rm -d \
    	--name aasee-db-dev \
    	-e MYSQL_ROOT_PASSWORD=aasee-db-password --network dse-network-dev \
    	--platform "linux/x86_64" mysql:5.7
			
	@docker run --rm -it \
		-e ENV=dev --name aasee-app-dev -v "$(PWD)":/usr/src \
		--network dse-network-dev \
		-p 8042:8000 \
		aasee-app-dev

stop-app-dev:	
	@docker kill aasee-app-dev
	@docker kill aasee-db-dev
	
app-dev-init:
	@docker exec -it aasee-app-dev bash -c "python app/db/create_db.py"
	
	@docker run --rm -it --name mysql-bash \
    	-v "$(PWD)"/temp:/usr/src/temp \
    	--network dse-network-dev \
    	--platform "linux/x86_64" mysql:5.7 \
    	bash -c "mysql -h aasee-db-dev -u root -paasee-db-password aasee_database < /usr/src/temp/dump.sql"
		