# ATV_Transporte_Rodoviario
INTEGRAÇÃO E HOMOGENEIDADE DE DADOS EM UMA API DE TRANSPORTE RODOVIÁRIO
# API de Integração e Homogeneidade de Dados de Transporte Rodoviário

API acadêmica desenvolvida em **Python** e **FastAPI** para receber, em uma única requisição, viagens provenientes de diferentes companhias rodoviárias, identificar automaticamente a origem de cada objeto pela sua estrutura, validar os dados e convertê-los para um **contrato homogêneo de saída**.

A solução foi desenhada para atender a quatro integrações: **Auto Viação Progresso**, **Rota Transportes**, **Gontijo** e **Sertão Bus**.

## 1. Problema

Cada companhia representa informações equivalentes de maneiras diferentes: nomes de campos, estruturas JSON, formatos de data, unidades de duração, representação monetária e códigos de categoria variam entre as integrações.

A API elimina essa heterogeneidade e entrega aos consumidores um formato único e previsível, reduzindo acoplamento e simplificando a evolução do sistema.

## 2. Objetivos atendidos

- Receber vários formatos de viagem em um único array JSON.
- Identificar automaticamente a companhia sem campo `empresa` e sem cadeia de `if/elif` no fluxo principal.
- Validar e normalizar datas, fusos, duração, preço, categoria, UF e assentos.
- Preservar a ordem dos objetos recebidos.
- Rejeitar integralmente a requisição com HTTP `422` se qualquer objeto for inválido.
- Ignorar campos adicionais que não façam parte do contrato normalizado.
- Permitir a inclusão de novas companhias com alterações concentradas em uma nova Strategy, seu registro e seus testes.
- Aplicar orientação a objetos, Strategy, Registry e princípios SOLID.

## 3. Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| FastAPI | API REST e documentação OpenAPI/Swagger |
| Pydantic | Modelagem e serialização do contrato homogêneo |
| Uvicorn | Servidor ASGI |
| Pytest | Testes automatizados |
| HTTPX / TestClient | Testes de integração HTTP |
| `datetime` / `zoneinfo` | Datas, ISO 8601 e fusos horários |
| `Decimal` | Precisão monetária durante as conversões |

Dependências do projeto:

```text
fastapi==0.141.1
uvicorn==0.52.4
pytest==9.1.1
httpx==0.28.1
tzdata==2026.4
```

## 4. Endpoint

```http
POST /api/v1/viagens/normalizar
Content-Type: application/json
```

O corpo da requisição é **diretamente um array JSON**. Não existe campo `empresa`, `companhia`, `tipo` ou `integracoes` para selecionar a origem.

## 5. Exemplo de requisição

```json
[
  {
    "codigoViagem": "PRG-2026-001",
    "cidadeOrigem": "Paulo Afonso",
    "ufOrigem": "BA",
    "cidadeDestino": "Recife",
    "ufDestino": "PE",
    "dataHoraSaida": "15/10/2026 06:30",
    "dataHoraChegada": "15/10/2026 12:50",
    "fusoHorario": "America/Bahia",
    "tempoEstimado": "06:20",
    "valorPassagem": "129,90",
    "tipoServico": "EXECUTIVO",
    "assentosDisponiveis": "18"
  },
  {
    "trip_id": "ROT-2026-872",
    "origem": {"municipio": "Paulo Afonso", "estado": "BA"},
    "destino": {"municipio": "Aracaju", "estado": "SE"},
    "partida_em": "2026-10-15T07:00:00-03:00",
    "chegada_em": "2026-10-15T12:10:00-03:00",
    "duracao_minutos": 310,
    "tarifa_centavos": 8990,
    "moeda": "BRL",
    "classe": "convencional",
    "vagas": 22
  },
  {
    "serviceCode": "GON-2026-554",
    "from": {"city": "Paulo Afonso", "state": "BA"},
    "to": {"city": "Belo Horizonte", "state": "MG"},
    "departure": "2026-10-15T19:30:00Z",
    "arrival": "2026-10-16T12:10:00Z",
    "estimatedDurationSeconds": 60000,
    "fare": {"amount": "289.50", "currency": "BRL"},
    "serviceClass": "SEMI_SLEEPER",
    "availableSeats": 9
  },
  {
    "numero": "SER-2026-100",
    "rota": {"partida": "Paulo Afonso/BA", "chegada": "Maceió/AL"},
    "horarios": {
      "saida": "2026-10-16T08:00:00-03:00",
      "chegada": "2026-10-16T13:30:00-03:00"
    },
    "duracao_horas": 5.5,
    "preco_total": 105.90,
    "moeda": "BRL",
    "servico": "EXEC",
    "lugares_livres": 14
  }
]
```

