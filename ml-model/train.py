import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import m2cgen as m2c

# 1. Gerador de Dados Simulados (D&D 5.5e)
# Como não temos um dataset real de milhões de mesas de RPG, nós vamos gerar dados 
# baseados na matemática do sistema para ensinar a IA.
print("⚔️ Gerando simulações de encontros...")

data = []
for _ in range(5000):
    party_size = np.random.randint(3, 7)
    avg_party_level = np.random.randint(1, 21)
    
    enemy_count = np.random.randint(1, 15)
    avg_enemy_cr = np.random.uniform(0.25, 25.0)
    
    # Feature Engineering (O segredo da IA)
    # Economia de Ações é brutal no D&D
    action_economy_ratio = enemy_count / party_size 
    # Poder bruto aproximado
    party_power = party_size * avg_party_level
    enemy_power = enemy_count * avg_enemy_cr
    power_ratio = enemy_power / party_power if party_power > 0 else 0

    # Lógica Heurística (O que a IA vai tentar aprender e otimizar)
    # Danger = 0.0 (Fácil) até 1.0 (TPK)
    danger = (power_ratio * 0.7) + ((action_economy_ratio - 1) * 0.1)
    
    # Adicionando um pouco de ruído/caos (dados do mundo real nunca são perfeitos)
    danger += np.random.normal(0, 0.05)
    danger = np.clip(danger, 0.0, 1.0) # Garante que fique entre 0 e 1

    data.append([party_size, avg_party_level, enemy_count, avg_enemy_cr, action_economy_ratio, danger])

df = pd.DataFrame(data, columns=['party_size', 'party_level', 'enemy_count', 'enemy_cr', 'action_economy', 'danger_score'])

# 2. Treinando a Inteligência Artificial (Árvore de Decisão)
print("🧠 Treinando o modelo de Machine Learning...")
X = df[['party_size', 'party_level', 'enemy_count', 'enemy_cr', 'action_economy']]
y = df['danger_score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeRegressor(max_depth=5) # Profundidade 5 para não ficar muito pesado
model.fit(X_train, y_train)

score = model.score(X_test, y_test)
print(f"🎯 Precisão (R2 Score) do modelo: {score:.2f}")

# 3. A MÁGICA: Exportando a IA direto para JavaScript Puro!
print("⚡ Convertendo a IA para JavaScript nativo...")
js_code = m2c.export_to_javascript(model, function_name="predictDanger")

# Vamos envelopar a IA numa função limpa
final_js = f"""// AUTO-GENERATED MACHINE LEARNING MODEL (D&D 5.5e)
// Features: [party_size, party_level, enemy_count, enemy_cr, action_economy]

{js_code}

export {{ predictDanger }};
"""

with open("../foundry-module/ai-model.js", "w") as f:
    f.write(final_js)

print("✅ Sucesso! O modelo de IA foi injetado diretamente na pasta do Foundry Module!")
