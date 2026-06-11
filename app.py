import streamlit as st
import os
from openai import OpenAI
import networkx as nx
from pyvis.network import Network
import tempfile

# Configuration
st.set_page_config(page_title="Grok Harness Loop", layout="wide")

st.title("🚀 Grok Agent Harness Loop")
st.markdown("""Un agent avec boucle de raisonnement + visualisation du graphe des étapes."""")

# Sidebar for API key
with st.sidebar:
    st.header("Configuration")
    grok_api_key = st.text_input("Clé API Grok (xAI)", type="password", value=os.getenv("XAI_API_KEY", ""))
    if grok_api_key:
        os.environ["XAI_API_KEY"] = grok_api_key
    model = st.selectbox("Modèle", ["grok-4", "grok-3-mini"])
    max_iterations = st.slider("Max itérations", 5, 30, 15)

# Tabs
tab1, tab2 = st.tabs(["💬 Chatbot", "📊 Visualisation Graphe"])

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'graph' not in st.session_state:
    st.session_state.graph = nx.DiGraph()
if 'step_count' not in st.session_state:
    st.session_state.step_count = 0

client = None
if grok_api_key:
    client = OpenAI(api_key=grok_api_key, base_url="https://api.x.ai/v1")

# Tool: Web Search simulation (for demo, use real if possible)
def web_search(query):
    # Placeholder - in production use Tavily, SerpAPI or similar
    return f"Résultats de recherche pour '{query}' : [Simulation] Informations pertinentes trouvées."

# Simple agent loop logic
def run_agent_loop(task, max_iter):
    context = f"Tâche: {task}\n"
    steps = []
    G = st.session_state.graph
    
    for i in range(max_iter):
        step_id = f"step_{i}"
        G.add_node(step_id, label=f"Step {i+1}", title="Think & Act")
        if i > 0:
            G.add_edge(f"step_{i-1}", step_id)
        
        # Think
        think_prompt = f"""{context}
Pense étape par étape. Propose une action (outil ou raisonnement)."""
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": think_prompt}],
            temperature=0.7
        ).choices[0].message.content
        
        steps.append({"step": i, "think": response})
        context += f"\nStep {i}: {response}"
        
        # Simulate tool use
        if "recherche" in response.lower() or "search" in response.lower():
            tool_result = web_search("example query")
            context += f"\nRésultat outil: {tool_result}"
        
        if "terminé" in response.lower():
            break
    
    st.session_state.graph = G
    return steps

with tab1:
    task = st.text_area("Décris ta tâche / prompt", height=100)
    if st.button("Lancer l'Agent Loop") and client and task:
        with st.spinner("Agent en cours..."):
            steps = run_agent_loop(task, max_iterations)
            for step in steps:
                st.session_state.history.append(step)
    
    # Display history
    for msg in st.session_state.history:
        st.write(f"**Step {msg['step']}**")
        st.write(msg['think'])

with tab2:
    st.subheader("Visualisation de la boucle")
    if len(st.session_state.graph.nodes) > 0:
        net = Network(height="600px", width="100%", directed=True)
        net.from_nx(st.session_state.graph)
        net.set_options('''{
            "physics": {"enabled": true, "solver": "forceAtlas2Based"}
        }''')
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
            net.save_graph(tmp.name)
            with open(tmp.name, 'r', encoding='utf-8') as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=700)
    else:
        st.info("Lance une tâche pour voir le graphe des étapes.")

st.caption("Harness Loop MVP - Grok xAI + Streamlit + Pyvis")