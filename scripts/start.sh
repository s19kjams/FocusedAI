pip install -r ./src/requirements.txt

if [ ! "$(docker ps -q -f name=focusedAiPostgres)" ]; then
    docker run -d --name focusedAiPostgres -p 5433:5432 -e POSTGRES_PASSWORD=password postgres
fi

python3 ./src/main.py