## 6. Contrato homogêneo de saída

Todas as companhias são convertidas para a mesma estrutura:

```json
{
  "total": 1,
  "viagens": [
    {
      "id_viagem": "PRG-2026-001",
      "empresa": "Auto Viação Progresso",
      "origem": {"cidade": "Paulo Afonso", "uf": "BA"},
      "destino": {"cidade": "Recife", "uf": "PE"},
      "partida": "2026-10-15T06:30:00-03:00",
      "chegada": "2026-10-15T12:50:00-03:00",
      "duracao_minutos": 380,
      "preco": {"valor": 129.90, "moeda": "BRL"},
      "categoria": "executivo",
      "assentos_disponiveis": 18
    }
  ]
}
```

## 7. Arquitetura

```text
Requisição HTTP
      |
      v
FastAPI
      |
      v
POST /api/v1/viagens/normalizar
      |
      v
NormalizacaoService
      |
      v
StrategyRegistry
      |
      v
strategy.identifica(payload)
      |
      v
Strategy da companhia
      |
      +--> conversores
      +--> validadores
      |
      v
ViagemNormalizada (Pydantic)
      |
      v
ViagensResponse
      |
      v
Resposta HTTP
```

Estrutura principal:

```text
app/
├── api/routes/viagens.py
├── domain/
│   ├── models/viagem.py
│   ├── registry.py
│   ├── strategies/
│   │   ├── base.py
│   │   ├── progresso.py
│   │   ├── rota.py
│   │   ├── gontijo.py
│   │   └── sertao_bus.py
│   └── utils/
│       ├── conversores.py
│       └── validadores.py
├── exceptions/viagem.py
├── services/normalizacao.py
└── main.py

tests/
```

## 8. Strategy Pattern

Cada companhia implementa o mesmo contrato abstrato:

```python
class ViagemStrategy(ABC):
    @abstractmethod
    def identifica(self, payload: dict[str, Any]) -> bool:
        ...

    @abstractmethod
    def normaliza(self, payload: dict[str, Any]) -> ViagemNormalizada:
        ...

    @abstractmethod
    def nome_empresa(self) -> str:
        ...
```

O padrão Strategy isola as regras de identificação e normalização de cada companhia. Assim, o fluxo principal não precisa conhecer os detalhes de Progresso, Rota, Gontijo ou Sertão Bus.

## 9. Registry

O `StrategyRegistry` mantém as Strategies disponíveis e procura a primeira capaz de reconhecer o payload:

```python
for strategy in self._strategies:
    if strategy.identifica(payload):
        return strategy
```

Isso atende ao requisito arquitetural de evitar uma cadeia de `if/elif/else` para selecionar a companhia.

## 10. Fluxo de normalização por companhia

| Companhia | Identificação | Conversões principais |
|---|---|---|
| Progresso | `codigoViagem`, `cidadeOrigem`, `dataHoraSaida`... | `dd/mm/aaaa HH:MM`, preço brasileiro, `HH:MM`, assentos em texto |
| Rota | `trip_id`, `origem`, `destino`, `partida_em`... | ISO 8601, centavos para reais, duração já em minutos |
| Gontijo | `serviceCode`, `from`, `to`, `departure`... | UTC para America/Bahia, segundos para minutos, `fare.amount`, `SEMI_SLEEPER` |
| Sertão Bus | `numero`, `rota`, `horarios`, `duracao_horas`... | `Cidade/UF`, horas decimais para minutos, preço decimal, `EXEC` |

## 11. Regras de normalização

A solução final aplica as seguintes regras:

1. Identifica a companhia pela estrutura do objeto.
2. Converte todas as datas para ISO 8601.
3. Usa `America/Bahia` quando não há fuso e converte datas com outro offset para esse fuso.
4. Converte durações para minutos inteiros.
5. Converte valores monetários para decimal e preserva a moeda.
6. Serializa `preco.valor` como número JSON.
7. Converte assentos para inteiro.
8. Padroniza categorias em `convencional`, `executivo`, `semileito` ou `leito`.
9. Ignora campos adicionais.
10. Não expõe campos particulares das companhias no contrato final.

