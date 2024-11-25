Título do Relatório:
Resumo de Dados para o Projeto de Recomendação Personalizada de Veículos

Data:
12/06/2024

Responsável:
12/12/2024

1. Fontes de Dados

1.1. fueleconomy.gov

	•	Tipo de Dados:
	•	Dados de Veículos: Informações sobre veículos disponíveis, incluindo:
	•	Marca
	•	Ano de fabricação
	•	Cilindros
	•	Litragem do Moto
	•	Modelo
	•	Tipo de Gasolina
	•	Consumo na Cidade
	•	Consumo na Rodovia
	•	Consumo combinado.
	•	Autonomia Total
	•	Galões por Milhas
	•	Objetivo de Uso:
	•	Extração de Dados: Coletar dados brutos de veículos disponíveis na fueleconomy.gov para análise e recomendação.
	•	Personalização: Usar os dados para comparar e recomendar veículos que correspondam às características especificadas pelo usuário.
	•	Integração do Modelo: Alimentar o modelo de LLM com dados para melhorar a precisão das recomendações.

1.2. Dados do Usuário

	•	Tipo de Dados:
	•	Preferências do Usuário: Informações fornecidas pelos usuários sobre as características desejadas em um veículo, como:
	•	Tipo de veículo (sedan, SUV, hatchback, etc.)
	•	Faixa de preço
	•	Ano de fabricação (preferido)
	•	Tipo de combustível
	•	Quilometragem máxima
	•	Localização preferida
	•	Objetivo de Uso:
	•	Personalização: Ajustar os critérios de busca com base nas preferências fornecidas para gerar recomendações mais relevantes.
	•	Interação com a Interface: Capturar as entradas dos usuários através da interface Streamlit e processar essas informações para gerar sugestões.

1.3. Dados de Feedback dos Usuários

	•	Tipo de Dados:
	•	Avaliações e Comentários: Feedback fornecido pelos usuários após utilizarem a aplicação, incluindo:
	•	Nível de satisfação com as recomendações
	•	Relevância das opções sugeridas
	•	Sugestões de melhorias
	•	Objetivo de Uso:
	•	Avaliação do Desempenho: Medir a precisão e a relevância das recomendações feitas pela aplicação.
	•	Melhoria Contínua: Identificar áreas para aprimoramento com base no feedback recebido e ajustar o modelo e a interface conforme necessário.

2. Descrição dos Dados

2.1. fueleconomy.gov

	•	Formato: Dados extraídos de páginas da fueleconomy.gov em formato HTML, transformados em formato estruturado (CSV) após o web scraping.
	•	Qualidade: A qualidade dos dados dependerá da consistência das informações disponíveis nas páginas da fueleconomy.gov e da eficácia do processo de scraping.

2.2. Dados do Usuário

	•	Formato: Dados inseridos pelos usuários na interface da aplicação em formato estruturado (CSV).
	•	Qualidade: Baseia-se na precisão das entradas fornecidas pelos usuários e na capacidade da aplicação de validar essas informações.

2.3. Dados de Feedback dos Usuários

	•	Formato: Dados coletados através de formulários de feedback em formato de texto e avaliações estruturadas (CSV).
	•	Qualidade: Depende da clareza e da utilidade das respostas fornecidas pelos usuários.

3. Estratégia de Coleta e Armazenamento

	•	Coleta de Dados da fueleconomy.gov: Utilização de técnicas de web scraping para extrair dados e armazená-los em uma base de dados estruturada.
	•	Coleta de Dados do Usuário: Interface Streamlit para captura de preferências e armazenamento em uma base de dados.
	•	Coleta de Dados de Feedback: Implementação de formulários de feedback na aplicação para coleta e análise contínua.

4. Considerações sobre a Qualidade dos Dados

	•	Precisão: Verificar a precisão dos dados extraídos da fueleconomy.gov e garantir que as informações fornecidas pelos usuários sejam corretas.
	•	Consistência: Garantir que os dados extraídos e as entradas dos usuários sejam consistentes e estejam livres de erros.
	•	Atualização: Atualizar periodicamente os dados da fueleconomy.gov para refletir as informações mais recentes sobre os veículos disponíveis.