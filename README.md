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


## Things to improve
### Optimization 

- The frontend should cache the results. We ask the server every time we reload the page or by clicking load more for 0 to N results, even if it’s already in the browser

- We could delegate API resource fetching to a task that could be done by another process so we don't have to wait for the response. Celery would be a nice choice here

### Design
- We could use DRF to write a RESTful API and create the front-end application using modern frameworks like React.js or Vue.js

- We could add a login and registration flow so many users can create their accounts and save their results

- We could add more CRUD options, for example: Deleting existing collections