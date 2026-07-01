import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import m2cgen as m2c

# 1. Gerador de Dados Simulados (D&D 5.5e)
# Como não temos um dataset real de milhões de mesas de RPG, nós vamos gerar dados 
# baseados na matemática do sistema para ensinar a IA.
print("⚔️ Gerando simulações de encontros...")

def get_encounter_multiplier(enemy_count):
    if enemy_count == 1: return 1.0
    if enemy_count == 2: return 1.5
    if enemy_count <= 6: return 2.0
    if enemy_count <= 10: return 2.5
    if enemy_count <= 14: return 3.0
    return 4.0

data = []
for _ in range(15000): # 15.000 simulações para a IA ficar bem treinada
    party_size = np.random.randint(3, 7)
    avg_party_level = np.random.randint(1, 21)
    
    enemy_count = np.random.randint(1, 15)
    avg_enemy_cr = np.random.uniform(0.125, 30.0)
    
    # Feature Engineering Avançado (Matemática real do D&D 5e)
    # O poder de um personagem escala de forma quase exponencial, não linear.
    party_power = party_size * (avg_party_level ** 1.2) * 10
    
    # O poder dos monstros também.
    enemy_base_power = enemy_count * (avg_enemy_cr ** 1.2) * 40
    
    # D&D 5e Action Economy Multiplier
    multiplier = get_encounter_multiplier(enemy_count)
    total_enemy_power = enemy_base_power * multiplier
    
    power_ratio = total_enemy_power / party_power if party_power > 0 else 0

    # Traduzindo o ratio de poder para a escala de Perigo (0.0 a 1.0)
    # Ratio 0.5 = Fácil (~0.2)
    # Ratio 1.2 = Médio (~0.4)
    # Ratio 1.8 = Difícil (~0.6)
    # Ratio 2.5 = Mortal (~0.8)
    # Ratio 3.0+ = TPK (1.0)
    danger = power_ratio / 3.0
    
    # Adicionando um pouco de caos (dados do mundo real nunca são perfeitos)
    danger += np.random.normal(0, 0.05)
    danger = np.clip(danger, 0.0, 1.0)

    action_economy_ratio = enemy_count / party_size 
    data.append([party_size, avg_party_level, enemy_count, avg_enemy_cr, action_economy_ratio, danger])

df = pd.DataFrame(data, columns=['party_size', 'party_level', 'enemy_count', 'enemy_cr', 'action_economy', 'danger_score'])

# 2. Treinando a Inteligência Artificial (Árvore de Decisão)
print("🧠 Treinando o modelo de Machine Learning...")
X = df[['party_size', 'party_level', 'enemy_count', 'enemy_cr', 'action_economy']]
y = df['danger_score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Profundidade aumentada para 8 para a IA entender melhor cenários complexos
model = DecisionTreeRegressor(max_depth=8)
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
