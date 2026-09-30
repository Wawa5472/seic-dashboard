import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import base64
import os

# Configuration générale
st.set_page_config(page_title="SEIC - Supply Chain & Reverse Logistics", layout="wide")

# Fonction pour encoder le logo local en base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_b64 = get_base64_image("logo.png")

# Styles SEIC
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }

    /* En-tête officiel SEIC */
    .seic-header {
        background: linear-gradient(135deg, #0B2545 0%, #005A9C 100%);
        border-radius: 14px;
        padding: 20px 32px;
        color: white;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 90, 156, 0.15);
    }
    .seic-logo-container {
        display: flex;
        align-items: center;
        gap: 18px;
    }
    .seic-logo-img {
        max-height: 65px;
        width: auto;
        object-fit: contain;
    }
    .seic-brand h1 {
        font-size: 38px;
        font-weight: 800;
        margin: 0;
        color: white;
        line-height: 1;
    }
    .seic-brand span {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        color: #7CD1F9;
        text-transform: uppercase;
    }
    .seic-motto {
        text-align: right;
        font-size: 13px;
        font-weight: 600;
        color: #E2E8F0;
        border-left: 2px solid #00A3E0;
        padding-left: 18px;
    }

    /* Onglets principaux */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 8px 8px 0px 0px;
        padding: 12px 20px;
        font-weight: 700;
        font-size: 13.5px;
        color: #0B2545;
        border: 1px solid #E2E8F0;
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #005A9C !important;
        color: #FFFFFF !important;
        border-color: #005A9C !important;
    }

    .step-card {
        background: white;
        border-radius: 12px;
        padding: 20px 16px;
        border-top: 5px solid #005A9C;
        box-shadow: 0 2px 10px rgba(11, 37, 69, 0.06);
        min-height: 220px;
    }
    .step-badge {
        background-color: #0B2545;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 12px;
    }

    .decision-card-green {
        background: #F0FDF4;
        border: 2px solid #22C55E;
        border-radius: 12px;
        padding: 22px;
    }
    .decision-card-red {
        background: #FEF2F2;
        border: 2px solid #EF4444;
        border-radius: 12px;
        padding: 22px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 16px 20px;
        border-radius: 10px;
        border-left: 4px solid #00A3E0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .scenario-box {
        background: white;
        border-radius: 12px;
        padding: 18px 24px;
        border: 1.5px solid #00A3E0;
        margin-bottom: 15px;
    }
    .financial-card {
        background: white;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }
    .total-card-highlight {
        background: linear-gradient(135deg, #0B2545 0%, #005A9C 100%);
        color: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 4px 15px rgba(0, 90, 156, 0.2);
    }
    .capex-card {
        background: white;
        border-radius: 10px;
        padding: 16px;
        border-top: 4px solid #00A3E0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .strategy-card {
        background: white;
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-top: 4px solid #0B2545;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Fonction de calcul de distance (Haversine)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return int(R * c)

# Construction de l'en-tête
if logo_b64:
    logo_markup = f'<img src="data:image/png;base64,{logo_b64}" class="seic-logo-img" alt="Logo SEIC">'
else:
    logo_markup = """
    <div class="seic-brand">
        <h1>SEIC</h1>
        <span>Smart Electronic Items Corporation</span>
    </div>
    """

st.markdown(f"""
<div class="seic-header">
    <div class="seic-logo-container">
        {logo_markup}
    </div>
    <div class="seic-motto">
        Moins de dechets<br>
        Plus de valeur<br>
        Plus durable
    </div>
</div>
""", unsafe_allow_html=True)

# Définition des partenaires
PARTENAIRES = {
    "Inde (Nagpur) - Modele Actuel": {
        "nom": "Partenaire Valorisation (Inde)",
        "lat": 20.5937,
        "lon": 78.9629,
        "mode": "Maritime + Routier",
        "facteur_cout": 1.00,
        "cout_tonne_km": 0.08,
        "emissions_ratio": "Eleve (Maritime long courrier)"
    },
    "Pologne (Cracovie) - Nearshoring UE": {
        "nom": "Partenaire Valorisation (Pologne)",
        "lat": 50.0647,
        "lon": 19.9450,
        "mode": "Fluvial / Ferroviaire direct",
        "facteur_cout": 0.42,
        "cout_tonne_km": 0.04,
        "emissions_ratio": "Tres faible (-78% CO2)"
    },
    "France (Lyon - Plastipolis)": {
        "nom": "Pole Recyclage Polymeres (France)",
        "lat": 45.7640,
        "lon": 4.8357,
        "mode": "Routier / Rail combine",
        "facteur_cout": 0.55,
        "cout_tonne_km": 0.05,
        "emissions_ratio": "Faible (-62% CO2)"
    },
    "Turquie (Bursa) - Alternative Mediterranee": {
        "nom": "Hub Plasturgie (Turquie)",
        "lat": 40.1885,
        "lon": 29.0610,
        "mode": "Ro-Ro Maritime court",
        "facteur_cout": 0.72,
        "cout_tonne_km": 0.065,
        "emissions_ratio": "Moyen (-35% CO2)"
    }
}

USINE_SLOVAQUIE = {"lat": 48.6690, "lon": 19.6990}

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Globe 3D & Simulateur de Relocalisation",
    "2. Reverse Logistics & RSE",
    "3. Strategie CODIR & Modele Hybride",
    "4. Assistant Finance & KPI Dynamiques"
])

