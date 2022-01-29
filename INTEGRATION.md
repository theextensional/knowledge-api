# Интеграция с сервисами хранения и поиска информации

## Настройка Typesense

Команды для загрузки, установки и запуска сервера Typesense:

```sh
wget https://dl.typesense.org/releases/0.22.1/typesense-server-0.22.1-linux-amd64.tar.gz
tar -xf typesense-server-0.22.1-linux-amd64.tar.gz
mkdir data
./typesense-server --data-dir=data --api-key=your_any_key &> /dev/null &
curl http://localhost:8108/health
```

Ключи запуска сервера:

- `--data-dir` - директория, в которой Typesense будет хранит базу данных. В примере это `data`;
- `--api-key` - ключ, по которому осуществляется досту к Typesense. В примере это `your_any_key`.

- Подробное описание установки: <https://typesense.org/docs/guide/install-typesense.html#%F0%9F%8E%AC-start>
- Описание API для работы с документами Typesense (включая разные способы поиска): <https://typesense.org/docs/0.22.1/api/documents.html#federated-multi-search>
- Примеры использования: <https://github.com/typesense/typesense-python/blob/master/examples>

## Firebase

Данная облачная база не поддерживает полнотекстовый поиск, а только поиск по точному совпадению значения. Для интеграции с полнотекстовыми системами на странице документации [предлагаются платные плагины](https://firebase.google.com/docs/firestore/solutions/search).

## GitHub - выгрузка свежих изменений

Тестирую на: <https://github.com/TVP-Support/knowledge/commit/b5f3762c967f7e9eb77f4534e33de4fd421588b2>

Выгрузка diff через GraphQL:

- описание GraphQL: <https://docs.github.com/en/graphql/guides>
- описание GraphQL: <https://docs.github.com/en/graphql/guides/forming-calls-with-graphql#authenticating-with-graphql>
- <https://coderoad.ru/18138885/Github-API-v3-%D0%B2%D1%8B%D0%B1%D0%BE%D1%80%D0%BA%D0%B0-diff-%D0%BA%D0%BE%D0%BD%D0%BA%D1%80%D0%B5%D1%82%D0%BD%D0%BE%D0%B3%D0%BE-%D0%BA%D0%BE%D0%BC%D0%BC%D0%B8%D1%82%D0%B0>
- <https://stackoverflow.com/questions/64202547/how-to-compare-two-branches-in-github-with-graphql>
- получить коммиты: <https://stackoverflow.com/questions/48285888/github-graphql-getting-a-repositorys-list-of-commits>

Выгрузка diff через Rest:

- Описание API всех категорий: <https://docs.github.com/en/rest/reference>
- Описание API сравнения коммитов (категория "репозиторий"): <https://docs.github.com/en/rest/reference/repos#compare-two-commits>
- <https://coderoad.ru/26925312/GitHub-API-%D0%BA%D0%B0%D0%BA-%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B8%D1%82%D1%8C-2-%D0%BA%D0%BE%D0%BC%D0%BC%D0%B8%D1%82%D0%B0>

### Пример REST API

URL: GET <https://api.github.com/repos/TVP-Support/knowledge/compare/755e7a25d70b04fb3243e207a235a213ea2a8596...b5f3762c967f7e9eb77f4534e33de4fd421588b2>

Заголовки HTTP:

- Accept: application/vnd.github.v3+json

### Пример GraphQL API

URL: POST <https://api.github.com/graphql>

Заголовки HTTP:

- Content-Type: application/json
- Authorization: bearer YourToken

Body:

 ```GraphQL
query getStartAndEndPoints {
  repository(owner:"TVP-Support", name:"knowledge") {
    endPoint:  ref(qualifiedName: "b5f3762c967f7e9eb77f4534e33de4fd421588b2") {
      ...internalBranchContent
    }
    startPoint:  ref(qualifiedName: "755e7a25d70b04fb3243e207a235a213ea2a8596") {
      ...internalBranchContent
    }
  }
}
fragment internalBranchContent on Ref {
  target {
    ... on Commit {
      history(first: 10) {
        edges {
          node {
            messageBody
          }
        }
      }
    }
  }
}
```

### Забор обновлений из репозитория базы знаний

- О вебхуках:
<https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks>
- Реализации GraphQL: <https://graphql.org/code/>
- Руководство: <https://graphql.org/learn/queries/>
- установка хуков на репозиторий:
  - <https://docs.github.com/en/rest/reference/repos#webhooks>
  - <https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#push>
