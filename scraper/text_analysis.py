from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

# Nigerian oil & gas regulation description (semantic anchor)
OIL_GAS_REGULATION_DESC = """
This article announces or describes a new or updated regulation, compliance 
rule, licensing requirement, guideline, or policy framework within Nigeria’s oil 
and gas industry. It includes directives from NCDMB, NUPRC, the Nigerian 
Midstream and Downstream Petroleum Regulatory Authority, or the Ministry 
of Petroleum. It covers changes in procurement rules, local content 
requirements, licensing terms, operational standards, gas utilization rules, 
safety compliance mandates, or amendments to petroleum regulations.
"""

# Sector-specific keywords
OIL_GAS_KEYWORDS = [
    "ncdmb", "nigerian content", "local content policy", "nuprc", "dpr",
    "nnpc", "pia", "mmdpra", "midstream authority", "downstream authority",
    "petroleum industry act", "federal ministry of petroleum",
    "new regulation", "policy directive", "regulatory framework",
    "procurement framework", "regulatory update", "policy change",
    "amended regulation", "licensing round", "oil block license",
    "marginal field license", "compliance requirement",
    "environmental compliance", "gas flaring regulation",
    "license renewal requirement", "nigeria first policy",
    "local capacity", "indigenous participation", "content certification"
]

KEYWORD_PATTERN = re.compile("|".join(OIL_GAS_KEYWORDS), re.IGNORECASE)

# Threshold tuning for oil & gas legal text
SEMANTIC_THRESHOLD = 0.7
KEYWORD_BOOST = 0.15


def classify_oil_gas_regulation(article_text: str):
    # 1. Embeddings
    emb_article = model.encode(article_text, convert_to_tensor=True)
    emb_label = model.encode(OIL_GAS_REGULATION_DESC, convert_to_tensor=True)

    semantic_score = float(util.cos_sim(emb_article, emb_label))

    # 2. Keyword detection
    keyword_hit = bool(KEYWORD_PATTERN.search(article_text))
    if keyword_hit:
        semantic_score += KEYWORD_BOOST

    # 3. Final decision
    is_regulatory = semantic_score >= SEMANTIC_THRESHOLD

    if is_regulatory:
        return True
    else:
        return False
    

   
