# Grok Harness Loop Streamlit

Un agent autonome avec boucle de raisonnement (Think-Act-Observe-Reflect) utilisant Grok xAI.

## Fonctionnalités
- **Interface Chatbot** : Lance des tâches agentiques.
- **Boucle complète** : Think → Act (outils) → Observe → Reflect.
- **Visualisation Graphe** : Noeuds et arêtes montrant chaque étape en temps réel.
- **Outil** : Recherche web (simulation, extensible).
- **LLM** : Grok via xAI API (clé à fournir).

## Installation locale
```bash
git clone https://github.com/Ulml/grok-harness-loop-streamlit.git
cd grok-harness-loop-streamlit
pip install -r requirements.txt
streamlit run app.py
```

Configure ta clé API Grok dans le sidebar ou via `export XAI_API_KEY=...`.

## Améliorations futures
- Intégration vraie Tavily/SerpAPI pour web search.
- Plus d'outils (code execution, file editing).
- Mémoire vectorielle.
- Streaming des étapes.

Créé avec ❤️ par Grok pour toi !