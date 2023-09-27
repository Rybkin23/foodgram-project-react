# Проект сервиса рецептов "Продуктовый помошник":
Доступен на ip: 158.160.6.227, или на [домене](http://foodgram-sam.ddns.net/signin)
login: yc-user
passphrase: 7KqoI_py

### Неавторизованные пользователи могут смотреть рецепты и зарегистрироваться
### Авторизованные пользователи могут:
- публиковать рецепты
- подписываться на других пользователей
- добавлять рецепты в избранное и список покупок
- сохранять ингредиенты в отдельный файл - список продуктов для покупок (shopping-list.txt)

### Для развертывания проекта на локальной машине:
- клонируйте проект: ```git clone https://github.com/Rybkin23/foodgram-project-react.git```                               
- создайте файл <.env> в корне проекта
- запишите в файл: 
  - SECRET_KEY=(secret key django app)
  - DEBUG, ALLOWED_HOSTS
  - POSTGRES_DB
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - DB_ENGINE
  - DB_NAME
  - DB_HOST
  - DB_PORT
- выполните команду ```$ docker-compose up``` из папки infra/ 

### Установка Docker: [docker](https://docs.docker.com/engine/install/ubuntu).

# Работа над проектом: Александр Судаков
### Стек технологий: Python3, Django4 ООП, REST_API, PostgreSQL, GIT, export txt, CI/CD, Docker