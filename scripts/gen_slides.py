import json, os, re

OUT = "melhor-vendedor"
os.makedirs(OUT, exist_ok=True)

HEAD = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>O Melhor Vendedor — Slide {num}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@200;300;400;500;600;700&family=Raleway:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&display=swap" rel="stylesheet">
<style>
:root {{
  --gold:#D9B855;--gold-light:#F2DEA0;--gold-dark:#A66617;--gold-deep:#734610;
  --gold-50:rgba(217,184,85,0.50);--gold-30:rgba(217,184,85,0.30);--gold-20:rgba(217,184,85,0.20);--gold-10:rgba(217,184,85,0.10);
  --gold-grad:linear-gradient(135deg,#F2DEA0 0%,#D9B855 30%,#A66617 65%,#734610 100%);
  --gold-grad-h:linear-gradient(90deg,#734610 0%,#A66617 15%,#D9B855 35%,#F2DEA0 50%,#D9B855 65%,#A66617 82%,#734610 100%);
  --bg:linear-gradient(160deg,#010A26 0%,#010D30 18%,#001240 40%,#011A55 65%,#021440 85%,#010A26 100%);
  --white-80:rgba(255,255,255,0.80);--white-60:rgba(255,255,255,0.60);--white-40:rgba(255,255,255,0.40);
  --font-display:"Oswald",sans-serif;--font-body:"Raleway",sans-serif;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;background:var(--bg);font-family:var(--font-body);overflow:hidden;cursor:none}}
#cur{{position:fixed;width:10px;height:10px;background:var(--gold);border-radius:50%;pointer-events:none;z-index:9999;transform:translate(-50%,-50%);mix-blend-mode:difference}}
#cur-r{{position:fixed;width:32px;height:32px;border:1px solid var(--gold-50);border-radius:50%;pointer-events:none;z-index:9998;transform:translate(-50%,-50%)}}
.slide{{width:100vw;height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:clamp(32px,6vw,80px);position:relative;overflow:hidden;text-align:center;gap:clamp(16px,2.5vh,32px)}}
.slide::before{{content:'';position:absolute;top:0;left:8vw;right:8vw;height:2px;background:var(--gold-grad-h);opacity:0.55}}
.slide::after{{content:'';position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse 65% 55% at 50% 50%,rgba(217,184,85,0.025) 0%,transparent 70%)}}
.badge{{display:inline-flex;align-items:center;gap:8px;background:rgba(217,184,85,0.08);border:1px solid rgba(217,184,85,0.3);border-radius:100px;padding:5px 16px;margin-bottom:4px}}
.badge span{{font-family:var(--font-display);font-size:clamp(8px,0.8vw,11px);letter-spacing:0.3em;text-transform:uppercase;color:var(--gold)}}
.badge-dot{{width:5px;height:5px;border-radius:50%;background:var(--gold);flex-shrink:0}}
h1{{font-family:var(--font-display);font-weight:600;font-size:clamp(32px,5.5vw,88px);background:var(--gold-grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.05;letter-spacing:-0.01em;z-index:2;animation:fadeUp 0.8s ease both}}
h2{{font-family:var(--font-display);font-weight:500;font-size:clamp(22px,3.5vw,54px);background:var(--gold-grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1;z-index:2;animation:fadeUp 0.8s ease both 0.1s}}
.sub{{font-family:var(--font-display);font-weight:200;font-size:clamp(11px,1.4vw,20px);letter-spacing:0.25em;text-transform:uppercase;color:var(--gold-50);z-index:2;animation:fadeUp 0.8s ease both 0.2s}}
.body-text{{font-family:var(--font-body);font-size:clamp(13px,1.3vw,20px);color:var(--white-60);line-height:1.7;max-width:820px;z-index:2;animation:fadeUp 0.8s ease both 0.15s}}
.body-text b,.body-text strong{{color:var(--white-80);font-weight:500}}
.highlight{{font-family:var(--font-display);font-size:clamp(18px,2.8vw,42px);font-weight:500;color:#fff;z-index:2;animation:fadeUp 0.8s ease both 0.1s;line-height:1.3}}
.big-number{{font-family:var(--font-display);font-weight:700;font-size:clamp(64px,12vw,160px);background:var(--gold-grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;z-index:2;animation:fadeUp 0.8s ease both}}
.list{{list-style:none;display:flex;flex-direction:column;gap:clamp(8px,1.2vh,16px);max-width:780px;width:100%;z-index:2;text-align:left}}
.list li{{display:flex;align-items:flex-start;gap:12px;font-family:var(--font-body);font-size:clamp(12px,1.2vw,18px);color:var(--white-60);line-height:1.5;animation:fadeUp 0.6s ease both}}
.list li::before{{content:'';width:7px;height:7px;border-radius:50%;background:var(--gold);flex-shrink:0;margin-top:6px}}
.list li b{{color:var(--white-80);font-weight:500}}
.cards{{display:flex;flex-wrap:wrap;gap:clamp(12px,1.8vw,24px);justify-content:center;z-index:2;width:100%}}
.card{{background:rgba(255,255,255,0.025);border:1px solid rgba(217,184,85,0.18);border-radius:16px;padding:clamp(16px,2vw,28px);flex:1;min-width:200px;max-width:340px;text-align:left;animation:fadeUp 0.7s ease both;position:relative;overflow:hidden}}
.card::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--gold-grad-h);opacity:0.45}}
.card-title{{font-family:var(--font-display);font-size:clamp(13px,1.3vw,18px);letter-spacing:0.05em;text-transform:uppercase;color:var(--gold-light);margin-bottom:8px}}
.card-body{{font-family:var(--font-body);font-size:clamp(11px,1vw,15px);color:var(--white-60);line-height:1.6}}
.divider{{width:60px;height:2px;background:var(--gold-grad-h);z-index:2}}
.pill-row{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;z-index:2}}
.pill{{font-family:var(--font-display);font-size:clamp(9px,0.85vw,12px);letter-spacing:0.2em;text-transform:uppercase;padding:6px 16px;border-radius:100px;border:1px solid rgba(217,184,85,0.4);color:rgba(217,184,85,0.85);background:rgba(217,184,85,0.07)}}
.shimmer-line{{position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--gold-grad-h);opacity:0.45}}
.table-wrap{{z-index:2;width:100%;max-width:800px;overflow:hidden;border-radius:16px;border:1px solid rgba(217,184,85,0.2)}}
table{{width:100%;border-collapse:collapse;font-family:var(--font-body)}}
th{{background:rgba(217,184,85,0.12);color:var(--gold-light);font-family:var(--font-display);font-size:clamp(9px,0.9vw,13px);letter-spacing:0.15em;text-transform:uppercase;padding:10px 16px;text-align:left}}
td{{padding:9px 16px;font-size:clamp(11px,1vw,14px);color:var(--white-60);border-top:1px solid rgba(255,255,255,0.05)}}
td:first-child{{color:var(--gold);font-weight:600}}
tr:hover td{{background:rgba(255,255,255,0.02)}}
.section-div{{width:100%;max-width:820px;height:1px;background:linear-gradient(90deg,transparent,rgba(217,184,85,0.3),transparent);z-index:2}}
.steps{{display:flex;flex-direction:column;gap:clamp(10px,1.5vh,18px);width:100%;max-width:720px;z-index:2}}
.step{{display:flex;align-items:flex-start;gap:16px;animation:fadeUp 0.6s ease both}}
.step-num{{font-family:var(--font-display);font-weight:700;font-size:clamp(18px,2.2vw,32px);background:var(--gold-grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;flex-shrink:0;width:36px}}
.step-text{{font-family:var(--font-body);font-size:clamp(12px,1.2vw,17px);color:var(--white-60);line-height:1.5;padding-top:4px}}
.step-text b{{color:var(--white-80);font-weight:500}}
.quote{{font-family:var(--font-body);font-style:italic;font-size:clamp(15px,1.8vw,26px);color:var(--white-80);max-width:800px;line-height:1.6;z-index:2;padding:24px 32px;border-left:3px solid var(--gold);border-right:3px solid var(--gold);background:rgba(217,184,85,0.04);border-radius:10px;animation:fadeUp 0.8s ease both 0.2s}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
</style>
</head>
<body>
<div id="cur"></div><div id="cur-r"></div>
<section class="slide">
'''

FOOT = '''  <div class="shimmer-line"></div>
</section>
<script>
const cur=document.getElementById('cur'),curR=document.getElementById('cur-r');
document.addEventListener('mousemove',e=>{{cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px';curR.style.left=e.clientX+'px';curR.style.top=e.clientY+'px';}});
</script>
</body>
</html>'''

def esc(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def lines(t):
    return [l.strip() for l in t.strip().split('\n') if l.strip()]

def badge(label):
    return f'  <div class="badge"><span class="badge-dot"></span><span>{esc(label)}</span></div>\n'

def make_slide(num, content):
    return HEAD.format(num=num) + content + FOOT.format()

# ── SLIDE DATA ──────────────────────────────────────────────────────────────

def s(num, content):
    path = os.path.join(OUT, f"slide-{num:03d}.htm")
    with open(path, "w", encoding="utf-8") as f:
        f.write(make_slide(num, content))

# 1 - Capa
s(1, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    {badge("Treinamento · Universo Corporativo")}
    <h1>O MELHOR VENDEDOR<br>DE TODOS OS TEMPOS</h1>
    <p class="sub">The Best Salesman Ever</p>
  </div>
  <div class="divider"></div>
  <div class="pill-row">
    <span class="pill">Bloco 1 · Ação na Prática</span>
    <span class="pill" style="border-color:rgba(0,200,180,0.4);color:rgba(0,200,180,0.85);background:rgba(0,200,180,0.07)">Bloco 2 · Neurociência</span>
    <span class="pill" style="border-color:rgba(160,80,220,0.4);color:rgba(160,80,220,0.85);background:rgba(160,80,220,0.07)">Bloco 3 · Estratégia</span>
  </div>
''')

# 2 - A Sua Moeda de Valor
s(2, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both;text-align:center">
    <p class="sub" style="font-size:clamp(14px,2vw,28px);letter-spacing:0.5em;line-height:2">A SUA MOEDA DE VALOR</p>
    <p class="sub" style="margin-top:16px">The Best Salesman Ever</p>
  </div>
''')

# 3 - Índice
s(3, f'''
  {badge("Estrutura do Treinamento")}
  <h2>BLOCOS DO TREINAMENTO</h2>
  <div class="cards">
    <div class="card" style="border-color:rgba(217,184,85,0.35)">
      <p class="card-title" style="font-size:clamp(10px,1vw,14px);color:var(--gold-50)">PÁG. 4</p>
      <p class="card-title">BLOCO 1</p>
      <p class="card-body">Ação na Prática</p>
    </div>
    <div class="card" style="border-color:rgba(0,200,180,0.25)" >
      <p class="card-title" style="font-size:clamp(10px,1vw,14px);color:rgba(0,200,180,0.5)">PÁG. 68</p>
      <p class="card-title" style="color:rgba(0,200,180,0.85)">BLOCO 2</p>
      <p class="card-body">Neurociência</p>
    </div>
    <div class="card" style="border-color:rgba(160,80,220,0.25)">
      <p class="card-title" style="font-size:clamp(10px,1vw,14px);color:rgba(160,80,220,0.5)">PÁG. 106</p>
      <p class="card-title" style="color:rgba(160,80,220,0.85)">BLOCO 3</p>
      <p class="card-body">Estratégia</p>
    </div>
  </div>
''')

# 4 - Bloco 1 divider
s(4, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both;text-align:center">
    <p class="sub">Bloco 1</p>
    <h1>AÇÃO NA<br>PRÁTICA</h1>
  </div>
''')

# 5 - Regra de Ouro
s(5, f'''
  {badge("Regra de Ouro")}
  <h1>VÁ E VENDA</h1>
  <div class="divider"></div>
  <p class="sub">Regra de Ouro</p>
''')

# 6 - O que o cliente ganha/perde
s(6, f'''
  {badge("A Pergunta Fundamental")}
  <div class="cards" style="max-width:900px">
    <div class="card" style="border-color:rgba(34,197,94,0.3);flex:1">
      <div style="font-size:28px;margin-bottom:10px">✅</div>
      <p class="card-title" style="color:#86efac">O que o cliente GANHA se ele comprar?</p>
    </div>
    <div class="card" style="border-color:rgba(239,68,68,0.3);flex:1">
      <div style="font-size:28px;margin-bottom:10px">❌</div>
      <p class="card-title" style="color:#fca5a5">O que o cliente PERDE se ele não comprar?</p>
    </div>
  </div>
''')

# 7 - Importância do atendimento
s(7, f'''
  {badge("Importância do Atendimento")}
  <h2>POR QUÊ SE PERDE UM CLIENTE?</h2>
  <ul class="list" style="max-width:640px">
    <li><b>65%</b> — Indiferença no atendimento</li>
    <li><b>14%</b> — Reclamações não atendidas</li>
    <li><b>10%</b> — Vantagens oferecidas pelo concorrente</li>
    <li><b>05%</b> — Amizade com o concorrente</li>
    <li><b>05%</b> — Mudança de endereço</li>
    <li><b>01%</b> — Falecimento do cliente</li>
  </ul>
''')

# 8 - 76%
s(8, f'''
  {badge("Dado Estratégico")}
  <div class="big-number">76%</div>
  <p class="highlight">Das escolhas de compra são feitas<br><b style="color:var(--gold-light)">DENTRO</b> da Construtora ou Imobiliária</p>
''')

# 9 - Lei da Venda Exponencial
s(9, f'''
  {badge("A Lei da Venda Exponencial")}
  <h2>A LEI DA VENDA EXPONENCIAL</h2>
  <div class="steps">
    <div class="step"><span class="step-num">1</span><p class="step-text"><b>Aponte um Problema</b></p></div>
    <div class="step"><span class="step-num">2</span><p class="step-text"><b>Gere Ansiedade</b></p></div>
    <div class="step"><span class="step-num">3</span><p class="step-text"><b>Apresente a Solução</b></p></div>
  </div>
''')

# 10 - Funil de Vendas (título)
s(10, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    {badge("Metodologia")}
    <h1>FUNIL DE<br>VENDAS</h1>
  </div>
''')

# 11 - Funil do vendedor comum
s(11, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    {badge("Comparativo")}
    <h2>FUNIL DE VENDAS DO<br>VENDEDOR COMUM</h2>
    <p class="body-text" style="margin-top:16px">O vendedor comum usa apenas o funil tradicional — prospecta, apresenta e aguarda. O melhor vendedor vai além, transformando o funil em ampulheta.</p>
  </div>
''')

# 12 - Ampulheta (título)
s(12, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    {badge("Metodologia Avançada")}
    <h1>AMPULHETA DO<br>MELHOR VENDEDOR<br>DE TODOS OS TEMPOS</h1>
  </div>
''')

# 13 - Ampulheta detalhada
s(13, f'''
  {badge("A Ampulheta Completa")}
  <h2>AMPULHETA DO MELHOR VENDEDOR</h2>
  <div class="cards">
    <div class="card" style="border-color:rgba(217,184,85,0.35)">
      <p class="card-title">FASE 1</p>
      <ul class="list" style="gap:6px">
        <li>Lead</li><li>Abordagem</li><li>Produto, Objeções, Oferta</li><li>Proposta</li><li>Negociação</li><li>Venda / Contrato</li>
      </ul>
    </div>
    <div class="card" style="border-color:rgba(0,200,180,0.25)">
      <p class="card-title" style="color:rgba(0,200,180,0.85)">FASE 2</p>
      <ul class="list" style="gap:6px">
        <li>Indicação</li><li>Bonificação</li><li>Escalabilidade</li><li>Receita Recorrente</li>
      </ul>
    </div>
  </div>
''')

# 14 - Vendendo na Prática (título)
s(14, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <p class="sub">Bloco 1 · Ação</p>
    <h1>VENDENDO<br>NA PRÁTICA</h1>
  </div>
''')

# 15 - (blank/visual)
s(15, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <p class="sub">Preparação</p>
    <h2>ANTES DE VENDER</h2>
    <p class="body-text" style="margin-top:16px">O sucesso na venda começa muito antes do primeiro contato com o cliente. Prepare-se com conhecimento, produto e região.</p>
  </div>
''')

# 16 - Estude
s(16, f'''
  {badge("Preparação")}
  <ul class="list" style="max-width:680px;gap:20px">
    <li style="font-size:clamp(14px,1.6vw,22px)"><b>Estude a Região.</b></li>
    <li style="font-size:clamp(14px,1.6vw,22px)"><b>Estude o Produto.</b></li>
    <li style="font-size:clamp(14px,1.6vw,22px)"><b>Conte os Diferenciais.</b></li>
    <li style="font-size:clamp(14px,1.6vw,22px)"><b>Mostre as Vantagens.</b></li>
    <li style="font-size:clamp(14px,1.6vw,22px)"><b>Dê Segurança!</b></li>
  </ul>
''')

# 17 - Não gere muita expectativa
s(17, f'''
  {badge("Mentalidade")}
  <div class="quote">NÃO GERE MUITA EXPECTATIVA COM SEU CLIENTE.<br><br>FOQUE EM SABER QUE VOCÊ DEU 100% DO SEU POTENCIAL EM CADA FRASE QUE ESCREVEU PARA O CLIENTE.</div>
''')

# 18 - Horário de atender
s(18, f'''
  {badge("Atendimento")}
  <div class="quote">NÃO EXISTE MELHOR HORÁRIO PARA ATENDER.<br><br>O HORÁRIO É QUANDO SEU CLIENTE RESPONDE E ESTÁ DISPOSTO A FALAR COM VOCÊ.</div>
''')

# 19 - Envie textos e áudios
s(19, f'''
  {badge("Comunicação")}
  <h2>ENVIE TEXTOS. ENVIE ÁUDIOS.</h2>
  <p class="highlight">Seja objetivo em ambos.</p>
  <div class="quote">"LEMBRE SEMPRE QUE A COMUNICAÇÃO É O QUE SEU CLIENTE ENTENDEU E NÃO AQUILO QUE VOCÊ COMUNICOU."</div>
''')

# 20 - Chamada de vídeo
s(20, f'''
  {badge("Atendimento Digital")}
  <h2>TENTE AGENDAR UMA CHAMADA DE VÍDEO!</h2>
  <ul class="list" style="max-width:660px">
    <li>Atenção ao <b>ambiente</b> que mostrará</li>
    <li>Atenção à sua <b>vestimenta</b></li>
    <li>Atenção ao seu <b>tom de voz</b> e sua energia</li>
    <li>Pergunte quanto <b>tempo o cliente tem disponível</b></li>
  </ul>
''')

# 21 - Estrutura da construtora
s(21, f'''
  {badge("Autoridade")}
  <h2>ENVIE FOTOS DO INTERIOR DA CONSTRUTORA.</h2>
  <p class="highlight">Mostre a estrutura que temos.</p>
  <div class="quote">ISSO TRANSMITE AUTORIDADE!!!</div>
''')

# 22 - Português na escrita
s(22, f'''
  {badge("Profissionalismo")}
  <h2>MUITA ATENÇÃO AO PORTUGUÊS NA SUA ESCRITA...</h2>
  <p class="highlight" style="max-width:680px">Revise sempre antes de enviar qualquer mensagem ao cliente.</p>
''')

# 23 - Foto de perfil
s(23, f'''
  {badge("Imagem Pessoal")}
  <h2>COMO É SUA FOTO DE PERFIL NO SEU INSTAGRAM E WHATS?</h2>
  <div class="quote">ELA É SUA VITRINE. CAPRICHE NA IMAGEM!</div>
''')

# 24 - Palavras positivas
s(24, f'''
  {badge("Linguagem de Impacto")}
  <h2>UTILIZE SEMPRE PALAVRAS POSITIVAS E EXPRESSÕES DE IMPACTO POSITIVO</h2>
  <div class="pill-row" style="max-width:800px">
    {''.join(f'<span class="pill">{w}</span>' for w in ['ÓTIMO','EXCELENTE','APROVEITE','DESCUBRA','INVISTA','VALOR','FUTURO','SEGURANÇA','VANTAGEM','LUCRATIVIDADE','RENTABILIDADE','PATRIMÔNIO','FAMÍLIA','RESERVA FUTURA'])}
  </div>
''')

# 25 - Chame pelo nome
s(25, f'''
  {badge("Técnica de Conexão")}
  <h2>CHAME O CLIENTE PELO NOME!</h2>
  <ul class="list" style="max-width:640px">
    <li>Vai escrever algo importante durante a negociação? <b>Chame ele pelo nome.</b></li>
    <li>Vai dar algum comando? <b>Chame ele pelo nome.</b></li>
  </ul>
''')

# 26 - Seja breve
s(26, f'''
  {badge("Velocidade na Venda")}
  <h2>SEJA BREVE, FOQUE EM RESPONDER EM POUCOS SEGUNDOS.</h2>
  <div class="quote">A VENDA É MOMENTO!<br>APROVEITE E ACELERE!</div>
''')

# 27 - Saudação inicial
s(27, f'''
  {badge("Script de Abordagem")}
  <h2>SAUDAÇÃO INICIAL</h2>
  <div class="quote">"Olá, sou Patrick Piccoli, especialista em investimento imobiliário em Porto Belo, da Tonolher Empreendimentos. Tudo bem [nome do cliente]?"<br><br><span style="font-size:0.85em;color:var(--gold-50)">Envie a imagem da campanha em que seu cliente clicou.</span></div>
''')

# 28 - Segunda abordagem
s(28, f'''
  {badge("Script de Abordagem")}
  <h2>SEGUNDA ABORDAGEM</h2>
  <div class="quote" style="font-size:clamp(12px,1.3vw,18px)">"Você demonstrou interesse em um dos nossos empreendimentos e vou dar início em seu atendimento.<br><br>Sua procura é para moradia ou investimento? O foco dos nossos produtos é para quem busca aquele investimento certeiro. Os stúdios hoje são uma moeda forte e cada vez mais procurados."</div>
''')

# 29 - Aguarde o cliente
s(29, f'''
  {badge("Técnica de Escuta")}
  <h1>AGUARDE O CLIENTE<br>SE MANIFESTAR</h1>
  <p class="body-text">Após a segunda abordagem, dê espaço. O silêncio estratégico é uma ferramenta poderosa de vendas.</p>
''')

# 30 - Já envie materiais
s(30, f'''
  {badge("Materiais de Apoio")}
  <h2>JÁ ENVIE AO CLIENTE:</h2>
  <ul class="list" style="max-width:600px;gap:20px">
    <li><b>App Institucional Construtora</b></li>
    <li><b>App Master Plan</b></li>
    <li><b>E-book do Empreendimento</b></li>
  </ul>
''')

# 31 - Tenha pronto
s(31, f'''
  {badge("Preparação")}
  <h2>JÁ TENHA PRONTO:</h2>
  <ul class="list" style="max-width:620px;gap:20px">
    <li><b>A Chave PIX de Reserva</b> dos Empreendimentos</li>
    <li><b>Formulário de Reserva</b></li>
  </ul>
''')

# 32 - Objeções gerais
s(32, f'''
  {badge("Contornando Objeções")}
  <h2>CONTORNANDO OBJEÇÕES</h2>
  <ul class="list" style="max-width:780px">
    <li>ACIP – junção do poder público com o privado</li>
    <li>Masterplan 2022–2032: a cidade de Porto Belo está sendo preparada</li>
    <li>Acordo das maiores construtoras para entregar os maiores projetos a partir de 2030</li>
    <li>Valorização média de <b>20 a 25% ao ano</b></li>
    <li>O cliente poderá revender a unidade <b>12 meses</b> após a assinatura do contrato</li>
  </ul>
''')

# 33 - Área demográfica
s(33, f'''
  {badge("Dados da Região")}
  <h2>ÁREA DEMOGRÁFICA</h2>
  <div class="cards">
    <div class="card">
      <p class="card-title">Balneário Camboriú</p>
      <p class="card-body">Pop. 2024: <b>148.758</b><br>Densidade: 3.077,70 hab/km²<br>Área: 58,210 km²</p>
    </div>
    <div class="card">
      <p class="card-title">Itapema</p>
      <p class="card-body">Pop. 2022: <b>75.940</b><br>Densidade: 1.304,59 hab/km²<br>Área: 45.214 km²</p>
    </div>
    <div class="card">
      <p class="card-title">Porto Belo</p>
      <p class="card-body">Pop. 2024: <b>30.590</b><br>Densidade: 295,58 hab/km²<br>Área: 93,673 km²</p>
    </div>
  </div>
''')

# 34 - Transbordo
s(34, f'''
  {badge("Expansão Regional")}
  <h2>TRANSBORDO</h2>
  <div class="cards">
    <div class="card"><p class="card-title">Balneário Camboriú</p><p class="card-body">58.210 km²</p></div>
    <div class="card"><p class="card-title">Itapema</p><p class="card-body">45.214 km²</p></div>
    <div class="card"><p class="card-title">Porto Belo</p><p class="card-body">93.673 km²</p></div>
  </div>
  <p class="body-text">O crescimento de BC e Itapema transborda naturalmente para Porto Belo — a próxima grande oportunidade.</p>
''')

# 35 - Master Plan
s(35, f'''
  {badge("Objeção: Prazo de Entrega")}
  <h2>MASTER PLAN · 10 ANOS</h2>
  <div class="cards">
    <div class="card"><p class="card-title">ACIP 2022–2032</p><p class="card-body">Preparar Porto Belo para receber os maiores projetos após 2030</p></div>
    <div class="card"><p class="card-title">A cidade ainda não está pronta</p><p class="card-body">O Porto Lagoon, Tonolher e os maiores projetos chegam após 2030</p></div>
  </div>
''')

# 36 - Construtora sem entrega
s(36, f'''
  {badge("Contornando Objeções")}
  <h2>CONSTRUTORA NÃO POSSUI OBRAS ENTREGUES NA REGIÃO</h2>
  <ul class="list" style="max-width:780px">
    <li>Somos uma construtora com <b>45 anos de história</b> no RS</li>
    <li>Construímos para <b>Panvel, Burger King, MadeiraMadeira e Loja Simons</b></li>
    <li>As maiores e melhores construtoras do Brasil estão vindo para Porto Belo e também <b>não possuem nada entregue na região</b></li>
    <li>Reforce a participação como membro na <b>ACIP</b></li>
  </ul>
''')

# 37 - Pré-pré-lançamento
s(37, f'''
  {badge("Objeção: Registro de Incorporação")}
  <h2>PRÉ-PRÉ-LANÇAMENTO</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">"Estamos em uma fase de pré-pré-lançamento, direcionada apenas para investidores que já fazem negócio com a construtora. O melhor momento para comprar um imóvel é quando ainda não saiu o registro de incorporação."</div>
''')

# 38 - Registro de incorporação 2
s(38, f'''
  {badge("Objeção: Registro de Incorporação")}
  <h2>ESTEJA PRONTO PARA INVESTIR</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">"Se você quiser comprar quando sair o Registro de Incorporação, você pagará o dobro do valor e certamente não teremos mais nenhuma unidade disponível."</div>
  <p class="body-text">A FG entrou com uma liminar em 2008 que permitiu o contrato de reserva de unidade. Quando sair o RI, será feito um aditivo tornando-o contrato de compra e venda.</p>
''')

# 39 - Distância do mar
s(39, f'''
  {badge("Objeção: Distância do Mar")}
  <h2>DISTÂNCIA É LONGE DO MAR?</h2>
  <ul class="list" style="max-width:760px">
    <li>Quem frequenta a região vai de carro para a praia — há várias praias paradisíacas</li>
    <li>O Master Plan de Porto Belo <b>limita as metragens</b> dentro de Balneário Perequê</li>
    <li>Os stúdios ficam mais distantes por razão de <b>fluxo de mobilidade de pessoas e veículos</b></li>
  </ul>
''')

# 40 - Muitos pré-lançamentos
s(40, f'''
  {badge("Objeção: Muitos Pré-lançamentos")}
  <h2>CONSTRUTORA TEM MUITOS PRÉ-LANÇAMENTOS?</h2>
  <div class="quote">"Nosso projeto de expansão é construir nos próximos 45 anos na região da Costa Esmeralda. Ainda teremos projetos em Barra Velha, Camboriú, Penha, entre outras praias. Somos fortes e seremos cada vez mais."</div>
''')

# 41 - Pontos-chave 1
s(41, f'''
  {badge("Nossos Diferenciais")}
  <h2>NOSSOS PONTOS CHAVE</h2>
  <ul class="list" style="max-width:720px">
    <li>Produtos <b>disruptivos</b> que se destacam no mercado</li>
    <li>Valorização <b>acima do mercado</b></li>
    <li>Forma <b>facilitada</b> de pagamento</li>
    <li>Vendas aceleradas</li>
    <li>Alta procura de clientes</li>
    <li>Nossos lançamentos vendem em sua totalidade <b>em 30 a 45 dias</b></li>
  </ul>
''')

# 42 - Pontos-chave 2
s(42, f'''
  {badge("Nossos Diferenciais")}
  <h2>NOSSOS PONTOS CHAVE</h2>
  <div class="card" style="max-width:700px;width:100%">
    <p class="card-title">Correção apenas pelo CUB</p>
    <p class="card-body" style="font-size:clamp(13px,1.2vw,18px);line-height:1.7">Correção apenas do CUB durante toda a vigência do contrato. O CUB é o <b>menor indexador do mercado</b> — média de 3 a 4% ao ano nos últimos 5 anos em Santa Catarina.</p>
  </div>
''')

# 43 - Envie a proposta
s(43, f'''
  {badge("Enviando a Proposta")}
  <h2>ENVIE A PROPOSTA</h2>
  <ul class="list" style="max-width:720px">
    <li>Faça cálculos</li>
    <li>Perceba o cliente</li>
    <li>Crie <b>mais de uma possibilidade</b></li>
    <li>Capriche — cada detalhe importa: escreva com caneta grossa na cor vermelha e envie imagem + vídeo explicando os detalhes</li>
    <li>Ou você pode digitar e enviar ao cliente</li>
  </ul>
''')

# 44 - Devo enviar a tabela?
s(44, f'''
  {badge("Estratégia de Proposta")}
  <h2>DEVO ENVIAR A TABELA?</h2>
  <div class="cards">
    <div class="card" style="border-color:rgba(34,197,94,0.3)">
      <p class="card-title" style="color:#86efac;font-size:clamp(20px,3vw,40px)">SIM</p>
      <p class="card-body">Caso existam <b>poucas unidades disponíveis</b></p>
    </div>
    <div class="card" style="border-color:rgba(239,68,68,0.3)">
      <p class="card-title" style="color:#fca5a5;font-size:clamp(20px,3vw,40px)">NÃO</p>
      <p class="card-body">Caso existam <b>muitas unidades disponíveis</b></p>
    </div>
  </div>
''')

# 45 - Valor do m²
s(45, f'''
  {badge("Argumento de Valor")}
  <h2>VALOR DO M²</h2>
  <div class="quote">CALCULE:<br><b>VALOR DA UNIDADE ÷ METRAGEM = VALOR DO M²</b><br><br>Compare o M² de Porto Belo versus o M² que o cliente está pagando agora.</div>
''')

# 46 - Valor do investimento
s(46, f'''
  {badge("Apresentando a Proposta")}
  <h2>VALOR DO INVESTIMENTO</h2>
  <div class="card" style="max-width:720px;width:100%;text-align:left">
    <p class="card-title">Exemplo: R$ 300.000</p>
    <ul class="list" style="gap:8px;margin-top:12px">
      <li>Sinal: <b>R$ 1.000</b></li>
      <li>Entrada: <b>R$ 5.000</b></li>
      <li><b>160x de R$ 1.837,50</b></li>
      <li>Entrega em <b>2032</b></li>
    </ul>
  </div>
  <div class="quote" style="font-size:clamp(12px,1.1vw,16px)">O cliente pagará até a entrega apenas <b>60% do valor total</b>. Após as chaves, o próprio aluguel paga o saldo devedor — além da valorização ter multiplicado <b>3x</b> até a entrega!</div>
''')

# 47 - Lucros futuros
s(47, f'''
  {badge("Projeção de Lucros")}
  <h2>VALOR DOS LUCROS FUTUROS</h2>
  <div class="big-number" style="font-size:clamp(40px,7vw,100px)">R$ 80–100 MIL</div>
  <p class="highlight">Por temporada com a locação de um stúdio</p>
  <p class="body-text">O cliente recupera o investimento total em <b>apenas 3 anos</b>, fora a valorização ao longo da obra.</p>
''')

# 48 - Planta das unidades
s(48, f'''
  {badge("Direcionamento")}
  <h2>NESTE MOMENTO:</h2>
  <ul class="list" style="max-width:700px;gap:20px">
    <li>Faça um <b>print da planta das unidades</b> e envie ao cliente</li>
    <li>Já <b>sugira uma unidade</b> e argumente sobre a posição solar, vista, entre outros...</li>
  </ul>
''')

# 49 - Você direciona
s(49, f'''
  {badge("Controle da Venda")}
  <h1>VOCÊ PRECISA<br>DIRECIONAR</h1>
  <div class="quote">QUEM CONTROLA A VENDA É VOCÊ!</div>
''')

# 50 - Prova social
s(50, f'''
  {badge("Prova Social")}
  <h2>MOSTRE PROVAS SOCIAIS DE GANHOS PASSADOS E FUTUROS</h2>
  <ul class="list" style="max-width:720px">
    <li>Apresente a <b>projeção de valorização</b></li>
    <li>Apresente o valor a ser pago pelo cliente <b>por ano</b></li>
    <li>Ele nunca vai comprar um imóvel com as nossas condições de pagamento de outra forma</li>
  </ul>
''')

# 51 - Crescimento Porto Belo
s(51, f'''
  {badge("Estatística de Ganhos")}
  <h2>CRESCIMENTO DE PORTO BELO 2020–2024</h2>
  <p class="body-text" style="max-width:800px">Entre 2020 e 2024, o mercado imobiliário de Porto Belo, SC, experimentou um crescimento significativo. Em 2020, o valor médio do metro quadrado era de <b>R$ 8.066,28</b>. Em janeiro de 2024, esse valor atingiu <b>R$ 16.110,00</b>, representando um aumento de aproximadamente <b>100% no período</b>.</p>
''')

# 52 - Tabela estatística
s(52, f'''
  {badge("Tabela de Ganhos")}
  <h2>TABELA — ESTATÍSTICA DE GANHOS</h2>
  <div class="table-wrap">
    <table>
      <tr><th>Ano</th><th>Valor Médio do M² (R$)</th><th>Crescimento Anual</th></tr>
      <tr><td>2020</td><td>8.066,28</td><td>7,55%</td></tr>
      <tr><td>2021</td><td>9.120,00</td><td>13,07%</td></tr>
      <tr><td>2022</td><td>10.500,00</td><td>15,14%</td></tr>
      <tr><td>2023</td><td>13.000,00</td><td>23,81%</td></tr>
      <tr><td>2024</td><td>16.110,00</td><td>23,92%</td></tr>
    </table>
  </div>
''')

# 53 - Gráfico ganhos (visual)
s(53, f'''
  {badge("Gráfico de Ganhos")}
  <h2>GRÁFICO — ESTATÍSTICA DE GANHOS</h2>
  <div class="table-wrap">
    <table>
      <tr><th>Ano</th><th>Valor Investimento de R$ 350.000</th></tr>
      <tr><td>2020</td><td>R$ 350.000</td></tr>
      <tr><td>2021</td><td>R$ 395.745 <span style="color:#86efac">(+7,55%)</span></td></tr>
      <tr><td>2022</td><td>R$ 455.661 <span style="color:#86efac">(+13,07%)</span></td></tr>
      <tr><td>2023</td><td>R$ 564.154 <span style="color:#86efac">(+15,14%)</span></td></tr>
      <tr><td>2024</td><td>R$ 699.099 <span style="color:#86efac">(+23,81%)</span></td></tr>
    </table>
  </div>
''')

# 54 - Projeção futura
s(54, f'''
  {badge("Projeção de Ganhos")}
  <h2>GRÁFICO — PROJEÇÃO DE GANHOS</h2>
  <div class="table-wrap">
    <table>
      <tr><th>Ano</th><th>Projeção (+18% a.a.)</th></tr>
      <tr><td>2025</td><td>R$ 300.000</td></tr>
      <tr><td>2026</td><td>R$ 354.000</td></tr>
      <tr><td>2027</td><td>R$ 417.720</td></tr>
      <tr><td>2028</td><td>R$ 492.910</td></tr>
      <tr><td>2029</td><td>R$ 581.633</td></tr>
      <tr><td>2030</td><td>R$ 686.327</td></tr>
      <tr><td>2031/32</td><td>R$ 809.466+</td></tr>
    </table>
  </div>
''')

# 55 - Informe como ele compra
s(55, f'''
  {badge("Fechamento")}
  <h2>INFORME COMO ELE COMPRA</h2>
  <ul class="list" style="max-width:720px">
    <li>Solicite o <b>pix de reserva</b> da unidade para garantir o valor negociado e a unidade desejada</li>
    <li>Envie os dados que ele precisa preencher</li>
    <li>Solicite <b>comprovante do pix, cópia CNH, comprovante de endereço</b> e certidão de casamento (se casado)</li>
  </ul>
''')

# 56 - Impulsionadores humanos
s(56, f'''
  {badge("Psicologia de Vendas")}
  <h2>IMPULSIONADORES HUMANOS</h2>
  <div class="cards">
    <div class="card" style="border-color:rgba(239,68,68,0.35);text-align:center">
      <p class="card-title" style="color:#fca5a5;font-size:clamp(22px,3vw,42px)">MEDO</p>
    </div>
    <div class="card" style="border-color:rgba(217,184,85,0.35);text-align:center">
      <p class="card-title" style="font-size:clamp(22px,3vw,42px)">DESEJO</p>
    </div>
  </div>
  <p class="body-text">Gere medo ou desejo para fechar sua venda e receber o sinal de reserva. <b>Trabalhe a escassez.</b></p>
''')

# 57 - Transmita segurança
s(57, f'''
  {badge("Autoridade e Confiança")}
  <h1>TRANSMITA SEGURANÇA<br>E AUTORIDADE</h1>
  <div class="quote">"COMPRE, PODE CONFIAR EM MIM!"</div>
''')

# 58 - Portfólio de empreendimentos
s(58, f'''
  {badge("Portfólio Tonolher")}
  <h2>EMPREENDIMENTOS</h2>
  <div class="cards">
    <div class="card"><p class="card-title">Sky View Tower</p><p class="card-body">O único com 2 mirantes da América Latina</p></div>
    <div class="card"><p class="card-title">Sky Marine Towers</p><p class="card-body">Resort residencial — 2 torres de 31 andares</p></div>
    <div class="card"><p class="card-title">Sky Green Tower</p><p class="card-body">Resort Residencial de alto padrão com Rooftop</p></div>
    <div class="card"><p class="card-title">Miguel Residence</p><p class="card-body">Alto padrão — fachada em película de vidro bronze</p></div>
    <div class="card"><p class="card-title">Sky Marine Tower II</p><p class="card-body">Luxo no litoral catarinense</p></div>
    <div class="card"><p class="card-title">Sky Marine Shopping</p><p class="card-body">Moradia, Office e Shopping Mall</p></div>
  </div>
''')

# 59 - SKY VIEW TOWER tipologia
s(59, f'''
  {badge("Sky View Tower — Tipologias")}
  <h2>SKY VIEW TOWER</h2>
  <div class="cards">
    <div class="card"><p class="card-title">Cobertura 01</p><p class="card-body">4 suítes · 192,83m²</p></div>
    <div class="card"><p class="card-title">Tipo 01</p><p class="card-body">3 suítes · 110,33m²</p></div>
    <div class="card"><p class="card-title">Tipo 02</p><p class="card-body">2 suítes · 82,67m²</p></div>
    <div class="card"><p class="card-title">Tipo 03</p><p class="card-body">2 suítes · 81,30m²</p></div>
    <div class="card"><p class="card-title">Tipo 04</p><p class="card-body">2 suítes · 80,79m²</p></div>
  </div>
  <p class="body-text">Sinal: R$ 1.000 · Entrada 10% · Saldo 120x · 8 Balões Anuais · Chaves 10%</p>
''')

# 60 - Sky View Tower descritivo
s(60, f'''
  {badge("Sky View Tower")}
  <h2>SKY VIEW TOWER</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Empreendimento de alto padrão elaborado com o propósito de mostrar outra perspectiva de lar, criando um novo conceito: <b>Resort Residencial</b>.<br><br>31 pavimentos com dois mirantes a mais de 106 metros de altura, proporcionando uma perspectiva única de vista.</div>
''')

# 61 - Sky Marine Towers
s(61, f'''
  {badge("Sky Marine Towers")}
  <h2>SKY MARINE TOWERS</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Empreendimento de alto padrão que redefine o conceito de moradia, oferecendo um estilo de vida de resort residencial. Duas torres de 31 andares com vista espetacular da cidade de Porto Belo e Itapema.</div>
''')

# 62 - Sky Green Tower
s(62, f'''
  {badge("Sky Green Tower")}
  <h2>SKY GREEN TOWER</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Resort Residencial de alto padrão com 31 pavimentos, Rooftop e lazer completo. Uma nova perspectiva de lar.</div>
  <div class="card" style="max-width:600px;width:100%">
    <p class="card-title">Fluxo de Pagamentos</p>
    <p class="card-body">Sinal: R$ 1.000 · Entrada R$ 5.000 ou 8%<br>Saldo em 160x · 8 Balões Anuais<br>Início de Obra: 2º Semestre 2027</p>
  </div>
''')

# 63 - Sky Marine Tower II
s(63, f'''
  {badge("Sky Marine Tower II")}
  <h2>SKY MARINE TOWER II</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Empreendimento de alto padrão que redefine o conceito de moradia de luxo no litoral catarinense. Design moderno e elegante com fachada revestida em película de vidro bronze, proporcionando visual contemporâneo e sofisticado.</div>
''')

# 64 - Sky Marine Shopping
s(64, f'''
  {badge("Sky Marine Shopping")}
  <h2>SKY MARINE SHOPPING</h2>
  <p class="highlight">Moradia, Office e Shopping Mall</p>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Empreendimento inovador onde moradia, lazer e negócios convivem em perfeita harmonia.</div>
  <div class="card" style="max-width:600px;width:100%">
    <p class="card-title">Fluxo de Pagamentos</p>
    <p class="card-body">Sinal: R$ 1.000 · Entrada R$ 10.000<br>Saldo parcelado</p>
  </div>
''')

# 65 - Vendeu? Ofereça comissão
s(65, f'''
  {badge("Pós-Venda")}
  <h1>VENDEU?<br>PARABÉNS!</h1>
  <div class="quote">AGORA OFEREÇA <b>1% DE COMISSÃO</b> AO SEU CLIENTE PARA TODAS AS INDICAÇÕES DELE QUE FECHAREM VENDAS COM VOCÊ.</div>
''')

# 66 - Cliente disse não
s(66, f'''
  {badge("Resiliência")}
  <h2>CLIENTE DISSE NÃO?</h2>
  <div class="quote">ISSO NÃO SIGNIFICA QUE ELE NÃO VAI COMPRAR.<br><br>MUDE SEUS ARGUMENTOS, CHAME ELE NOVAMENTE DENTRO DE <b>2 DIAS</b> E VOCÊ TERÁ MAIS UMA CHANCE.</div>
''')

# 67 - Cliente parou de responder
s(67, f'''
  {badge("Gestão do Pipeline")}
  <h2>CLIENTE PAROU DE RESPONDER?</h2>
  <div class="quote">TENTE CHAMAR A ATENÇÃO DELE DE OUTRA FORMA E CASO NÃO CONSIGA, FOQUE EM PROCURAR OUTRO CLIENTE.<br><br>NÃO GASTE ENERGIA AQUI.</div>
''')

# 68 - Bloco 2 divider
s(68, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both;text-align:center">
    <p class="sub">Bloco 2</p>
    <h1>NEUROCIÊNCIA</h1>
  </div>
''')

# 69 - Conheça a si mesmo (título)
s(69, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <h1>CONHEÇA A<br>SI MESMO</h1>
  </div>
''')

# 70 - Neurociência def
s(70, f'''
  {badge("Neurociência")}
  <h2>CONHEÇA A SI MESMO</h2>
  <div class="card" style="max-width:720px;width:100%">
    <p class="card-title">Neurociência</p>
    <p class="card-body" style="font-size:clamp(13px,1.3vw,19px);line-height:1.7">É o estudo científico do sistema nervoso. Sua tarefa é descobrir padrões. Seu cérebro determina como você age, reage e decide.</p>
  </div>
''')

# 71 - Conheça...
s(71, f'''
  {badge("Autoconhecimento")}
  <h2>CONHEÇA A SI MESMO</h2>
  <div class="cards">
    <div class="card">
      <p class="card-title">Desenvolva</p>
      <ul class="list" style="gap:6px">
        <li>Saiba seus hábitos, qualidades e habilidades</li>
        <li>Desenvolva o que tem de melhor</li>
        <li>Aprenda coisas novas todos os dias</li>
      </ul>
    </div>
    <div class="card">
      <p class="card-title">Evite</p>
      <ul class="list" style="gap:6px">
        <li>A perigosa Zona de Conforto</li>
        <li>O Piloto Automático</li>
      </ul>
    </div>
    <div class="card">
      <p class="card-title">Cultive</p>
      <ul class="list" style="gap:6px">
        <li>Encantamento humanizado</li>
        <li>Geração de experiência</li>
        <li>Mudança de Cultura</li>
      </ul>
    </div>
  </div>
''')

# 72 - Jeito de ser
s(72, f'''
  {badge("Presença")}
  <h2>SEU JEITO DE SER</h2>
  <div class="cards">
    <div class="card" style="text-align:center"><p class="card-title">Ótimo dia</p></div>
    <div class="card" style="text-align:center"><p class="card-title">Ótima tarde</p></div>
    <div class="card" style="text-align:center"><p class="card-title">Ótima noite</p></div>
  </div>
  <p class="body-text">Seja sempre positivo. Seu jeito de ser impacta diretamente na percepção do cliente.</p>
''')

# 73 - Seus pilares (título)
s(73, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <h1>SEUS<br>PILARES</h1>
  </div>
''')

# 74 - Pilares
s(74, f'''
  {badge("Pilares de Alta Performance")}
  <h2>SEUS PILARES</h2>
  <div class="pill-row" style="gap:16px">
    {''.join(f'<span class="pill" style="font-size:clamp(10px,1vw,14px);padding:10px 22px">{p}</span>' for p in ['EXPERIÊNCIA','EXCELÊNCIA','EXCLUSIVIDADE','ENCANTAMENTO','PERFORMANCE'])}
  </div>
''')

# 75 - Controle emocional (título)
s(75, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <h1>CONTROLE<br>EMOCIONAL</h1>
  </div>
''')

# 76 - Agilidade emocional
s(76, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <h1>AGILIDADE<br>EMOCIONAL</h1>
  </div>
''')

# 77 - Urgência
s(77, f'''
  {badge("Neurociência da Urgência")}
  <h2>A IMPORTÂNCIA DO SENSO DE URGÊNCIA</h2>
  <div class="quote">DESTRAVE SEU CÉREBRO.<br><br>Senso de <b>AGORA</b> gera escassez.</div>
''')

# 78 - Cérebro trino (título)
s(78, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <h1>O CÉREBRO<br>TRINO</h1>
  </div>
''')

# 79 - Cérebro trino detalhado
s(79, f'''
  {badge("Neurociência")}
  <h2>O CÉREBRO TRINO</h2>
  <div class="cards">
    <div class="card" style="border-color:rgba(239,68,68,0.3)">
      <p class="card-title" style="color:#fca5a5">Reptiliano (Réptil)</p>
      <p class="card-body">Cérebro instintivo — credibilidade, sobrevivência</p>
    </div>
    <div class="card" style="border-color:rgba(160,80,220,0.3)">
      <p class="card-title" style="color:rgba(160,80,220,0.85)">Sistema Límbico (Mamífero)</p>
      <p class="card-body">Cérebro emocional — emoções, sentimentos</p>
    </div>
    <div class="card" style="border-color:rgba(0,200,180,0.3)">
      <p class="card-title" style="color:rgba(0,200,180,0.85)">Neocórtex (Humano)</p>
      <p class="card-body">Cérebro racional — lógica, raciocínio</p>
    </div>
  </div>
''')

# 80 - Cérebro trino visual
s(80, f'''
  {badge("Neurociência")}
  <h1>O CÉREBRO<br>TRINO</h1>
  <p class="body-text" style="max-width:700px">Toda decisão de compra passa pelos três cérebros. O vendedor que domina essa sequência vende mais: primeiro gera <b>credibilidade</b> (reptiliano), depois desperta <b>emoção</b> (límbico), por fim apresenta a <b>lógica</b> (neocórtex).</p>
''')

# 81 - Conheça o cliente
s(81, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <h1>CONHEÇA O<br>SEU CLIENTE</h1>
  </div>
''')

# 82 - Evolução das gerações (título)
s(82, f'''
  {badge("Perfil do Cliente")}
  <h2>A EVOLUÇÃO DAS GERAÇÕES</h2>
''')

# 83 - Gerações
s(83, f'''
  {badge("Perfil do Cliente")}
  <h2>A EVOLUÇÃO DAS GERAÇÕES</h2>
  <div class="pill-row" style="gap:12px">
    <span class="pill">Baby Boomers 1946–1964</span>
    <span class="pill">Geração X · 1960–1980</span>
    <span class="pill">Geração Y · 1980–2000</span>
    <span class="pill">Geração Z · 1990–2010</span>
    <span class="pill">Alpha · 2010+</span>
    <span class="pill">Beta · 2025+</span>
  </div>
  <p class="body-text">O que ainda não mudou? A necessidade de <b>segurança, pertencimento e status</b>.</p>
''')

# 84 - O cérebro
s(84, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <h1>O<br>CÉREBRO</h1>
  </div>
''')

# 85 - Lei do cérebro
s(85, f'''
  {badge("A Lei do Cérebro")}
  <h2>A LEI DO CÉREBRO</h2>
  <div class="cards">
    <div class="card" style="text-align:center">
      <p class="big-number" style="font-size:clamp(48px,8vw,100px)">3</p>
      <p class="card-title">Segundos</p>
      <p class="card-body">Tempo para o cérebro fazer a primeira impressão</p>
    </div>
    <div class="card" style="text-align:center">
      <p class="big-number" style="font-size:clamp(36px,6vw,80px)">&lt; 1 min</p>
      <p class="card-title">Medo ou Desejo</p>
      <p class="card-body">Tempo para gerar o impulso de compra</p>
    </div>
  </div>
''')

# 86 e 87 - Lei do cérebro (visual pages)
for n in [86, 87]:
    s(n, f'''
  {badge("A Lei do Cérebro")}
  <h2>A LEI DO CÉREBRO</h2>
  <p class="body-text" style="max-width:720px">O cérebro toma decisões de forma automática e instantânea. Em <b>3 segundos</b>, ele forma a primeira impressão. Em <b>menos de 1 minuto</b>, ele decide entre medo ou desejo — e isso determina a compra.</p>
''')

# 88 - Homem das cavernas
s(88, f'''
  {badge("Neurociência")}
  <h2>HOJE TOMAMOS AS MESMAS DECISÕES<br>DO HOMEM DAS CAVERNAS</h2>
  <p class="body-text" style="max-width:720px">O cérebro humano permanece inalterado há milhares de anos. As decisões de compra são guiadas por <b>impulso</b> — medo ou desejo — assim como nossos ancestrais decidiam sobre sobrevivência.</p>
''')

# 89 - Perfil do público (título)
s(89, f'''
  {badge("Segmentação")}
  <h2>PERFIL DO PÚBLICO<br>ATENDIDO</h2>
''')

# 90 - Perfil público detalhado
s(90, f'''
  {badge("Perfil do Público Atendido")}
  <h2>PERFIL DO PÚBLICO ATENDIDO</h2>
  <div class="cards">
    <div class="card">
      <p class="card-title">Por Geração</p>
      <p class="card-body">Baby Boomer · Geração X · Geração Y · Geração Z</p>
    </div>
    <div class="card">
      <p class="card-title">Por Perfil</p>
      <p class="card-body">Adultos · Adolescentes · Crianças · Mulheres · Homens</p>
    </div>
    <div class="card">
      <p class="card-title">Por Origem</p>
      <p class="card-body">De qual cidade · Delivery · Salão · Retirada · Balcão</p>
    </div>
  </div>
  <p class="body-text">Cada geração exige um atendimento diferente. <b>Conheça quem está na sua frente.</b></p>
''')

# 91 - Impulsionadores (título)
s(91, f'''
  {badge("Psicologia")}
  <h2>OS ÚNICOS IMPULSIONADORES<br>HUMANOS</h2>
''')

# 92 - Medo ou Desejo
s(92, f'''
  {badge("Os Únicos Impulsionadores Humanos")}
  <div class="cards" style="gap:40px">
    <div class="card" style="border-color:rgba(239,68,68,0.35);text-align:center;padding:clamp(24px,4vw,48px)">
      <div style="font-size:clamp(40px,7vw,80px);margin-bottom:12px">😨</div>
      <p class="card-title" style="color:#fca5a5;font-size:clamp(22px,3.5vw,48px)">MEDO</p>
    </div>
    <div class="card" style="border-color:rgba(217,184,85,0.35);text-align:center;padding:clamp(24px,4vw,48px)">
      <div style="font-size:clamp(40px,7vw,80px);margin-bottom:12px">🔥</div>
      <p class="card-title" style="font-size:clamp(22px,3.5vw,48px)">DESEJO</p>
    </div>
  </div>
''')

# 93 - Desequilibre
s(93, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <h1>DESEQUILIBRE</h1>
    <p class="body-text" style="margin-top:24px;max-width:640px">Para que o cliente tome uma decisão, é necessário <b>desequilibrar</b> seu estado atual. Gere medo ou desejo. Sem desequilíbrio, não há decisão.</p>
  </div>
''')

# 94 - Apenas 1 minuto
s(94, f'''
  {badge("Janela de Oportunidade")}
  <div class="big-number">1 MIN</div>
  <p class="highlight">Apenas um minuto</p>
  <p class="body-text">Você tem menos de 1 minuto para criar o gatilho de medo ou desejo no seu cliente. Cada segundo conta.</p>
''')

# 95 - 5 sentidos (título)
s(95, f'''
  {badge("Neurociência")}
  <h2>EXPLORANDO OS 5 SENTIDOS<br>NO ATENDIMENTO</h2>
''')

# 96 - 5 sentidos conceito
s(96, f'''
  {badge("Experiência Neurosensorial")}
  <h2>EXPLORANDO OS 5 SENTIDOS NO ATENDIMENTO</h2>
  <p class="body-text" style="max-width:700px">Uma experiência de venda completa ativa todos os sentidos do cliente, criando uma memória poderosa e uma conexão emocional que vai além do produto.</p>
''')

# 97 - 5 sentidos detalhado
s(97, f'''
  {badge("Experiência Neurosensorial")}
  <h2>EXPLORANDO OS 5 SENTIDOS</h2>
  <div class="cards">
    <div class="card"><p class="card-title">👁️ Visão</p><p class="card-body">O primeiro impacto. Mantenha o espaço sempre limpo e organizado.</p></div>
    <div class="card"><p class="card-title">👂 Audição</p><p class="card-body">O som do ambiente e o que você diz ao cliente.</p></div>
    <div class="card"><p class="card-title">👃 Olfato</p><p class="card-body">O sentido que mais registramos em memória. Um aroma aconchegante é muito importante.</p></div>
    <div class="card"><p class="card-title">👅 Paladar</p><p class="card-body">Se possível, ofereça água, chá — gestos de hospitalidade que conectam.</p></div>
    <div class="card"><p class="card-title">🤝 Tato</p><p class="card-body">O toque cria conexão física e confiança entre pessoas.</p></div>
  </div>
''')

# 98 - Tomada de decisão
s(98, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    {badge("Psicologia")}
    <h1>TOMADA DE<br>DECISÃO</h1>
  </div>
''')

# 99 - Conheça os instintos
s(99, f'''
  {badge("Tomada de Decisão")}
  <h2>OS INSTINTOS E A TOMADA DE DECISÃO</h2>
  <p class="highlight">Conheça o seu cliente</p>
''')

# 100 - Homens e mulheres decidem diferente
s(100, f'''
  {badge("Tomada de Decisão")}
  <h2>HOMENS E MULHERES DECIDEM DE FORMA DIFERENTE.</h2>
  <p class="body-text" style="max-width:720px">O homem tende a decidir com mais rapidez e objetividade. A mulher pondera mais os detalhes e o impacto emocional. Ajuste sua abordagem de acordo com quem está diante de você.</p>
''')

# 101 - Decisões baseadas no "eu"
s(101, f'''
  {badge("Psicologia de Vendas")}
  <div class="quote" style="font-size:clamp(16px,2.2vw,30px)">TODAS AS DECISÕES SÃO BASEADAS EM<br><b>SATISFAÇÃO OU PROTEÇÃO DO "EU".</b></div>
''')

# 102 - 80% emocional
s(102, f'''
  {badge("Neurociência")}
  <div class="big-number">80%+</div>
  <p class="highlight">De qualquer decisão é motivada<br>pelo lado <b style="color:var(--gold-light)">emocional</b></p>
''')

# 103 - (visual/imagem)
s(103, f'''
  {badge("Neurociência")}
  <h2>O LADO EMOCIONAL COMANDA</h2>
  <p class="body-text" style="max-width:720px">O neocórtex racionaliza as decisões, mas quem as inicia é o sistema límbico — emocional. Por isso, conecte-se primeiro emocionalmente, depois apresente os números.</p>
''')

# 104 - Fluxo de impactos
s(104, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    {badge("Neurociência")}
    <h1>FLUXO DE<br>IMPACTOS</h1>
  </div>
''')

# 105 - 8/3000
s(105, f'''
  {badge("Fluxo de Impactos")}
  <div class="big-number" style="font-size:clamp(48px,9vw,128px)">8/3000</div>
  <p class="highlight">Impactos constantes</p>
  <p class="body-text" style="max-width:680px">Seu cliente recebe cerca de 3.000 estímulos por dia e retém apenas 8. Seja um dos 8. Seja impactante, memorável e relevante.</p>
''')

# 106 - Bloco 3 divider
s(106, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both;text-align:center">
    <p class="sub">Bloco 3</p>
    <h1>ESTRATÉGIAS</h1>
  </div>
''')

# 107 - Conexão com cliente digital
s(107, f'''
  {badge("Estratégia Digital")}
  <h2>GERANDO CONEXÃO<br>COM CLIENTE DIGITAL</h2>
''')

# 108 - Era da informação
s(108, f'''
  {badge("Contexto Digital")}
  <h2>ERA DA INFORMAÇÃO</h2>
  <p class="body-text" style="max-width:780px">Vivemos na era da informação, onde o volume de dados consultados diariamente é gigantesco, sobrecarregando o cérebro humano, que permanece inalterado há milhares de anos.<br><br>As decisões de compra são guiadas por <b>impulso</b> (medo ou desejo), enquanto a conexão emocional e a recomendação envolvem níveis mais profundos de confiança.</p>
''')

# 109 - Imagem e tom de voz
s(109, f'''
  {badge("Comunicação")}
  <h2>A SUA IMAGEM</h2>
  <h2>TOM DE VOZ</h2>
''')

# 110 - Imagem e tom de voz 2
s(110, f'''
  {badge("Comunicação")}
  <h2>A SUA IMAGEM E TOM DE VOZ</h2>
  <p class="body-text" style="max-width:720px">Sua imagem e seu tom de voz são as primeiras mensagens que o cliente recebe. Antes de qualquer palavra, ele já formou uma opinião sobre você. <b>Cuide de ambos com dedicação.</b></p>
''')

# 111 - Linguagem corporal
s(111, f'''
  {badge("Comunicação")}
  <h2>A SUA IMAGEM</h2>
  <h2>LINGUAGEM CORPORAL</h2>
''')

# 112 - Linguagem corporal detalhada
s(112, f'''
  {badge("Linguagem Corporal")}
  <h2>SUA EXPRESSÃO E LINGUAGEM CORPORAL</h2>
  <div class="cards">
    <div class="card">
      <p class="card-title">Linguagem Corporal</p>
      <p class="card-body">É a mais importante. Nosso corpo fala muito — gestos, postura e olhar comunicam mais do que as palavras.</p>
    </div>
    <div class="card">
      <p class="card-title">Linguagem Falada</p>
      <p class="card-body">Complementa a linguagem corporal. Tom, ritmo e escolha das palavras são fundamentais.</p>
    </div>
  </div>
''')

# 113 - Os olhos
s(113, f'''
  {badge("Linguagem Corporal")}
  <h2>A LINGUAGEM CORPORAL</h2>
  <div class="quote" style="font-size:clamp(15px,2vw,28px)">OS OLHOS ENTREGAM SENTIMENTOS</div>
  <p class="body-text" style="max-width:680px">Mantenha contato visual firme e seguro. Seus olhos transmitem confiança, honestidade e presença.</p>
''')

# 114 - Atenção à linguagem do cliente
s(114, f'''
  {badge("Linguagem Corporal")}
  <h2>A LINGUAGEM DO CORPO</h2>
  <ul class="list" style="max-width:700px;gap:18px">
    <li>Muita atenção para a <b>Linguagem Corporal do cliente</b></li>
    <li>Muita atenção para a <b>sua Linguagem Corporal</b></li>
  </ul>
''')

# 115 - Sinais corporais
s(115, f'''
  {badge("Leitura Corporal")}
  <h2>A LINGUAGEM DO CORPO</h2>
  <div class="cards">
    <div class="card" style="border-color:rgba(239,68,68,0.3)">
      <p class="card-title" style="color:#fca5a5">Sinais Negativos</p>
      <ul class="list" style="gap:8px">
        <li>Olhar desfocado — insegurança</li>
        <li>Mão tocando o queixo — pode estar mentindo</li>
        <li>Braços cruzados — desconforto</li>
      </ul>
    </div>
    <div class="card" style="border-color:rgba(34,197,94,0.3)">
      <p class="card-title" style="color:#86efac">Sinais de Autoconfiança</p>
      <ul class="list" style="gap:8px">
        <li>Olhar nos olhos — seguro e no controle</li>
        <li>Postura neutra — mãos levemente abertas</li>
      </ul>
    </div>
  </div>
''')

# 116 - Modo de se comunicar
s(116, f'''
  {badge("Comunicação")}
  <h2>O MODO DE SE COMUNICAR</h2>
''')

# 117 - 7/38/55
s(117, f'''
  {badge("Comunicação Eficaz")}
  <h2>O MODO DE SE COMUNICAR</h2>
  <div class="cards">
    <div class="card" style="text-align:center;border-color:rgba(217,184,85,0.35)">
      <p class="big-number" style="font-size:clamp(48px,8vw,100px)">55%</p>
      <p class="card-title">Seu Visual</p>
    </div>
    <div class="card" style="text-align:center">
      <p class="big-number" style="font-size:clamp(48px,8vw,100px)">38%</p>
      <p class="card-title">Como você diz</p>
    </div>
    <div class="card" style="text-align:center">
      <p class="big-number" style="font-size:clamp(48px,8vw,100px)">7%</p>
      <p class="card-title">O que você diz</p>
    </div>
  </div>
  <p class="body-text">Comunicação eficaz e objetiva</p>
''')

# 118 - Treine o modo de se comunicar
s(118, f'''
  {badge("Comunicação")}
  <h2>TREINE O MODO DE SE COMUNICAR</h2>
  <ul class="list" style="max-width:700px;gap:18px">
    <li>Grave vídeos de si mesmo e analise sua comunicação</li>
    <li>Treine o tom de voz — grave áudios e ouça</li>
    <li>Pratique na frente do espelho</li>
    <li>Peça feedback de pessoas próximas</li>
  </ul>
''')

# 119 - O palco do atendimento
s(119, f'''
  {badge("Atendimento Presencial")}
  <h2>O PALCO DO ATENDIMENTO</h2>
  <p class="body-text" style="max-width:720px">Seu local de atendimento é um palco. Cada detalhe — organização, iluminação, aroma, materiais — comunica profissionalismo e confiança ao cliente.</p>
''')

# 120 - Sua comunicação
s(120, f'''
  {badge("Comunicação")}
  <h2>SUA COMUNICAÇÃO</h2>
  <p class="body-text" style="max-width:720px">Sua comunicação deve ser a extensão da sua identidade profissional. Seja consistente em todos os canais: WhatsApp, redes sociais, vídeos e presencialmente.</p>
''')

# 121 - Perfil na rede social
s(121, f'''
  {badge("Presença Digital")}
  <h2>O SEU PERFIL NA REDE SOCIAL</h2>
''')

# 122 - Comunicação clara
s(122, f'''
  {badge("Comunicação")}
  <h2>SUA COMUNICAÇÃO</h2>
  <div class="cards">
    <div class="card"><p class="card-title">RÁPIDA</p><p class="card-body">Focada em fazer o que precisa ser feito na busca de resultados</p></div>
    <div class="card"><p class="card-title">CLARA</p><p class="card-body">Sem ambiguidades — o cliente entende exatamente o que você quer dizer</p></div>
    <div class="card"><p class="card-title">PROFISSIONAL</p><p class="card-body">Mantém autoridade e credibilidade em todo contato</p></div>
  </div>
''')

# 123 - Perfil como vitrine
s(123, f'''
  {badge("Seu Perfil Digital")}
  <h2>SEU PERFIL É A VITRINE DO SEU NEGÓCIO</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Tudo começa com uma reflexão sobre como está sua vida atualmente e o posicionamento do seu perfil nas redes sociais. Por mais que você seja uma pessoa física, o agente de negócios deve sempre tratar-se como uma empresa.</div>
''')

# 124 - Equilíbrio perfil profissional/pessoal
s(124, f'''
  {badge("Presença Digital")}
  <h2>EQUILÍBRIO PROFISSIONAL E PESSOAL</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Tenha um perfil digital focado no profissional, mas nunca esqueça de compartilhar momentos de alegria e com sua família. Por mais que seja um perfil para gerar negócios, lembre-se que você é humano — o equilíbrio é essencial.</div>
''')

# 125 - Rotina e consistência (título)
s(125, f'''
  {badge("Estratégia Digital")}
  <h2>SUA ROTINA E CONSISTÊNCIA</h2>
''')

# 126 - Rotina detalhada
s(126, f'''
  {badge("Rotina e Consistência")}
  <h2>SUA ROTINA E CONSISTÊNCIA</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Após atualizar seu perfil, defina sua rotina de publicação. O que chamará a atenção do seu público-alvo é a <b>frequência</b> com que eles enxergam o que você posta — isso é consistência.</div>
''')

# 127 - Carga horária dedicada
s(127, f'''
  {badge("Foco e Consistência")}
  <h2>SUA ROTINA E CONSISTÊNCIA</h2>
  <div class="quote">"Quando resolvemos fazer tudo, não fazemos quase nada realmente bem-feito."</div>
  <p class="body-text" style="max-width:680px">Reserve uma <b>carga horária diária</b> para dedicar-se ao seu negócio. Foco gera resultado.</p>
''')

# 128 - Ancoragem
s(128, f'''
  {badge("Credibilidade")}
  <h2>SUA ANCORAGEM E CREDIBILIDADE</h2>
''')

# 129 - Tenha uma âncora
s(129, f'''
  {badge("Ancoragem")}
  <h2>TENHA UMA ÂNCORA</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Se agarre a algo maior que você: sua cidade de atuação, a construtora, o projeto de expansão da região — apoie-se em pilares sólidos. Ao fazer isso, você aumenta sua ancoragem e torna maior a chance de ser percebido frente à acirrada concorrência.</div>
''')

# 130 - Verdade e confiança
s(130, f'''
  {badge("Credibilidade")}
  <h2>VERDADE E CONFIANÇA</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Seu perfil precisa exibir conteúdos verdadeiros. Sua linguagem deve transmitir palavras de segurança, firmes, que gerem confiança. Em qualquer tipo de venda, estabelecer confiança entre vendedor e comprador é fundamental.</div>
''')

# 131 - Seu investimento
s(131, f'''
  {badge("Investimento em Tráfego")}
  <h2>SEU INVESTIMENTO</h2>
''')

# 132 - Invista em redes sociais
s(132, f'''
  {badge("Tráfego Pago")}
  <h2>SEU INVESTIMENTO</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">"As redes sociais se tornaram o canal de comunicação mais lucrativo existente atualmente. <b>Se você não investe, você não aparece.</b> Reserve um valor para iniciar suas campanhas online, contrate especialistas e direcione seus recursos corretamente."</div>
''')

# 133 - Empatia
s(133, f'''
  {badge("Conexão")}
  <h2>SUA EMPATIA PARA CONECTAR</h2>
''')

# 134 - A empatia conecta
s(134, f'''
  {badge("Empatia")}
  <h2>A EMPATIA É O QUE CONECTA</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Você elaborou cuidadosamente seu perfil, definiu sua rotina, aplicou consistência, ancorou e gerou credibilidade, fez o investimento correto e mesmo assim não teve resultado? <b>Saiba que a empatia é o que conecta.</b></div>
''')

# 135 - Identifique-se com o cliente
s(135, f'''
  {badge("Empatia")}
  <h2>SEU CLIENTE PRECISA SE IDENTIFICAR COM VOCÊ</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Defina qual tipo de cliente você deseja atrair. O ideal é que o perfil seja semelhante ao seu — tudo ficará mais fácil e natural para interagir. Quando buscamos clientes muito diferentes de nós, fica mais difícil nos moldarmos a este novo perfil.</div>
''')

# 136 - Conhecimento e reinvenção
s(136, f'''
  {badge("Crescimento")}
  <h2>SEU CONHECIMENTO E O PODER DE SE REINVENTAR</h2>
''')

# 137 - Rebranding pessoal
s(137, f'''
  {badge("Reinvenção")}
  <h2>SEU CONHECIMENTO E O PODER DE SE REINVENTAR</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Faça cursos, leia livros, busque inspirar-se todos os dias. Seu conhecimento é apenas seu — ninguém tira. Lembre-se que você é uma <b>marca viva</b>, e vai precisar passar por um rebranding muitas vezes ao longo de sua vida.</div>
''')

# 138 - Negociação
s(138, f'''
  {badge("Habilidades")}
  <h2>SUAS HABILIDADES EM NEGOCIAÇÃO</h2>
''')

# 139 - Atenção plena na negociação
s(139, f'''
  {badge("Negociação")}
  <h2>SUAS HABILIDADES EM NEGOCIAÇÃO</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">O momento da negociação é crucial. É quando você precisa de <b>atenção plena</b> — mindfulness. O princípio básico do êxito em qualquer negociação é o controle da sua ansiedade e do seu estresse. Controle sua mente — ela é sua maior aliada.</div>
''')

# 140 - Poder de persuasão
s(140, f'''
  {badge("Persuasão")}
  <h2>SEU PODER DE PERSUASÃO</h2>
  <p class="body-text" style="max-width:720px">A persuasão não é manipulação. É a arte de apresentar o valor real do produto de forma que o cliente perceba claramente o benefício para si. Persuasão ética gera confiança e relacionamento de longo prazo.</p>
''')

# 141 - Qual comando você dá?
s(141, f'''
  {badge("Fechamento")}
  <h2>QUAL COMANDO VOCÊ DÁ AO CLIENTE?</h2>
''')

# 142 - Ele executa
s(142, f'''
  {badge("Comando")}
  <h1>QUAL COMANDO<br>VOCÊ DÁ AO<br>SEU CLIENTE?</h1>
  <div class="quote">CUIDA, POIS ELE EXECUTA.</div>
''')

# 143 - Fechamento da venda (título)
s(143, f'''
  {badge("Fechamento")}
  <h2>O FECHAMENTO<br>DA VENDA</h2>
''')

# 144 - Fechamento 1
s(144, f'''
  {badge("O Fechamento da Venda")}
  <h2>O FECHAMENTO DA VENDA</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Saiba que quem define aquilo que será vendido ou comprado é o <b>vendedor</b>. Gerar uma conexão não significa que realizou uma venda. Para a venda acontecer é necessário estudar o fechamento.<br><br>Este é o momento de repetir o nome do seu cliente — a palavra que mais gostamos de ouvir é o nosso próprio nome.</div>
''')

# 145 - Fechamento 2
s(145, f'''
  {badge("O Fechamento da Venda")}
  <h2>O FECHAMENTO DA VENDA</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Nesta etapa você continuará contornando objeções. Valorize a conexão que estabeleceu com seu cliente. Respire fundo, se mantenha firme e focado.<br><br>Reforce todos os benefícios que conquistou na negociação para o seu cliente. Reforce os ganhos futuros.</div>
''')

# 146 - Fechamento 3
s(146, f'''
  {badge("O Fechamento da Venda")}
  <h2>O FECHAMENTO DA VENDA</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Transmita <b>segurança e otimismo</b>. Seja firme e jamais tenha medo de solicitar os dados para a elaboração do contrato. Mesmo após o envio do contrato, poderão existir questionamentos jurídicos — isso é normal. Explique os detalhes e ajuste o que for necessário.</div>
''')

# 147 - Fechamento 4 - equilíbrio
s(147, f'''
  {badge("Mentalidade")}
  <h2>O FECHAMENTO DA VENDA</h2>
  <div class="quote" style="font-size:clamp(12px,1.2vw,17px)">Trabalhe sua mente, seu equilíbrio. Pratique a meditação e faça exercícios. O resultado do seu trabalho é uma consequência de uma série de combinações do seu modo de ser e agir frente às mais diversas situações. <b>Seu sucesso é inevitável.</b></div>
''')

# 148 - Repete e aprimora
s(148, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both">
    <h1>REPETE E<br>APRIMORA</h1>
  </div>
''')

# 149 - Por isso você precisa ter
s(149, f'''
  {badge("Consistência")}
  <h2>POR ISSO VOCÊ PRECISA TER</h2>
  <div class="pill-row" style="gap:16px">
    {''.join(f'<span class="pill" style="font-size:clamp(10px,1.1vw,15px);padding:10px 24px">{p}</span>' for p in ['CONSISTÊNCIA','DISCIPLINA','FOCO','RESILIÊNCIA','AUTOCONHECIMENTO'])}
  </div>
''')

# 150 - Encantar e gerar experiência
s(150, f'''
  {badge("Filosofia")}
  <h1>COM FOCO EM<br>ENCANTAR E<br>GERAR EXPERIÊNCIA</h1>
''')

# 151 - Medindo sua performance (título)
s(151, f'''
  {badge("Performance")}
  <h2>MEDINDO SUA<br>PERFORMANCE</h2>
''')

# 152 - Métricas
s(152, f'''
  {badge("Métricas de Performance")}
  <h2>MEDINDO SUA PERFORMANCE</h2>
  <div class="cards">
    <div class="card">
      <p class="card-title">📈 Taxa de Conversão</p>
      <p class="card-body">Serve para avaliar apenas sua empresa de tráfego pago ou campanhas</p>
    </div>
    <div class="card">
      <p class="card-title">🤝 Taxa de Fechamento</p>
      <p class="card-body">Serve para realmente avaliar o seu desempenho — propostas apresentadas vs. fechadas</p>
    </div>
    <div class="card">
      <p class="card-title">💎 VGV</p>
      <p class="card-body">Valor Geral de Vendas — e unidades vendidas. Sua principal métrica de resultado.</p>
    </div>
  </div>
''')

# 153 - Psicologia das cores
s(153, f'''
  {badge("Psicologia das Cores")}
  <h2>PSICOLOGIA DAS CORES</h2>
  <div style="display:grid;grid-template-columns:repeat(9,1fr);gap:clamp(6px,1vw,14px);width:100%;max-width:900px;z-index:2">
    {''.join(f'''<div style="display:flex;flex-direction:column;align-items:center;gap:6px;animation:fadeUp 0.5s ease both {0.3+i*0.05:.2f}s">
      <div style="width:100%;aspect-ratio:1;border-radius:8px;background:{c};border:1px solid rgba(255,255,255,0.1)"></div>
      <p style="font-family:var(--font-display);font-size:clamp(7px,0.7vw,9px);letter-spacing:0.08em;text-transform:uppercase;color:rgba(255,255,255,0.55);text-align:center">{n}</p>
      <p style="font-family:var(--font-body);font-size:clamp(6px,0.6vw,8px);color:rgba(255,255,255,0.32);text-align:center;line-height:1.2">{m}</p>
    </div>''' for i,(c,n,m) in enumerate([
      ('#1E40AF','Azul','Confiança e segurança'),
      ('#DC2626','Vermelho','Emoção e paixão'),
      ('#EA580C','Laranja','Amigável e agradável'),
      ('#16A34A','Verde','Tranquilidade e serenidade'),
      ('#7C3AED','Roxo','Inovação e inteligência'),
      ('#9333EA','Violeta','Criatividade e luxo'),
      ('#CA8A04','Amarelo','Alegria e jovialidade'),
      ('linear-gradient(135deg,#F2DEA0,#D9B855,#A66617)','Dourado','Luxo e excelência'),
      ('linear-gradient(135deg,#fff,#e5e7eb)','Branco','Transparência'),
    ]))}
  </div>
''')

# 154 - The Best Salesman Ever (closing)
s(154, f'''
  <div style="z-index:2;animation:fadeUp 0.8s ease both;text-align:center">
    <p class="sub">The Best Salesman Ever</p>
    <h1>A SUA MOEDA<br>DE VALOR</h1>
  </div>
''')

# 155 - Encerramento
s(155, f'''
  {badge("Encerramento")}
  <h1>GRATO PELA<br>ATENÇÃO!</h1>
  <div class="divider"></div>
  <p class="highlight">Siga nossas Redes Sociais</p>
  <div class="quote" style="font-size:clamp(14px,1.8vw,24px);padding:16px 32px">THE BEST SALESMAN EVER<br><span style="font-size:0.7em;color:var(--gold-50)">Universo Corporativo · Patrick Piccoli</span></div>
''')

print(f"Generated {155} slides in ./{OUT}/")
