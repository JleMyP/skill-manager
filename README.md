# skill-manager

[![CodeFactor](https://www.codefactor.io/repository/github/jlemyp/skill-manager/badge)](https://www.codefactor.io/repository/github/jlemyp/skill-manager) 
![lint](https://github.com/JleMyP/skill-manager/workflows/lint/badge.svg?branch=master)

прообразы - nimbus note, mindly, buku  

клиенты:

- mobile: xamarin [android] / flutter / qt
- web: bootstrap + jquery / react / flutter / chrome расширение
- desktop gui: wpf / qt / juce
- cli (+ offline non-server (sqlite)): commands / gui
- боты: vk, tg, discord

сервер:

- app: django / flask / fastapi / aiohttp / go
- субд: pg, mongo, tarantool
- serverless: zappa, ...
- aws, yandex, heroku, firebase (уведомления)

проекты / project manager  
клиент-сервер  
локальная база + синхронизация  

графики:

- изучения
- выполнения задач

задачи по скилам (найти ide, купить мк, ...)

линия технологий:

- лево - транзисторы
- право - оси / хз че
- ветки софт/железо
- ответвления неизвестных/неприоритетных технологий

направления - один верхний уровень групп  
группы компетенций (языки, технологии), метки  
неограниченная глубина вложенности  
желаемый уровень владения (вычислять прогресс из весов)  
текущий //-//  
сложность  
приоритет  
прикрепляемые файлы  
ресурсы для изучения (курсы, книги):

- объем ресурса (пункты) - страниц, роликов, статей и тд
- регистрация изученных пунктов

заметки для себя

отборы, группировки и сортировки по всем параметрам  
сохранение страниц по ссылкам (html, pdf)  
предпросмотр ссылок  

импорт-экспорт:

- файл (свой + общие, типа excel)
- проекты гитхаб / гитлаб (https://developer.github.com/v3/activity/starring/, https://api.github.com/users/JleMyP/starred)
- карта ума
- вк закладки (https://vk.com/dev/fave.get)
- хром закладки (json, buku, exported html)
- ютуб каналы (хрен)
- степик (https://stepik.org/api/user-courses)
- интуит
- html с чем-нить
- буфер сырых данных для последующего разбора

визуализация:

- рисование карты ума (https://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot/, https://github.com/pydot/pydot)

интеграция проектов и гита:

- активность коммитов
- обновление прогресса
- закрытие задач

какая-нибудь геймификация:

- очки
- множители очков
- достижения
- дневные задачи

работа с файлами:

- распаковка / предпросмотр архивов
- обложка и кол-во страниц для книг

че-нить про смежность технологий, типа python - django - web - devops - linux admin  
поиск похожестей: по меткам  
к изученным ресурсам прилагать конспект

---

для иерархических поисков можно в каждом ребенке хранить всю цепочку батек (array field)  
боты - прослойка перед апи, имеет ключ, позволяющий действовать от любого юзера  
весь текст с поддержкой markdown  
доп инфа - pg hstore или json  
расширение для браузера:

- быстрое добавление ресурса
- мини gui
- импорт-экспорт

---

вероятная реструктуризация / обновление:  
- логические группы (мб выделить в приложения):
    - пользователь / профиль
    - метки, папки и все для группировки и навигации
    - заметки
    - ресурсы изучения на базе заметок
    - задачи и их отслеживание
    - проекты
    - визуализация
- версионирование с просмотром истории конкретных элементов и последних изменений в целом


## install

```bash
docker plugin install grafana/loki-docker-driver --alias loki --grant-all-permissions
```

## todo

разбить compose на инфраструктурные и только приложение  
инфрастуктура:
- sentry
- *portainer*
- postgres
- redis
- nginx \[локальное хранилище или прокся в s3\]
- logi
- grafana
- *dockprom*

приложение:
- бек
- celery
  - worker
  - scheduler
  - flower
- redis
- *rabbitmq*
