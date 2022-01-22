# django_knowledge

"django knowledge" - это сервер базы знаний. Призван обеспечить:
- выгрузку данных из резервного хранилища в рабочее и наоборот;
- полнотекстовый поиск по хранилищу;
- добавления
- удобные API- и GUI-инструменты для управления выгрузкой, наполнения и поиска даных из различных внешних систем. Например, чат боты, приложения для веб и смартфонов.

# Настройка Typesense

Команды для закгрузки, установки и запуска сервера Typesense: 
```sh
wget https://dl.typesense.org/releases/0.22.1/typesense-server-0.22.1-linux-amd64.tar.gz
tar -xf typesense-server-0.22.1-linux-amd64.tar.gz
mkdir data
./typesense-server --data-dir=data --api-key=your_any_key &> /dev/null &
curl http://localhost:8108/health
```

Ключи запуска сервера:
- `--data-dir` - директория, в которой Typesense будет хранит базу данных. В примере это `data`;
- `--api-key` = ключ, по которому осуществляется досту к Typesense. В примере это `your_any_key`.

Подробное описание:
- https://typesense.org/docs/guide/install-typesense.html#%F0%9F%8E%AC-start

Пример использования:
- https://github.com/typesense/typesense-python/blob/master/examples/index_and_search.py
 