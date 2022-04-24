---
title: Black Hat Python Book em Python3
---

### Black Hat Python Book em Python3

Esse repositório contem os códigos trabalhados no libro [Black Hat Python 1 Edição](https://www.amazon.com.br/dp/B06Y3L9ZXJ/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1), atualizados e convertidos para python 3. Tentando se aproximar ao máximo da [nova versão do livro publicada em Abril de 2021](https://nostarch.com/black-hat-python2E).

Aqui eu não fiz a organização dos códigos por capítulo. Fiz isso agrupando-os por áreas relacionadas. 

Por exemplo, os códigos relacionados ao Burp Suite foram alocados em um repositório chamado `burp/` que fica dentro de um repositório chamado `web/`. Já os arquivos relacionados ao tópico de `sniff/` estão alocados dentro de um repositório chamado `network/`.

### Estrutura do repositório

```
.
├── network
|   ├── sniff
|   |    ├── arper.pcap
|   |    ├── arper.py
|   |    ├── mail_sniffer.py
|   |    ├── pic_carver.py
|   |    ├── scanner.py
|   |    ├── sniffer_ip_header_decode.py
|   |    ├── sniffer.py
|   |    └── snnifer_with_icmp.py
│   ├── ssh
│   │   ├── diplomat
|   |   ├── README.md
|   |   ├── rfoward.py
│   │   ├── sshcmd.py
│   │   ├── sshrcmd.py
│   │   ├── sshserver.py
|   |   └── test_rsa.key
|   ├── nc.py
|   ├── tcpclient.py
|   ├── tcpproxy.py
|   ├── tcpserver.py
|   └── udpclient.py
├── trojan
|   ├── config
|   ├── data
|   └── modulesw
├── web
│   ├── burp
|   |   ├── bhp_bing.py 
|   |   └── bhp_fuzzer.py 
|   ├── all.txt
│   ├── cain.txt
│   ├── content_bruter.py
│   ├── joomla_killer.py
│   └── web_app_mapper.py
|   
└── README.md
```