# TTRPG Danger Meter (5.5e AI)

![Foundry Version](https://img.shields.io/badge/Foundry-v11%20%7C%20v12-blue)
![System](https://img.shields.io/badge/System-D&D%205.5e-red)

Um módulo para Foundry VTT que utiliza Machine Learning local para prever a verdadeira letalidade de um encontro em D&D 5.5e.

## 🧠 Como Funciona?
O sistema tradicional de *Challenge Rating* (CR) de D&D frequentemente falha em prever a real dificuldade de um combate. Este módulo analisa os tokens presentes na cena ativa (Nível médio dos jogadores, CR dos monstros e, principalmente, a Economia de Ações) e submete essas características a um modelo de **Inteligência Artificial (Árvore de Decisão)** que foi treinado com milhares de simulações de combate.

O modelo roda 100% offline, embutido no próprio JavaScript do módulo, retornando o resultado em milissegundos diretamente no chat do Mestre.

## 📦 Como Usar
1. Instale o módulo e ative-o no seu Mundo (exclusivo para o sistema `dnd5e`).
2. Arraste tokens de Jogadores e de Inimigos para o mapa.
3. No menu lateral esquerdo de **Token Controls**, clique no ícone do **Cérebro (🧠)**.
4. O módulo sussurrará a previsão de dificuldade (Fácil, Médio, Difícil, Mortal ou TPK) no seu Chat Log.

## 🛠️ Arquitetura e Desenvolvimento
Este repositório é dividido em duas partes:
* `/ml-model`: Scripts em Python (`scikit-learn`) usados para simular combates, treinar a IA e exportar o modelo treinado para código JavaScript nativo usando `m2cgen`.
* `/foundry-module`: O módulo de Foundry propriamente dito, que importa a IA gerada e injeta a interface gráfica no VTT.

### Requisitos para desenvolvimento:
- Python 3.10+
- Pandas, Numpy, Scikit-Learn e m2cgen.

## 📜 Licença
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
