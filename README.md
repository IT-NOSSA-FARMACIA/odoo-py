# odoo-py

**odoo-py** é uma biblioteca Python projetada para facilitar a interação com servidores Odoo através de chamadas RPC (Remote Procedure Call). Esta biblioteca oferece uma interface simplificada para desenvolvedores que desejam integrar ou automatizar operações no Odoo sem a necessidade de lidar diretamente com as complexidades das chamadas XML-RPC ou JSON-RPC.

## Funcionalidades

- **Conexão Simplificada**: Estabelece conexões com servidores Odoo utilizando protocolos XML-RPC ou JSON-RPC.
- **Operações CRUD**: Permite criar, ler, atualizar e excluir registros nos modelos do Odoo de forma intuitiva.
- **Execução de Métodos**: Facilita a chamada de métodos personalizados definidos nos modelos do Odoo.
- **Gestão de Contexto**: Suporta o gerenciamento do contexto do usuário, permitindo operações que respeitam permissões e configurações específicas.

## Instalação

Para instalar o **odoo-py**, utilize o pip:

```bash
pip install odoo-py
```

## Configuração de Credenciais
Recomenda-se armazenar as credenciais de acesso ao Odoo num ficheiro .env para garantir segurança e organização.

Crie um ficheiro .env na raiz do seu projeto com o seguinte conteúdo:

```bash
ODOO_URL=http://localhost
ODOO_DB=nome_do_banco
ODOO_USERNAME=usuario
ODOO_PASSWORD=senha
```

Em seguida, instale a biblioteca environs para gerir variáveis de ambiente:
```bash
pip install environs
```

Exemplo de carregamento das variáveis com environs:


```python3
from environs import Env

# Inicializa e carrega variáveis do ficheiro .env
env = Env()
env.read_env()

```

## Exemplo de Uso
Abaixo apresenta-se um exemplo de integração com Odoo através da classe OdooIntegration, utilizando o modelo PartnerModel para consultar contactos com base no NIF (VAT):

```python3
from odoo import PartnerModel

# Exceção personalizada para sinalizar que um ou mais contactos não foram encontrados
class ContactsNotFound(Exception):
    pass

# Classe de integração com o Odoo, focada na entidade 'res.partner'
class OdooIntegration:
    def __init__(self):
        # Instancia o modelo de parceiros, encapsulando a lógica de acesso à API do Odoo
        self._partner_model = PartnerModel()

    def get_contact_by_vat(self, vat: str):
        """
        Obtém um contacto (empresa) no Odoo com base no NIF (VAT).
        - Se nenhum contacto for encontrado, levanta uma exceção.
        - Se mais de um contacto for encontrado com o mesmo NIF, também levanta exceção.
        - Se apenas um contacto for encontrado, retorna os seus dados.
        """
        # Define o filtro de pesquisa: NIF exacto e deve ser uma empresa
        filter_partner = [["vat", "=", vat], ["is_company", "=", True]]

        # Executa a consulta no Odoo e lê os campos especificados
        contact = self._partner_model.get_and_read_partners_by_any_filter(
            filter=filter_partner, fields=["id", "name", "is_company"]
        )

        # Registo da resposta para efeitos de depuração
        print(contact)

        # Validação dos resultados obtidos
        if not contact:
            # Nenhum resultado encontrado
            raise ContactsNotFound(f"Contact with VAT {vat} not found")
        elif len(contact) == 1:
            # Resultado único — retorna o contacto
            return contact[0]
        elif len(contact) > 1:
            # Múltiplos resultados — compõe mensagem detalhada e levanta exceção
            except_message = [
                f"{c['id']} - {c['name']} - is_company: {c['is_company']}"
                for c in contact
            ]
            raise ContactsNotFound(
                "More than one contact with the same "
                f"VAT {vat}. Contacts: {except_message}"
            )
```

## Remoção
Se desejar remover a biblioteca do seu ambiente Python, utilize o seguinte comando:

```bash
pip uninstall odoo-py
```

## Contribuição
Contribuições para o aprimoramento do odoo-py são bem-vindas. Caso identifique problemas ou deseje sugerir melhorias, por favor, submeta um issue ou pull request no repositório oficial do projeto.

## Licença
O **odoo-py** é distribuído sob a licença MIT. Para mais detalhes, consulte o arquivo LICENSE no repositório do projeto.
