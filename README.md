# skill-manager

[![CodeFactor](https://www.codefactor.io/repository/github/jlemyp/skill-manager/badge)](https://www.codefactor.io/repository/github/jlemyp/skill-manager) 
![lint](https://img.shields.io/github/workflow/status/JleMyP/skill-manager/lint/master?label=lint)
![build](https://img.shields.io/github/workflow/status/JleMyP/skill-manager/release)
![code factor](https://img.shields.io/codefactor/grade/github/JleMyP/skill-manager)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/JleMyP/skill-manager)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/JleMyP/skill-manager)

прообразы - nimbus note, mindly, buku, notion, joplin, astral, hackmd  

клиенты:

- mobile: flutter
- web: bootstrap + jquery / react / **flutter** / chrome расширение
- desktop gui: wpf / qt / juce / **flutter**
- cli (+ offline non-server (sqlite)): commands / gui
- боты: vk / tg

сервер:

- app: **django** / fastapi / go
- субд: **pg** / mongo / tarantool / ydb
- iaas, heroku, firebase (уведомления)

управление проектами  
клиент-сервер  
локальная база + синхронизация:

- s3
- sftp
- http

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
- звезды гитхаб / гитлаб [тык1](https://developer.github.com/v3/activity/starring/), [тык2](https://api.github.com/user/starred)
- карта ума
- вк закладки (https://vk.com/dev/fave.get)
- хром закладки (json, buku, exported html)
- ютуб каналы (youtubedl)
- хабр закладки
- [степик](https://stepik.org/api/user-courses)
- интуит
- html с чем-нить
- буфер сырых данных для последующего разбора

визуализация:

- рисование карты ума [pydot1](https://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot/), [pydot2](https://github.com/pydot/pydot), plantuml

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
    - метки, папки и все для группировки и навигации
    - заметки
    - ресурсы изучения на базе заметок
    - задачи и их отслеживание
    - визуализация
- версионирование с просмотром истории конкретных элементов и последних изменений в целом


## todo

docker:

- non-root
- healthckecks
- multi-arch

тех часть:

- идемпотентность
- версионирование в сериализаторах (?)
- gunicorn
- celery
- сокеты
- настроить логирование

фиксы:

- сбрасывается маска типов ресурсов при открытии метки
- починить картинки

логика:

- иерархия меток
- взаимосвязь меток и навыков
  - конвертация
  - взаимозаменяемость?

deploy:

- ya containers
- ya service token
- ya functions:
  - creating function
