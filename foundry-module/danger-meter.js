import { predictDanger } from "./ai-model.js";

Hooks.once("init", () => {
    console.log("🔥 TTRPG Danger Meter | Inicializando Módulo de IA Local");
});

Hooks.once("ready", () => {
    // Esquece a barra de ferramentas! O seu Foundry tem dezenas de módulos (The Ripper, TokenMagic, etc) 
    // que alteram a barra padrão do V12. Vamos criar nosso próprio botão Flutuante Indestrutível!
    
    // Evita duplicar
    if (document.getElementById("btn-danger-meter")) return;

    const btn = document.createElement("button");
    btn.id = "btn-danger-meter";
    btn.innerHTML = `<i class="fas fa-brain"></i> IA de Combate`;
    
    // Estilização braba pra ficar flutuando no canto inferior direito, perto do Chat
    Object.assign(btn.style, {
        position: "fixed",
        bottom: "80px",
        right: "320px", // Fica logo à esquerda da barra de chat
        zIndex: "9999",
        width: "140px",
        height: "40px",
        backgroundColor: "#ff6400",
        color: "white",
        border: "2px solid #222",
        borderRadius: "8px",
        boxShadow: "0 0 10px rgba(0,0,0,0.8)",
        cursor: "pointer",
        fontWeight: "bold",
        fontSize: "14px"
    });
    
    // Efeito de Hover (Brilhar ao passar o mouse)
    btn.onmouseenter = () => btn.style.backgroundColor = "#ff8533";
    btn.onmouseleave = () => btn.style.backgroundColor = "#ff6400";

    btn.addEventListener("click", () => {
        analyzeCurrentCombat();
    });

    document.body.appendChild(btn);
});

function analyzeCurrentCombat() {
    if (!canvas.tokens) return;
    
    const tokens = canvas.tokens.placeables;
    let partySize = 0;
    let totalPartyLevel = 0;
    let enemyCount = 0;
    let totalEnemyCr = 0;

    // Lógica para D&D 5.5e (dnd5e system)
    tokens.forEach(token => {
        const actor = token.actor;
        if (!actor) return;

        const isPlayer = actor.hasPlayerOwner;
        
        if (isPlayer) {
            partySize++;
            // Tenta pegar o level do jogador no sistema dnd5e
            totalPartyLevel += actor.system.details?.level || 1; 
        } else {
            enemyCount++;
            // Tenta pegar o CR do monstro
            totalEnemyCr += actor.system.details?.cr || 0.25;
        }
    });

    if (partySize === 0) {
        ui.notifications.warn("TTRPG Danger Meter: Nenhum jogador encontrado na cena!");
        return;
    }

    const avgPartyLevel = totalPartyLevel / partySize;
    const avgEnemyCr = enemyCount > 0 ? (totalEnemyCr / enemyCount) : 0;
    const actionEconomy = enemyCount / partySize;

    // Feature Array exigido pelo modelo: [party_size, party_level, enemy_count, enemy_cr, action_economy]
    const features = [partySize, avgPartyLevel, enemyCount, avgEnemyCr, actionEconomy];
    
    // Chama a nossa Inteligência Artificial Pura em JavaScript!
    const dangerScore = predictDanger(features);
    
    // Converte o score matemático (0.0 a 1.0) para algo legível
    let dangerLabel = "Fácil";
    let color = "green";
    
    if (dangerScore > 0.8) { dangerLabel = "TPK (Massacre Total)"; color = "darkred"; }
    else if (dangerScore > 0.6) { dangerLabel = "Mortal"; color = "red"; }
    else if (dangerScore > 0.4) { dangerLabel = "Difícil"; color = "orange"; }
    else if (dangerScore > 0.2) { dangerLabel = "Médio"; color = "yellow"; }

    // Exibe o resultado para o Mestre
    ChatMessage.create({
        speaker: { alias: "🧠 IA do Medidor de Perigo" },
        content: `
            <div style="border: 2px solid ${color}; padding: 10px; border-radius: 5px; background: rgba(0,0,0,0.1);">
                <h3 style="color: ${color}; text-align: center; margin-top: 0;">Análise de Combate (5.5e)</h3>
                <p><b>Aventureiros:</b> ${partySize} (Nível Médio: ${avgPartyLevel.toFixed(1)})</p>
                <p><b>Inimigos:</b> ${enemyCount} (CR Médio: ${avgEnemyCr.toFixed(1)})</p>
                <hr>
                <h2 style="text-align: center; color: ${color}; margin-bottom: 0;">Previsão: ${dangerLabel}</h2>
            </div>
        `,
        whisper: ChatMessage.getWhisperRecipients("GM") // Sussurra apenas para o GM
    });
}
