# jackcompiler
Por Lucas Cléopas e Aridson Filho

## Uso rápido
Com o Python instalado, apenas rode no terminal :

`python main.py`

## Classe JackTokenizer
Para definir a classe JackTokenizer, importe-a:

`from JackTokenizer import *`

O parâmetro que ela recebe é apenas o nome do arquivo, por exemplo:

`tknz = JackTokenizer('name/to/path/file.jack')`

Após definir a instância da classe com o caminho para o arquivo `.jack`, ela carrega o arquivo e identifica os tokens nesse processo.

Para exportar o xml com os tokens, use:

`tknz.export_xml()`

## Classe CompilationEngine
Para definir a classe CompilationEngine, importe-a:

`from CompilationEngine import *`

O parâmetro que ela recebe é apenas uma instância do JackTokenizer, por exemplo:

`tknz = JackTokenizer('name/to/path/file.jack')`
`ce = CompilationEngine(tknz)`

Após definir a instância da classe, rode o comando `ce.run()` para executar a compilação.

O parse tree é feito e o xml é salvo no mesmo diretório do arquivo `.jack`

