# StarWars-Explorer
Browse the universe of Star Wars with ease

## Setup
```
git clone https://github.com/Miszo97/StarWars-Explorer.git 
cd StarWars-Explorer
cp .env.example .env
```
## Start services
```
docker-compose up
```
## Run migrations
```
docker-compose exec -it web python manage.py migrate
```

## Visit homepage


http://0.0.0.0:8000/
