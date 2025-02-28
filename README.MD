

![Logo](app/static/img/DDH.png)


Um projeto desenvolvido pelo SENAI-SP, para implementação em um projeto fomentado pelo FINEP.

Device Data Hub é um projeto com o objetivo de facilitar a distribuição de dados de dispositivos industriais, para a implementação de gemeos digitais, dashboards, entre outros.

O sistema oferece uma plataforma WEB onde conexões com dispositivos podem ser criadas e gerenciadas.

O Device Data Hub centraliza todos os dados coletados dos dispositivos em brokers MQTT, que podem também ser cadastrados e atrelados a uma conexão existente.




## Sobre dispositivos

Os dispositivos disponíveis para conexão serão adicionados conforme a demanda, não sendo possível a adição de um novo dispostivo via plataforma WEB, apenas pelo código (implementações futuras podem mudar a maneira como isso é feito).


## Observações antes de iniciarmos

O objetivo desse rojeto não é rodar em nuvem e sim em um servidor ou computador que deve estar na mesma rede que os dispositivos que terão seus respectivos dados coletados.
## Rodando o projeto

Para rodar o projeto localmente, siga os passos a seguir e se atente as observações.

- Necessário python Python 3.13.0.

1. Clone o repositório
```bash
  git clone https://github.com/Piovezan1207/Device-Data-Hub
```

2. Acesse a pasta do projeto
```bash
  cd Device-Data-Hub
```

3. Instale as dependencias necessárias
```bash
    pip install -r requirements.txt
```

4. Instancie o seu banco de dados
```bash
    python app\database\sqliteCreateTable.py
```
5. Faça uma códia do arquivo .env.example e renomeie para .env

6. Crie uma key rodando o script a baixo e copie o resultado que foi printado.
```
   python app\database\fernetKeyGenerator.py
```

7. Cole a key no arquivo .env.
```
   APP_KEY=<KEY COPIADA>
```

8. Acesse a pasta app
```bash
   cd app
```

9. Rode o projeto
```bash
   python app.py
```