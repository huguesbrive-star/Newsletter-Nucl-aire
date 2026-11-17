#!/usr/bin/env python3
import os, re, json, hashlib, argparse
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import quote_plus
import feedparser, requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
TZ=ZoneInfo("Europe/Paris")
HEADERS={"User-Agent":"ObservatoireNucleaireFrancais/1.0 (veille de presse)"}
TOPICS={
 "Parc et production EDF":"nucléaire France EDF production réacteurs centrale",
 "EPR et nouveaux réacteurs":"EPR2 France SMR nouveau réacteur nucléaire",
 "Sûreté et régulation":"sûreté nucléaire France ASNR ASN centrale",
 "Combustible et déchets":"uranium combustible nucléaire France déchets retraitement",
 "Politique énergétique":"politique énergétique France nucléaire gouvernement",
 "Industrie, investissements et emplois":"industrie nucléaire française investissements emplois"}
def clean(s):
 return re.sub(r"\\s+"," ",BeautifulSoup(s or "","html.parser").get_text(" ",strip=True)).strip()
def article_text(url):
 try:
  r=requests.get(url,headers=HEADERS,timeout=15); r.raise_for_status()
  soup=BeautifulSoup(r.text,"html.parser")
  for x in soup(["script","style","nav","footer","header","aside"]): x.decompose()
  node=soup.select_one("article") or soup.select_one("main") or soup.body
  return clean(node.get_text(" ",strip=True) if node else "")[:14000]
 except Exception: return ""
def make_summary(title,body):
 if not body: return "Le texte intégral n'est pas accessible automatiquement. Ouvrez la source originale pour consulter l'article."
 key=os.getenv("OPENAI_API_KEY")
 if key:
  try:
   from openai import OpenAI
   c=OpenAI(api_key=key)
   out=c.chat.completions.create(model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),temperature=0.2,
    messages=[{"role":"system","content":"Tu es documentaliste spécialisé dans l'énergie nucléaire française. Rédige en français un résumé détaillé fidèle de 5 à 8 phrases. Distingue faits, déclarations et opinions. N'invente rien et signale les limites du texte."},
    {"role":"user","content":"Titre : "+title+"\\nTexte accessible : "+body[:12000]}])
   return out.choices[0].message.content.strip()
  except Exception as e: print("Résumé IA indisponible:",e)
 parts=re.split(r"(?<=[.!?])\\s+",body)
 return " ".join(parts[:5])[:1300] or "Résumé non disponible."
def main():
 p=argparse.ArgumentParser(); p.add_argument("--force",action="store_true"); a=p.parse_args()
 now=datetime.now(TZ)
 if not a.force and not(now.weekday()==0 and now.hour==7):
  print("En attente du lundi à 7 h, heure de Paris."); return
 articles=[]; seen=set()
 for category,q in TOPICS.items():
  rss="https://news.google.com/rss/search?q="+quote_plus(q+" when:7d")+"&hl=fr&gl=FR&ceid=FR:fr"
  feed=feedparser.parse(rss)
  for e in feed.entries[:20]:
   title=clean(e.get("title","")); url=e.get("link","")
   if not title or not url: continue
   key=hashlib.sha256((title.lower()+url.split("?")[0]).encode()).hexdigest()
   if key in seen: continue
   seen.add(key)
   excerpt=article_text(url)
   summary=make_summary(title,excerpt or clean(e.get("summary","")))
   articles.append({"id":key[:16],"title":title,"url":url,"source":clean(e.get("source",{}).get("title","")) or "Source de presse",
    "published":e.get("published",""),"category":category,"summary":summary,"excerpt":excerpt[:500],"full_text_accessible":bool(excerpt)})
 articles.sort(key=lambda x:x["published"],reverse=True)
 edition={"title":"Revue de presse — nucléaire français","generated_at":now.isoformat(),"period":"7 derniers jours",
  "article_count":len(articles),"articles":articles,
  "methodology":"Collecte RSS Google Actualités. Résumés IA si OPENAI_API_KEY est configurée, sinon résumé extractif. Les articles et leurs droits restent ceux des éditeurs ; les liens renvoient aux sources originales."}
 out=ROOT/"editions"; (out/"historique").mkdir(parents=True,exist_ok=True)
 data=json.dumps(edition,ensure_ascii=False,indent=2)
 (out/"latest.json").write_text(data,encoding="utf-8")
 (out/"historique"/(now.strftime("%Y-%m-%d")+".json")).write_text(data,encoding="utf-8")
 print(f"Édition créée : {len(articles)} articles.")
if __name__=="__main__": main()