## 12. Validações

A requisição é rejeitada quando:

- o formato não corresponde a nenhuma Strategy;
- falta um campo obrigatório;
- data, duração, preço ou assentos não podem ser convertidos;
- chegada é anterior ou igual à saída;
- duração informada não corresponde aos horários;
- preço ou duração é menor ou igual a zero;
- assentos são negativos;
- UF não possui exatamente dois caracteres;
- categoria não pode ser normalizada.

Se um único objeto for inválido, **nenhum resultado parcial é retornado**.

## 13. Resposta de erro

```json
{
  "detail": {
    "indice": 1,
    "empresa_identificada": "Rota Transportes",
    "campo": "chegada_em",
    "mensagem": "A data de chegada deve ser posterior à data de saída."
  }
}
```

Formato desconhecido:

```json
{
  "detail": {
    "indice": 1,
    "empresa_identificada": null,
    "campo": null,
    "mensagem": "O formato do payload não corresponde a nenhuma companhia suportada."
  }
}
```

## 14. SOLID e decisões de projeto

### SRP - Single Responsibility Principle

- Route: HTTP.
- Service: orquestração.
- Registry: descoberta da Strategy.
- Strategy: regras de uma companhia.
- Conversores: transformação de tipos/unidades.
- Validadores: regras comuns.
- Models: contrato normalizado.

### OCP - Open/Closed Principle

O fluxo principal permanece estável quando uma nova companhia é adicionada. A extensão ocorre por uma nova Strategy, registro e testes.

### Polimorfismo

Todas as integrações são tratadas pelo tipo abstrato `ViagemStrategy`, permitindo que o Service trabalhe com uma interface comum.

## 15. Banco de dados

A API não utiliza banco de dados nesta entrega. Essa é uma decisão de arquitetura coerente com o escopo: o endpoint recebe dados, transforma-os e devolve o resultado na mesma requisição, sem requisito de persistência.

Portanto, a solução é **stateless**. Se persistência for necessária futuramente, ela pode ser adicionada em uma camada de repositório sem alterar as regras de identificação e normalização.

## 16. Instalação

```bash
git clone <URL_DO_REPOSITORIO>
cd ATV_Transporte_Rodoviario-main
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Git Bash:

```bash
source .venv/Scripts/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## 17. Execução

```bash
uvicorn app.main:app --reload
```

A documentação interativa fica disponível em:

```text
http://127.0.0.1:8000/docs
```

## 18. Testes

Execute:

```bash
python -m pytest -q
```

A suíte deve cobrir:

- normalização das quatro companhias;
- ordem preservada;
- identificação pelo Registry;
- formato desconhecido;
- campo obrigatório ausente;
- data inválida;
- chegada anterior/igual à saída;
- duração zero, negativa ou incompatível;
- preço inválido, zero ou negativo;
- assentos negativos;
- UF inválida;
- categoria inválida;
- rejeição integral da requisição;
- serialização do contrato final.

## 19. Como adicionar uma nova companhia

1. Criar uma classe que herde de `ViagemStrategy`.
2. Implementar `identifica()` usando características exclusivas do payload.
3. Implementar `normaliza()` convertendo o payload para `ViagemNormalizada`.
4. Implementar `nome_empresa()`.
5. Registrar a nova Strategy no `StrategyRegistry`.
6. Criar testes unitários e de integração para a nova companhia.

Não é necessário alterar o endpoint, o contrato de saída, o `NormalizacaoService` ou as Strategies existentes.

## 20. Decisão de extensibilidade

O sistema segue a regra:

> **A companhia conhece seu formato; o fluxo principal conhece apenas a interface.**

Esse desenho reduz acoplamento, melhora coesão e torna a inclusão de novas integrações previsível.

## 21. Status

A solução de entrega contempla:

- quatro companhias suportadas;
- identificação automática por estrutura;
- contrato homogêneo;
- normalização de timezone, duração, preço, categoria e assentos;
- validações exigidas;
- erro HTTP 422 sem resultado parcial;
- Strategy + Registry;
- testes automatizados;
- documentação de instalação, execução e extensibilidade.
