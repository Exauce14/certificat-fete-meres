import streamlit as st
import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

# Configuration de la page
st.set_page_config(page_title="Certificat – Fête des Mères", page_icon="🌹", layout="centered")

# Injection du design CSS personnalisé
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Great+Vibes&family=Lato:wght@300;400;700&display=swap');

    /* Fond et Styles Généraux */
    .stApp {
        background: linear-gradient(160deg, #fff0f5 0%, #fdf6f0 50%, #fff8f0 100%);
        font-family: 'Lato', sans-serif;
    }

    .main-header {
        text-align: center;
        padding-top: 2rem;
    }

    .header-accent {
        width: 60px; height: 2px;
        background: #c2185b;
        margin: 0 auto 1.2rem;
        border-radius: 2px;
    }

    h1 {
        font-family: 'Great Vibes', cursive !important;
        font-size: 4rem !important;
        color: #c2185b !important;
        text-align: center;
        margin-bottom: 0.2rem !important;
    }

    .subtitle {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #7a6070;
        text-align: center;
        margin-bottom: 3rem;
    }

    /* Style du pied de page */
    .custom-footer {
        text-align: center;
        padding: 2.5rem 1rem;
        border-top: 1px solid rgba(194,24,91,0.12);
        margin-top: 4rem;
    }

    .footer-divider {
        display: flex; align-items: center; justify-content: center; gap: 1rem;
        margin-bottom: 1.2rem;
    }

    .line { width: 100px; height: 1px; background: rgba(194,24,91,0.2); }
    .footer-rose { color: #c2185b; font-size: 1.2rem; }

    footer {visibility: hidden;} /* Cache le footer Streamlit par défaut */
</style>

<div class="main-header">
    <div class="header-accent"></div>
    <h1>Fête des Mères</h1>
    <p class="subtitle">Communauté d'Ottawa Est · Église Néo-Apostolique</p>
</div>
""", unsafe_allow_html=True)

# Zone de saisie (Card style)
with st.container():
    nom_mere = st.text_input("NOM DE LA MÈRE", placeholder="Ex : Rachel Ngolo")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        generer_btn = st.button("✦  GÉNÉRER LE CERTIFICAT", use_container_width=True)

if generer_btn:
    if nom_mere:
        # --- LOGIQUE DE GÉNÉRATION PDF ---
        # Remarque : Utilisez ici le nom exact de votre dernier fichier PDF uploader sur GitHub
        CHEMIN_PDF = "modele.pdf" 
        CHEMIN_POLICE = "GreatVibes-Regular.ttf"

        if not os.path.exists(CHEMIN_PDF) or not os.path.exists(CHEMIN_POLICE):
            st.error("Erreur : Fichiers sources manquants sur le serveur GitHub.")
        else:
            # 1. Création du calque
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=(842, 595))
            pdfmetrics.registerFont(TTFont('MaPolice', CHEMIN_POLICE))
            
            can.setFont('MaPolice', 65)
            can.setFillColorRGB(0.1, 0.05, 0.1) # Presque noir
            
            # --- AJUSTEMENT DE L'ESPACE ---
            # On écarte légèrement les lettres pour plus de clarté
            can.setCharSpace(1.5) 
            
            # On ajoute un triple espace entre le prénom et le nom pour aérer
            # split() enlève les espaces inutiles, "   ".join() remet 3 espaces au milieu
            nom_aere = "   ".join(nom_mere.split())
            
            # Positionnement (421 = centre, 285 = légèrement remonté pour l'emblème)
            can.drawCentredString(421, 285, nom_aere)
            
            can.save()
            packet.seek(0)

            # 2. Fusion
            lecteur_modele = PdfReader(CHEMIN_PDF)
            page = lecteur_modele.pages[0]
            page.merge_page(PdfReader(packet).pages[0])

            # 3. Export
            output = BytesIO()
            ecrivain = PdfWriter()
            ecrivain.add_page(page)
            ecrivain.write(output)
            
            st.markdown("<p style='text-align:center; color:#c2185b; font-weight:bold;'>✅ Certificat prêt !</p>", unsafe_allow_html=True)
            
            st.download_button(
                label="⬇️ TÉLÉCHARGER MON CERTIFICAT (PDF)",
                data=output.getvalue(),
                file_name=f"Certificat_{nom_mere.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.warning("Veuillez entrer un nom.")

# Footer personnalisé
st.markdown("""
<div class="custom-footer">
    <div class="footer-divider">
        <div class="line"></div>
        <span class="footer-rose">✦</span>
        <div class="line"></div>
    </div>
    <p style="font-family: 'Cormorant Garamond', serif; font-size: 0.9rem; color: #7a6070;">
        © 2026 · <strong>Exaucé Ngolo</strong><br>
        Tous droits réservés · Développé avec ♡ pour la Communauté d'Ottawa Est
    </p>
</div>
""", unsafe_allow_html=True)