# =====================================================================================
# ONGLET 1 : GLOBE 3D + SIMULATEUR RELOCALISATION
# =====================================================================================
with tab1:
    st.subheader("Simulateur Interactif de Fret & Cartographie 3D")
    
    c_sel1, c_sel2 = st.columns([2, 1])
    with c_sel1:
        choix_partenaire = st.selectbox(
            "Selectionnez la localisation du prestataire de recyclage des resines plastiques :",
            list(PARTENAIRES.keys()),
            index=0
        )
    
    partenaire_actif = PARTENAIRES[choix_partenaire]
    dist_km = haversine_distance(USINE_SLOVAQUIE["lat"], USINE_SLOVAQUIE["lon"], partenaire_actif["lat"], partenaire_actif["lon"])
    base_dist = haversine_distance(USINE_SLOVAQUIE["lat"], USINE_SLOVAQUIE["lon"], PARTENAIRES["Inde (Nagpur) - Modele Actuel"]["lat"], PARTENAIRES["Inde (Nagpur) - Modele Actuel"]["lon"])
    gain_km = base_dist - dist_km

    with c_sel2:
        st.metric(
            label="Distance depuis l'usine (Slovaquie)",
            value=f"{dist_km:,} km".replace(",", " "),
            delta=f"-{gain_km:,} km".replace(",", " ") if gain_km > 0 else "Base reference",
            delta_color="normal" if gain_km > 0 else "off"
        )

    sites = [
        {"nom": "Hub Hambourg (Allemagne)", "role": "Centre Reverse Logistics & Tri", "lat": 53.5511, "lon": 9.9937, "color": "#00FF66"},
        {"nom": "Usine & Incinerateur (Slovaquie)", "role": "Production (29M) & Valorisation", "lat": 48.6690, "lon": 19.6990, "color": "#00E5FF"},
        {"nom": "Usine Assemblage (Portugal)", "role": "Moulage injection plastique", "lat": 39.3999, "lon": -8.2245, "color": "#00E5FF"},
        {"nom": partenaire_actif["nom"], "role": f"Valorisation ({partenaire_actif['mode']})", "lat": partenaire_actif["lat"], "lon": partenaire_actif["lon"], "color": "#FF9900"}
    ]
    df_sites = pd.DataFrame(sites)

    fig = go.Figure()

    flux = [
        ([-8.2245, 9.9937], [39.3999, 53.5511], "#00E5FF", "Flux Portugal -> Hub Hambourg"),
        ([19.6990, 9.9937], [48.6690, 53.5511], "#00E5FF", "Flux Slovaquie -> Hub Hambourg"),
        ([9.9937, 19.6990], [53.5511, 48.6690], "#FF3366", "Flux Dechets -> Incinerateur Slovaquie"),
        ([19.6990, partenaire_actif["lon"]], [48.6690, partenaire_actif["lat"]], "#FFAA00", f"Flux Recyclage Resines -> {partenaire_actif['nom']}")
    ]

    for lons, lats, col, name in flux:
        fig.add_trace(go.Scattergeo(
            lon=lons, lat=lats, mode="lines",
            line=dict(width=3, color=col),
            hoverinfo="text", text=name, name=name
        ))

    fig.add_trace(go.Scattergeo(
        lon=df_sites["lon"],
        lat=df_sites["lat"],
        mode="markers+text",
        text=df_sites["nom"],
        textposition="top center",
        textfont=dict(color="#FFFFFF", size=12, family="Inter"),
        marker=dict(size=14, color=df_sites["color"], line=dict(width=2, color="#FFFFFF")),
        hoverinfo="text", hovertext=df_sites["nom"] + "<br>Role: " + df_sites["role"],
        name="Sites Actifs"
    ))

    target_lon = 20 if dist_km < 3000 else 45
    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=True, coastlinecolor="#5c7f4e",
        showland=True, landcolor="#2c3e27",
        showocean=True, oceancolor="#0c1e36",
        showcountries=True, countrycolor="#415a37",
        showlakes=True, lakecolor="#0c1e36",
        projection_rotation=dict(lon=target_lon, lat=40, roll=0),
        bgcolor="rgba(0,0,0,0)"
    )

    fig.update_layout(
        height=580,
        margin=dict(r=0, t=10, l=0, b=0),
        paper_bgcolor="#030712",
        plot_bgcolor="#030712",
        legend=dict(x=0.02, y=0.05, bgcolor="rgba(11,37,69,0.9)", bordercolor="#00A3E0", borderwidth=1, font=dict(color="#FFFFFF", size=11))
    )

    st.plotly_chart(fig, use_container_width=True)

    cout_sortant_base = 173.6 * 0.31
    cout_sortant_simule = cout_sortant_base * partenaire_actif["facteur_cout"]
    economie_annuelle = cout_sortant_base - cout_sortant_simule

    st.markdown(f"""
    <div class="scenario-box">
        <h4 style="color:#005A9C; margin-top:0;">Bilan d'impact du scenario : {choix_partenaire}</h4>
        <div style="display:flex; justify-content:space-between; flex-wrap:wrap;">
            <div>• <b>Mode de transport :</b> {partenaire_actif['mode']}</div>
            <div>• <b>Impact Carbone :</b> {partenaire_actif['emissions_ratio']}</div>
            <div>• <b>Cout du fret sortant :</b> {cout_sortant_simule:.2f} M€ (vs {cout_sortant_base:.2f} M€ en Inde)</div>
            <div style="color:{'#16A34A' if economie_annuelle > 0 else '#0B2545'}; font-weight:700;">
                • <b>Gain logistique net annuel : +{economie_annuelle:.2f} M€ / an</b>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================================
# ONGLET 2 : REVERSE LOGISTICS & RSE
# =====================================================================================
with tab2:
    st.subheader("Processus Operationnel de Reverse Logistics")
    st.caption("Standardisation des etapes de diagnostic, d'hygiene et seuil de decision economique.")

    c1, c2, c3, c4, c5 = st.columns(5)
    steps = [
        ("1", "Retour client -> Reception", "• Collecte des retours<br>• Enregistrement SI<br>• Tracabilite a l'arrivee"),
        ("2", "Tri et diagnostic", "• Analyse technique bloc/moteur<br>• Choix de la filiere adaptee"),
        ("3", "Desinfection", "• Nettoyage approfondi<br>• Respect des regles d'hygiene"),
        ("4", "Reconditionnement", "• Remplacement pieces d'usure<br>• Controle qualite usine<br>• Nouveau packaging"),
        ("5", "Controle & revente", "• Validation finale<br>• Remise marche secondaire")
    ]
    for col, (num, title, desc) in zip([c1, c2, c3, c4, c5], steps):
        with col:
            st.markdown(f"""
            <div class="step-card">
                <div>
                    <div class="step-badge">{num}</div>
                    <div style="color:#0B2545; font-weight:700; font-size:14px; margin-bottom:8px;">{title}</div>
                    <p style="color:#4A5568; font-size:12px; line-height:1.5;">{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Arbitrage Economique & Critere de Rentabilite")
    st.caption("Une tondeuse dont la valeur de revente estimee est inferieure a 20 € n'est pas rentable a reconditionner.")

    sim1, sim2 = st.columns(2)
    with sim1:
        valeur = st.slider("Valeur de revente estimee (€)", 5.0, 40.0, 28.73, 0.5)
        etat = st.radio("Etat technique de l'appareil :", ["Fonctionnel / Piece remplacable", "Hors d'usage (irreparable)"])
    with sim2:
        if valeur >= 20.0 and etat == "Fonctionnel / Piece remplacable":
            st.markdown(f"""
            <div class="decision-card-green">
                <h4 style="color:#16A34A; margin-top:0;">Produit reconditionne (Valeur >= 20 €)</h4>
                <p style="margin-bottom:8px;"><strong>Action :</strong> Reconditionnement et revente sur le marche secondaire.</p>
                <span style="font-size:13px; color:#475569;">
                • Cout remise a neuf : 5,63 € (44% du cout de fabrication standard de 12,80 €)<br>
                • Nouveau packaging blister et certification sanitaire
                </span>
                <div style="margin-top:12px; font-weight:700; color:#0F172A;">
                    Marge brute estimee : {(valeur - 5.63):.2f} €
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="decision-card-red">
                <h4 style="color:#DC2626; margin-top:0;">Demontage & Valorisation Matiere (< 20 €)</h4>
                <p style="margin-bottom:8px;"><strong>Action :</strong> Tri, demantelement et recyclage matiere.</p>
                <span style="font-size:13px; color:#475569;">
                • Extraction batterie Ni-MH et contacteurs metalliques<br>
                • Broyage des resines plastiques pour valorisation matiere<br>
                • Non viable economiquement pour remise a neuf unitaire
                </span>
            </div>
            """, unsafe_allow_html=True)

# =====================================================================================
# ONGLET 3 : STRATÉGIE CODIR & MODÈLE HYBRIDE (NOUVEL ONGLET)
# =====================================================================================
with tab3:
    st.subheader("Synthese Strategique CODIR : Une Supply Chain Hybride et Circulaire")
    st.caption("Alignement du Modele de Fisher, de l'eco-conception amont et de la gouvernance RSE (Prestataire : INGENIOUS LOGISTICS).")

    # 1. Modèle de Fisher : Décomposition de la Supply Chain Hybride
    st.markdown("#### 1. Positionnement Selon le Modele de Fisher (1997)")
    col_fish1, col_fish2 = st.columns(2)

    with col_fish1:
        st.markdown("""
        <div class="strategy-card">
            <h4 style="color:#005A9C; margin-top:0;">Flux Amont & Classique : Logique Risk-Hedging</h4>
            <p><b>Diagnostic produit (Tondeuse sans fil) :</b></p>
            <ul>
                <li><b>Demande relativement previsible :</b> 29 millions d'unites / an, best-seller standardise a 39,90 €.</li>
                <li><b>Incertitude de l'offre elevee :</b> Risque de penurie de composants electroniques, dependance a 2 usines de production (Slovaquie & Portugal).</li>
            </ul>
            <hr style="border:0; border-top:1px solid #E2E8F0;">
            <p><b>Leviers operationnels deployes :</b></p>
            <ul>
                <li>Stocks de securite cibles sur composants critiques (batteries Ni-MH, têtes de coupe).</li>
                <li>Mutualisation des ressources logistiques et SI commun avec INGENIOUS LOGISTICS.</li>
                <li>Diversification et double sourcing des sous-traitants d'injection.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_fish2:
        st.markdown("""
        <div class="strategy-card">
            <h4 style="color:#0B2545; margin-top:0;">Flux Aval & Retours : Logique Responsive / Agile</h4>
            <p><b>Diagnostic des flux inverses (Reverse Logistics) :</b></p>
            <ul>
                <li><b>Gisement annuel :</b> 1 305 000 retours / an (4,5 % des volumes vendus, soit 450 tonnes).</li>
                <li><b>Incertitude qualitative :</b> L'etat a l'arrivee exige un diagnostic reactif en temps reel.</li>
            </ul>
            <hr style="border:0; border-top:1px solid #E2E8F0;">
            <p><b>Leviers operationnels deployes :</b></p>
            <ul>
                <li>Tri et reconditionnement rapide pilote par IA et Blockchain au Hub de Hambourg.</li>
                <li>Aiguillage Buy-Back strict : reconditionnement si revente >= 20 €, sinon demontage matiere.</li>
                <li>Reinjection des pieces reutilisables pour amortir les penuries de fabrication.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. Collaboration Amont-Aval & Eco-Conception
    st.markdown("#### 2. Eco-Conception Amont & Bouclage Circulaire")
    eco1, eco2, eco3 = st.columns(3)

    with eco1:
        st.markdown("""
        <div class="financial-card">
            <h5 style="color:#005A9C; margin-top:0;">Pertes Plastiques & Methode SMED</h5>
            <p style="font-size:13px; color:#475569;">
                <b>Constat amont :</b> 51 kg de dechets plastiques pour 1 000 kg injectes (dont 7 kg finissaient en decharge).<br><br>
                <b>Solution :</b> Application de la methode SMED pour reduire les temps de reglage machine a moins de 10 min, eliminant ainsi les rebuts de demarrage de serie.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with eco2:
        st.markdown("""
        <div class="financial-card">
            <h5 style="color:#005A9C; margin-top:0;">Design for Disassembly (Clips vs Colle)</h5>
            <p style="font-size:13px; color:#475569;">
                <b>Constat :</b> Produits complexes a demonter au hub de reverse logistics.<br><br>
                <b>Action R&D :</b> Remplacement systematique de la colle par des clips d'assemblage mecaniques, facilitant le demontage sans degradation de la coque par les operateurs.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with eco3:
        st.markdown("""
        <div class="financial-card">
            <h5 style="color:#005A9C; margin-top:0;">Emballages Consignes & Reemploi</h5>
            <p style="font-size:13px; color:#475569;">
                <b>Amont :</b> Remplacement des emballages jetables fournisseurs par des bacs et conteneurs consignes standardises.<br><br>
                <b>Broyage sur site :</b> Chutes d'injection thermoplastiques directement broyees et reinjectees sur les sites de Slovaquie et du Portugal.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Volet Social, Environnemental & Partenariat INGENIOUS LOGISTICS
    st.markdown("#### 3. Infrastructures, Certifications & Inclusion Sociale")
    soc1, soc2, soc3 = st.columns(3)

    with soc1:
        st.markdown("""
        <div class="financial-card">
            <h5 style="color:#0B2545; margin-top:0;">Hub Logistique de Hambourg</h5>
            <p style="font-size:13px; color:#475569;">
                • <b>Superficie optimisee :</b> 30 000 m² (un tiers de surface en moins vs Stuttgart).<br>
                • <b>Connectivite multimodale :</b> Acces direct autoroute A7 (2,3 km), port maritime (1,7 km) et fret ferroviaire (2,5 km).<br>
                • <b>Loyer & exploitation :</b> 2,0 a 2,5 M€ / an negocies avec INGENIOUS LOGISTICS.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with soc2:
        st.markdown("""
        <div class="financial-card">
            <h5 style="color:#005A9C; margin-top:0;">Certifications ISO 14001 & ISO 50001</h5>
            <p style="font-size:13px; color:#475569;">
                • <b>ISO 14001 :</b> Gestion environnementale certifiee par organisme tiers et suivi rigoureux de la valorisation dechets.<br>
                • <b>ISO 50001 :</b> Pilotage de l'efficacite energetique et reduction de l'empreinte carbone entrepot.<br>
                • <b>Garantie clients :</b> Preuve auditable de la conformite DEEE et RoHS.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with soc3:
        st.markdown("""
        <div class="financial-card">
            <h5 style="color:#16A34A; margin-top:0;">Inclusion Sociale & Norme ISO 26000</h5>
            <p style="font-size:13px; color:#475569;">
                • <b>Emploi inclusif :</b> Integration de travailleurs RQTH (handicap) et contrats d'insertion (historiquement 0).<br>
                • <b>Handicap moteur :</b> Tables reglables en hauteur et passages elargis adaptes.<br>
                • <b>Handicap auditif :</b> Consignes de securite sur ecrans tactiles et alertes visuelles lumineuses.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =====================================================================================
# ONGLET 4 : ASSISTANT FINANCE & KPI DYNAMIQUES
# =====================================================================================
with tab4:
    st.subheader("Assistant Financier & Structure des Charges en Temps Reel")
    st.caption("Consolidation annuelle integrant les economies de fret selon le scenario selectionne a l'onglet 1.")

    volume_annuel = 29_000_000
    prix_vente_neuf = 39.90
    cout_fab_unitaire = 12.80
    ca_tondeuses = volume_annuel * prix_vente_neuf
    cout_prod_total = volume_annuel * cout_fab_unitaire
    marge_brute_prod = ca_tondeuses - cout_prod_total

    cout_logistique_initial = ca_tondeuses * 0.15
    fret_sortant_dynamique = (cout_logistique_initial * 0.31) * partenaire_actif["facteur_cout"]
    cout_logistique_ajuste = (cout_logistique_initial * 0.69) + fret_sortant_dynamique
    gain_logistique = cout_logistique_initial - cout_logistique_ajuste

    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Chiffre d'Affaires Categorie", f"{ca_tondeuses / 1e6:.1f} M€", "29M unites a 39,90 €")
    f2.metric("Cout de Fabrication Total", f"{cout_prod_total / 1e6:.1f} M€", "12,80 € / unite fabriquee")
    f3.metric(
        "Charges Logistiques Annuelles",
        f"{cout_logistique_ajuste / 1e6:.1f} M€",
        f"-{gain_logistique / 1e6:.2f} M€ ({choix_partenaire.split(' ')[0]})" if gain_logistique > 0 else "Base Inde (15% CA)",
        delta_color="normal"
    )
    f4.metric(
        "Poids Logistique / CA",
        f"{(cout_logistique_ajuste / ca_tondeuses)*100:.2f} %",
        f"Gain net : +{gain_logistique / 1e6:.2f} M€" if gain_logistique > 0 else "Reference 15%",
        delta_color="normal"
    )

    st.markdown("---")

    # =========================================================================
    # SECTION DÉTAILLÉE : INVESTISSEMENTS DE DÉPART (CAPEX) & OPEX
    # =========================================================================
    st.subheader("Detail des Investissements de Depart (CAPEX) & Frais Annuels (OPEX)")
    st.caption("Decomposition individuelle des investissements technologiques et des couts d'exploitation du depot.")

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.markdown("""
        <div class="capex-card">
            <span style="font-size:11px; text-transform:uppercase; color:#64748B; font-weight:700;">Systeme d'Information</span>
            <div style="font-size:24px; font-weight:800; color:#0B2545; margin:6px 0;">275 000 €</div>
            <p style="font-size:12px; color:#475569; margin:0;">
                <b>Investissement de base :</b> 275 k€<br>
                <b>Frais annuels :</b> 35 000 € / an
            </p>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div class="capex-card">
            <span style="font-size:11px; text-transform:uppercase; color:#64748B; font-weight:700;">Blockchain Tracabilite</span>
            <div style="font-size:24px; font-weight:800; color:#0B2545; margin:6px 0;">120 000 €</div>
            <p style="font-size:12px; color:#475569; margin:0;">
                <b>Investissement initial :</b> 120 k€<br>
                <b>Frais annuels :</b> 20 000 € / an<br>
                <i>Delai : 3 a 4 mois d'installation</i>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with d3:
        st.markdown("""
        <div class="capex-card">
            <span style="font-size:11px; text-transform:uppercase; color:#64748B; font-weight:700;">Intelligence Artificielle</span>
            <div style="font-size:24px; font-weight:800; color:#0B2545; margin:6px 0;">350 000 €</div>
            <p style="font-size:12px; color:#475569; margin:0;">
                <b>Investissement initial :</b> 350 k€<br>
                <b>Frais annuels :</b> 40 000 € / an<br>
                <i>Tri predictif & diagnostic</i>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with d4:
        st.markdown("""
        <div class="capex-card">
            <span style="font-size:11px; text-transform:uppercase; color:#64748B; font-weight:700;">Jumeaux Numeriques</span>
            <div style="font-size:24px; font-weight:800; color:#0B2545; margin:6px 0;">160 000 €</div>
            <p style="font-size:12px; color:#475569; margin:0;">
                <b>Investissement initial :</b> 160 k€<br>
                <b>Frais annuels :</b> 20 000 € / an<br>
                <i>Simulation dynamique des flux</i>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tot_col1, tot_col2 = st.columns(2)
    with tot_col1:
        st.markdown("""
        <div class="total-card-highlight">
            <span style="font-size:12px; text-transform:uppercase; letter-spacing:1.5px; color:#7CD1F9; font-weight:700;">Total Investissement de Depart (CAPEX)</span>
            <div style="font-size:38px; font-weight:800; margin:8px 0;">905 000 €</div>
            <p style="font-size:13px; color:#E2E8F0; margin:0;">
                Cumul des 4 projets technologiques :<br>
                SI (275 k€) + Blockchain (120 k€) + IA (350 k€) + Jumeaux Numeriques (160 k€).
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tot_col2:
        st.markdown("""
        <div class="financial-card" style="border-left:5px solid #005A9C;">
            <span style="font-size:12px; text-transform:uppercase; letter-spacing:1.5px; color:#64748B; font-weight:700;">Total Frais de Fonctionnement Annuels (OPEX)</span>
            <div style="font-size:38px; font-weight:800; margin:8px 0; color:#0B2545;">2 115 000 € / an</div>
            <p style="font-size:13px; color:#475569; margin:0;">
                • <b>Depot Logistique :</b> 2 000 000 € / an<br>
                • <b>Frais annuels technologies :</b> 115 000 € / an (SI: 35k, Blockchain: 20k, IA: 40k, Jumeaux: 20k).
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    donnees_invest = [
        {"Poste / Projet": "Systeme d'Information (SI)", "Investissement de base (CAPEX)": 275000, "Frais par an (OPEX)": 35000, "Commentaire / Delai": "Socle SI reverse logistics"},
        {"Poste / Projet": "Blockchain", "Investissement de base (CAPEX)": 120000, "Frais par an (OPEX)": 20000, "Commentaire / Delai": "3/4 mois d'installation"},
        {"Poste / Projet": "Intelligence Artificielle (IA)", "Investissement de base (CAPEX)": 350000, "Frais par an (OPEX)": 40000, "Commentaire / Delai": "Tri predictif et diagnostic automatique"},
        {"Poste / Projet": "Jumeaux Numeriques", "Investissement de base (CAPEX)": 160000, "Frais par an (OPEX)": 20000, "Commentaire / Delai": "Modelisation dynamique des flux"},
        {"Poste / Projet": "Depot Logistique", "Investissement de base (CAPEX)": 0, "Frais par an (OPEX)": 2000000, "Commentaire / Delai": "Frais annuels d'exploitation du depot"},
        {"Poste / Projet": "TOTAL GENERAL", "Investissement de base (CAPEX)": 905000, "Frais par an (OPEX)": 2115000, "Commentaire / Delai": "Budget initial et fonctionnement annuel"}
    ]
    df_invest = pd.DataFrame(donnees_invest)

    st.write("**Synthese detaillee des couts par projet :**")
    st.dataframe(
        df_invest.style.format({
            "Investissement de base (CAPEX)": "{:,.0f} €",
            "Frais par an (OPEX)": "{:,.0f} €"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader(f"Structure Analytique des Charges Logistiques Globales ({cout_logistique_ajuste / 1e6:.1f} M€)")
    col_chart, col_table = st.columns([1, 1])

    postes_data = [
        {"Categorie": "Logistique Transport", "Sous-poste": f"Flux sortants ({partenaire_actif['nom']})", "Montant (M€)": fret_sortant_dynamique / 1e6},
        {"Categorie": "Logistique Transport", "Sous-poste": "Flux entrants (Retours/Usines)", "Montant (M€)": cout_logistique_initial * 0.22 / 1e6},
        {"Categorie": "Stockage", "Sous-poste": "Stockage & Batiments", "Montant (M€)": cout_logistique_initial * 0.14 / 1e6},
        {"Categorie": "Stockage", "Sous-poste": "Manutention", "Montant (M€)": cout_logistique_initial * 0.10 / 1e6},
        {"Categorie": "Administratif & SI", "Sous-poste": "Systeme d'Information", "Montant (M€)": cout_logistique_initial * 0.13 / 1e6},
        {"Categorie": "Administratif & SI", "Sous-poste": "Administration generale", "Montant (M€)": cout_logistique_initial * 0.05 / 1e6},
        {"Categorie": "Administratif & SI", "Sous-poste": "Frais financiers", "Montant (M€)": cout_logistique_initial * 0.05 / 1e6}
    ]
    df_charges = pd.DataFrame(postes_data)
    total_m = df_charges["Montant (M€)"].sum()
    df_charges["Part (%)"] = (df_charges["Montant (M€)"] / total_m) * 100

    with col_chart:
        fig_donut = px.pie(
            df_charges, values="Montant (M€)", names="Sous-poste", hole=0.5,
            title="Ventilation Reajustee des Couts Logistiques (M€)",
            color_discrete_sequence=["#005A9C", "#00A3E0", "#0B2545", "#38BDF8", "#64748B", "#94A3B8", "#CBD5E1"]
        )
        fig_donut.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_table:
        st.write(f"**Postes analytiques avec relocalisation ({choix_partenaire}) :**")
        st.dataframe(
            df_charges[["Sous-poste", "Montant (M€)", "Part (%)"]].style.format({"Part (%)": "{:.1f} %", "Montant (M€)": "{:.2f} M€"}),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    st.subheader("Gains de la Filiere Reconditionnement (450 Tonnes / 1 305 000 Retours)")
    ret_col1, ret_col2 = st.columns(2)

    with ret_col1:
        st.markdown("""
        <div class="financial-card">
            <h4 style="color:#005A9C; margin-top:0;">Bilan Annee 1 (Palier 38 % Reconditionne)</h4>
            <p>• <b>Gisement de retours :</b> 1 305 000 unites (4,5 % des ventes)</p>
            <p>• <b>Unites reconditionnees :</b> 495 900 unites (38 %)</p>
            <p>• <b>Prix de revente moyen (72% neuf) :</b> 28,73 €</p>
            <p>• <b>Cout remise a neuf unitaire :</b> 5,63 €</p>
            <hr style="border: 0; border-top: 1px solid #E2E8F0;">
            <p style="font-size:16px;"><b>Chiffre d'Affaires secondaire genere :</b> 14,25 M€</p>
            <p style="font-size:16px; color:#16A34A;"><b>Marge brute additionnelle recuperee : +11,46 M€</b></p>
        </div>
        """, unsafe_allow_html=True)

    with ret_col2:
        st.markdown("""
        <div class="financial-card">
            <h4 style="color:#0B2545; margin-top:0;">Projection Cible a 3 Ans (Cible 65 %)</h4>
            <p>• <b>Gisement de retours :</b> 1 305 000 unites</p>
            <p>• <b>Unites reconditionnees :</b> 848 250 unites (65 %)</p>
            <p>• <b>Prix de revente moyen (72% neuf) :</b> 28,73 €</p>
            <p>• <b>Cout unitaire remise a neuf :</b> 5,63 €</p>
            <hr style="border: 0; border-top: 1px solid #E2E8F0;">
            <p style="font-size:16px;"><b>Chiffre d'Affaires secondaire projete :</b> 24,37 M€</p>
            <p style="font-size:16px; color:#16A34A;"><b>Marge brute additionnelle projetee : +19,59 M€</b></p>
        </div>
        """, unsafe_allow_html=True)
