import re, shutil
PAGES=[("index.html","トップ"),("symmetry-matrices.html","対称操作の行列"),("basis-change.html","基底変換 P"),("crystal-systems.html","晶系と格子系"),("cells.html","慣用セルと基本セル"),("basis-vectors.html","基底ベクトル")]
def nav(cur):
    return '<nav class="top">'+''.join(f'<a href="{f}"{" class=\"cur\"" if f==cur else ""}>{t}</a>' for f,t in PAGES)+'</nav>'
def page(fn,title,body):
    html=f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}｜結晶の対称性と格子</title><link rel="stylesheet" href="style.css"></head>
<body>{nav(fn)}<main>{body}</main></body></html>'''
    open(fn,'w',encoding='utf-8').write(html)

def mk(id_,col): return f'<marker id="{id_}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="{col}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
PU,CO='#534AB7','#D85A30'

SVG_HEX3=f'''<svg viewBox="0 0 380 400" role="img" aria-label="六方軸の3回回転と行列"><defs>{mk("hP",PU)}{mk("hC",CO)}</defs>
<g fill="var(--t)" opacity="0.6"><circle cx="55" cy="92" r="3"/><circle cx="145" cy="92" r="3"/><circle cx="235" cy="92" r="3"/><circle cx="325" cy="92" r="3"/><circle cx="100" cy="170" r="3"/><circle cx="190" cy="170" r="3"/><circle cx="280" cy="170" r="3"/><circle cx="55" cy="248" r="3"/><circle cx="145" cy="248" r="3"/><circle cx="235" cy="248" r="3"/><circle cx="325" cy="248" r="3"/></g>
<line x1="190" y1="170" x2="276" y2="170" stroke="{PU}" stroke-width="2" marker-end="url(#hP)"/>
<line x1="190" y1="170" x2="147" y2="96" stroke="{PU}" stroke-width="2" marker-end="url(#hP)"/>
<line x1="190" y1="170" x2="147" y2="244" stroke="{CO}" stroke-width="2" stroke-dasharray="5 3" marker-end="url(#hC)"/>
<path d="M230 170 A40 40 0 0 0 172 134" fill="none" stroke="{CO}" stroke-width="1" marker-end="url(#hC)"/>
<path d="M175 144 A30 30 0 0 0 175 196" fill="none" stroke="{CO}" stroke-width="1" marker-end="url(#hC)"/>
<text class="th" x="290" y="175">a₁</text><text class="th" x="60" y="72">a₂ = R a₁</text><text class="th" x="40" y="280">R a₂ = −a₁ − a₂</text><text class="ts" x="250" y="135">120° 回転</text>
<text class="th" x="100" y="345" text-anchor="middle" dominant-baseline="central">W =</text>
<path d="M150 315 L142 315 L142 375 L150 375" fill="none" stroke="var(--p)" stroke-width="1"/><path d="M250 315 L258 315 L258 375 L250 375" fill="none" stroke="var(--p)" stroke-width="1"/>
<rect x="157" y="312" width="38" height="66" rx="4" fill="none" stroke="{PU}" stroke-width="0.6" stroke-dasharray="3 2"/><rect x="205" y="312" width="38" height="66" rx="4" fill="none" stroke="{CO}" stroke-width="0.6" stroke-dasharray="3 2"/>
<text class="t" x="176" y="330" text-anchor="middle" dominant-baseline="central">0</text><text class="t" x="176" y="360" text-anchor="middle" dominant-baseline="central">1</text><text class="t" x="224" y="330" text-anchor="middle" dominant-baseline="central">−1</text><text class="t" x="224" y="360" text-anchor="middle" dominant-baseline="central">−1</text>
<text class="ts" x="176" y="392" text-anchor="middle">R a₁</text><text class="ts" x="224" y="392" text-anchor="middle">R a₂</text></svg>'''

SVG_RH3=f'''<svg viewBox="0 0 380 400" role="img" aria-label="菱面体軸の3回回転と行列"><defs>{mk("rP",PU)}{mk("rC",CO)}</defs>
<circle cx="190" cy="160" r="4" fill="var(--p)"/>
<line x1="190" y1="160" x2="190" y2="79" stroke="{PU}" stroke-width="2" marker-end="url(#rP)"/>
<line x1="190" y1="160" x2="120" y2="200" stroke="{PU}" stroke-width="2" marker-end="url(#rP)"/>
<line x1="190" y1="160" x2="260" y2="200" stroke="{PU}" stroke-width="2" marker-end="url(#rP)"/>
<path d="M180.4 105.8 A55 55 0 0 0 138.3 178.8" fill="none" stroke="{CO}" stroke-width="1" marker-end="url(#rC)"/>
<path d="M147.9 195.4 A55 55 0 0 0 232.1 195.4" fill="none" stroke="{CO}" stroke-width="1" marker-end="url(#rC)"/>
<path d="M241.7 178.8 A55 55 0 0 0 199.6 105.8" fill="none" stroke="{CO}" stroke-width="1" marker-end="url(#rC)"/>
<text class="th" x="198" y="76">a₁</text><text class="th" x="108" y="218" text-anchor="end">a₂</text><text class="th" x="272" y="218">a₃</text>
<text class="ts" x="190" y="252" text-anchor="middle">[111] 方向から見た投影（中心が 3 回軸）</text>
<text class="th" x="95" y="325" text-anchor="middle" dominant-baseline="central">W =</text>
<path d="M146 290 L138 290 L138 360 L146 360" fill="none" stroke="var(--p)" stroke-width="1"/><path d="M234 290 L242 290 L242 360 L234 360" fill="none" stroke="var(--p)" stroke-width="1"/>
''' + ''.join(f'<text class="t" x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central">{v}</text>' for (x,y,v) in [(160,300,0),(190,300,0),(220,300,1),(160,325,1),(190,325,0),(220,325,0),(160,350,0),(190,350,1),(220,350,0)]) + '''
<text class="ts" x="160" y="382" text-anchor="middle">Ra₁</text><text class="ts" x="190" y="382" text-anchor="middle">Ra₂</text><text class="ts" x="220" y="382" text-anchor="middle">Ra₃</text></svg>'''

SVG_P=f'''<svg viewBox="0 0 380 400" role="img" aria-label="基底変換行列Pの意味"><defs>{mk("pP",PU)}{mk("pC",CO)}</defs>
<g fill="var(--t)" opacity="0.6">''' + ''.join(f'<circle cx="{x}" cy="{y}" r="3"/>' for x in (70,150,230,310) for y in (230,150,70)) + f'''</g>
<path d="M150 230 L230 150 L150 150" fill="none" stroke="{CO}" stroke-width="0.8" stroke-dasharray="4 3"/>
<path d="M150 230 L150 150 L70 150" fill="none" stroke="{PU}" stroke-width="0.8" stroke-dasharray="4 3"/>
<line x1="70" y1="230" x2="146" y2="230" stroke="{PU}" stroke-width="2" marker-end="url(#pP)"/>
<line x1="70" y1="230" x2="70" y2="154" stroke="{PU}" stroke-width="2" marker-end="url(#pP)"/>
<line x1="70" y1="238" x2="146" y2="238" stroke="{CO}" stroke-width="2" marker-end="url(#pC)"/>
<line x1="70" y1="230" x2="147" y2="153" stroke="{CO}" stroke-width="2" marker-end="url(#pC)"/>
<text class="th" x="100" y="222" text-anchor="middle">a₁</text><text class="th" x="100" y="258" text-anchor="middle">b₁ = a₁</text><text class="th" x="56" y="195" text-anchor="end">a₂</text><text class="th" x="160" y="128">b₂ = a₁ + a₂</text>
<text class="th" x="100" y="320" text-anchor="middle" dominant-baseline="central">P =</text>
<path d="M150 290 L142 290 L142 350 L150 350" fill="none" stroke="var(--p)" stroke-width="1"/><path d="M250 290 L258 290 L258 350 L250 350" fill="none" stroke="var(--p)" stroke-width="1"/>
<rect x="157" y="287" width="38" height="66" rx="4" fill="none" stroke="{CO}" stroke-width="0.6" stroke-dasharray="3 2"/><rect x="205" y="287" width="38" height="66" rx="4" fill="none" stroke="{CO}" stroke-width="0.6" stroke-dasharray="3 2"/>
<text class="t" x="176" y="305" text-anchor="middle" dominant-baseline="central">1</text><text class="t" x="176" y="335" text-anchor="middle" dominant-baseline="central">0</text><text class="t" x="224" y="305" text-anchor="middle" dominant-baseline="central">1</text><text class="t" x="224" y="335" text-anchor="middle" dominant-baseline="central">1</text>
<text class="ts" x="176" y="370" text-anchor="middle">b₁ を a で</text><text class="ts" x="224" y="386" text-anchor="middle">b₂ を a で</text>
<text class="ts" x="290" y="310">紫：古い基底</text><text class="ts" x="290" y="334">橙：新しい基底</text></svg>'''

SVG_RECT=f'''<svg viewBox="0 0 380 210" role="img" aria-label="同じ長方形セルでも直方晶と単斜晶がある例">
<text class="ts" x="100" y="40" text-anchor="middle">a ≠ b, γ = 90°</text><text class="ts" x="280" y="40" text-anchor="middle">a ≠ b, γ = 90°</text>
<rect x="40" y="60" width="120" height="80" fill="none" stroke="var(--s)" stroke-width="1"/><rect x="220" y="60" width="120" height="80" fill="none" stroke="var(--s)" stroke-width="1"/>
<line x1="100" y1="52" x2="100" y2="148" stroke="#1D9E75" stroke-width="1.2" stroke-dasharray="5 3"/><line x1="32" y1="100" x2="168" y2="100" stroke="#1D9E75" stroke-width="1.2" stroke-dasharray="5 3"/>
<g class="c-gray">''' + ''.join(f'<circle cx="{x}" cy="{y}" r="6"/>' for x in (40,160,220,340) for y in (60,140)) + f'''</g>
<line x1="85" y1="100" x2="115" y2="100" stroke="{CO}" stroke-width="2"/><line x1="264" y1="90" x2="296" y2="110" stroke="{CO}" stroke-width="2"/>
<g class="c-coral"><circle cx="85" cy="100" r="7"/><circle cx="115" cy="100" r="7"/><circle cx="264" cy="90" r="7"/><circle cx="296" cy="110" r="7"/></g>
<ellipse cx="280" cy="100" rx="3" ry="6" fill="var(--p)"/>
<text class="th" x="100" y="172" text-anchor="middle">直方晶</text><text class="ts" x="100" y="192" text-anchor="middle">鏡映面あり（緑の点線）</text>
<text class="th" x="280" y="172" text-anchor="middle">単斜晶</text><text class="ts" x="280" y="192" text-anchor="middle">鏡映面なし、2 回軸のみ</text></svg>'''

HEXS={(75,170),(145,170),(40,109.4),(110,109.4)}
def hexagon(cx,cy,r=5): 
    import math
    return '<polygon points="'+' '.join(f'{cx+r*math.cos(k*math.pi/3):.1f},{cy+r*math.sin(k*math.pi/3):.1f}' for k in range(6))+'"/>'
def tri(cx,cy,r=5):
    import math
    return '<polygon points="'+' '.join(f'{cx+r*math.cos(math.radians(a)):.1f},{cy-r*math.sin(math.radians(a)):.1f}' for a in (90,210,330))+'"/>'
L_CORN=[(75,170),(145,170),(40,109.4),(110,109.4)]; R_CORN=[(255,170),(325,170),(220,109.4),(290,109.4)]
R_IN=[(290,149.8),(255,129.6)]
SVG_LAT=f'''<svg viewBox="0 0 380 290" role="img" aria-label="六方格子hPと菱面体格子hRの格子点と対称軸">
<text class="ts" x="190" y="70" text-anchor="middle">c 軸方向から見た六方セル（数字は高さ z）</text>
<path d="M75 170 L145 170 L110 109.4 L40 109.4 Z" fill="none" stroke="var(--s)" stroke-width="1"/><path d="M255 170 L325 170 L290 109.4 L220 109.4 Z" fill="none" stroke="var(--s)" stroke-width="1"/>
<g class="c-coral">''' + ''.join(f'<circle cx="{x}" cy="{y}" r="8"/>' for x,y in L_CORN+R_CORN+R_IN+[(50,248)]) + '</g><g fill="var(--p)">' + ''.join(hexagon(x,y) for x,y in L_CORN+[(180,248)]) + ''.join(tri(x,y) for x,y in R_CORN+R_IN+[(50,271)]) + '''</g>
<text class="ts" x="279" y="154" text-anchor="end">1/3</text><text class="ts" x="266" y="134">2/3</text>
<text class="th" x="92" y="202" text-anchor="middle">hP（六方格子）</text><text class="ts" x="92" y="222" text-anchor="middle">格子の対称 6/mmm</text>
<text class="th" x="272" y="202" text-anchor="middle">hR（菱面体格子）</text><text class="ts" x="272" y="222" text-anchor="middle">格子の対称 3̄m</text>
<text class="ts" x="62" y="252">格子点</text><text class="ts" x="194" y="252">6 回軸</text><text class="ts" x="62" y="276">3 回軸</text></svg>'''
import math
def ring(cx,cy,n,r=12,start=0):
    return [(cx+r*math.cos(math.radians(start+360*k/n)), cy-r*math.sin(math.radians(start+360*k/n))) for k in range(n)]
atoms=[]
for c in L_CORN: atoms+=ring(*c,6)
for c in R_CORN: atoms+=ring(*c,3,start=90)
SVG_MOT=f'''<svg viewBox="0 0 380 290" role="img" aria-label="同じhP単位胞での六方晶系と三方晶系">
<text class="ts" x="190" y="70" text-anchor="middle">格子はどちらも hP（同じ菱形の単位胞）</text>
<path d="M75 170 L145 170 L110 109.4 L40 109.4 Z" fill="none" stroke="var(--s)" stroke-width="0.8"/><path d="M255 170 L325 170 L290 109.4 L220 109.4 Z" fill="none" stroke="var(--s)" stroke-width="0.8"/>
<g class="c-coral">''' + ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5"/>' for x,y in atoms+[(50,248)]) + '</g><g fill="var(--p)">' + ''.join(hexagon(x,y) for x,y in L_CORN+[(180,248)]) + ''.join(tri(x,y) for x,y in R_CORN+[(50,271)]) + '''</g>
<text class="th" x="92" y="202" text-anchor="middle">六方晶系</text><text class="ts" x="92" y="222" text-anchor="middle">6 回対称の原子配置</text>
<text class="th" x="272" y="202" text-anchor="middle">三方晶系</text><text class="ts" x="272" y="222" text-anchor="middle">3 回対称の原子配置</text>
<text class="ts" x="62" y="252">原子</text><text class="ts" x="194" y="252">6 回軸</text><text class="ts" x="62" y="276">3 回軸</text></svg>'''

TA,TB,TC=[open(f"src/figs/tiling_{k}.svg",encoding="utf-8").read() for k in "abc"]
ZLEG='<p style="font-size:13px;color:var(--sub)"><span style="color:#888780">●</span> z = 0　<span style="color:#D85A30">●</span> z = 1/3　<span style="color:#1D9E75">●</span> z = 2/3</p>'
# ---- pages ----
page("index.html","トップ",f'''<h1>結晶の対称性と格子 — 図解</h1>
<p class="lead">結晶座標での対称操作の行列、基底変換、晶系と格子系、慣用セルと基本セルを図で確認するための教材です。</p>
<ul class="cards">
<li><a href="symmetry-matrices.html"><b>対称操作の行列</b><span>結晶座標では行列要素が 0, ±1 になる理由。六方軸と菱面体軸の 3 回回転。</span></a></li>
<li><a href="basis-change.html"><b>基底変換 P</b><span>(a′, b′, c′) = (a, b, c)P、ξ = Pξ′、W′ = P⁻¹WP。各ブラベー格子の P。</span></a></li>
<li><a href="crystal-systems.html"><b>晶系と格子系</b><span>セルの形だけでは晶系が決まらない例。hP と hR、六方晶系と三方晶系。</span></a></li>
<li><a href="cells.html"><b>慣用セルと基本セル（立体図）</b><span>BCC・FCC・底心・六方・三方の慣用セルと基本セルを重ねて回転できる図。</span></a></li>
<li><a href="basis-vectors.html"><b>基底ベクトル（立体図）</b><span>a, b, c と a′, b′, c′ を矢印で示し、変換行列 P と対応させた図。</span></a></li>
</ul>''')

page("symmetry-matrices.html","対称操作の行列",f'''<h1>対称操作の行列</h1>
<p class="lead">標準の結晶軸（慣用セル）で書くと、点群の対称操作の行列要素は 0, ±1 になる。</p>
<h2>基底によらず言えること</h2>
<ul><li>格子点を格子点に写すので、結晶座標での行列 W は整数行列。</li><li>det W = ±1（回転は +1、鏡映・反転・回反は −1）。</li><li>回転角 θ の回転では tr W = 1 + 2cos θ が整数。よって θ は 60°, 90°, 120°, 180°, 360° に限られる（結晶学的制限定理）。</li></ul>
<p>0, ±1 に収まるのは基底の選び方による。斜めの基底を選ぶと 2 以上の整数も現れる（例：正方格子で b₁ = a₁、b₂ = a₁ + a₂ とすると 90° 回転は ((−1, −2), (1, 1))）。</p>
<h2>六方軸の 3 回回転</h2>
<figure>{SVG_HEX3}<figcaption>行列の各列は、回した基底ベクトルを元の基底で表した係数。ab 面内に基底が 2 本しかないため、3 本目の等価なベクトル −a₁ − a₂ を使い −1 が現れる。</figcaption></figure>
<h2>菱面体軸の 3 回回転</h2>
<figure>{SVG_RH3}<figcaption>等価な 3 方向がすべて基底なので、a₁ → a₂ → a₃ → a₁ と入れ替わるだけ。行列は置換行列で、立方晶の [111] まわりの 3 回回転と同じ形。</figcaption></figure>
<h2>操作ごとの det と trace</h2>
<table><tr><th>種類</th><th>操作</th><th>det</th><th>trace</th></tr>
<tr><td>回転</td><td>1, 2, 3, 4, 6</td><td>+1</td><td>1 + 2cos θ</td></tr>
<tr><td>反転</td><td>1̄</td><td>−1</td><td>−3</td></tr>
<tr><td>鏡映</td><td>m（= 2̄）</td><td>−1</td><td>1</td></tr>
<tr><td>回反</td><td>3̄, 4̄, 6̄</td><td>−1</td><td>−(1 + 2cos θ)</td></tr></table>
<p>trace と det は相似変換 W′ = P⁻¹WP で変わらないので、どの基底で計算しても同じ値になる。</p>''')

page("basis-change.html","基底変換 P",f'''<h1>基底変換 P</h1>
<p class="lead">P の各列は、新しい基底ベクトルを古い基底で表した係数。International Tables・VESTA と同じ流儀。</p>
<pre>基底の変換   (a′, b′, c′) = (a, b, c)P     … 基底には右から
座標の変換   ξ = Pξ′,  ξ′ = P⁻¹ξ         … 座標には左から
ベクトル     x = (a, b, c)ξ = (a, b, c)Pξ′ = (a′, b′, c′)ξ′
対称操作     W′ = P⁻¹WP
体積比       det P = V′ / V</pre>
<h2>例：正方格子</h2>
<figure>{SVG_P}<figcaption>新しい座標 (0, 1)（b₂ を 1 本）に P をかけると第 2 列 (1, 1) が出て、古い座標と一致する。正方形と平行四辺形の面積は等しく、det P = 1。</figcaption></figure>
<h2>慣用セル → 基本セルの P</h2>
<pre>BCC（I）  a′ = ( a + b − c)/2, b′ = (−a + b + c)/2, c′ = (a − b + c)/2   det P = 1/2
FCC（F）  a′ = (b + c)/2,  b′ = (a + c)/2,  c′ = (a + b)/2              det P = 1/4
底心（C）  a′ = (a − b)/2,  b′ = (a + b)/2,  c′ = c                      det P = 1/2
六方（hP）  P = E（慣用セル = 基本セル）                                 det P = 1
三方（hR）  a′ = (2a + b + c)/3, b′ = (−a + b + c)/3, c′ = (−a − 2b + c)/3  det P = 1/3</pre>
<p>det P は慣用セルに含まれる格子点の数（I = 2、F = 4、C = 2、R = 3）の逆数。立体図は <a href="basis-vectors.html">基底ベクトル</a> のページ。</p>''')

page("crystal-systems.html","晶系と格子系",f'''<h1>晶系と格子系</h1>
<p class="lead">晶族・晶系・ブラベー格子の型は、単位胞の形ではなく、結晶がもつ対称要素、具体的には回転軸（回反軸を含む）で決まる。セルの形は、その回転軸があれば必ず満たされる結果（必要条件）にすぎない。</p>
<h2>分類を決めるもの：回転軸</h2>
<p>各晶系は、次の回転軸をもつかどうかで決まる。鏡映面は 2̄ 軸、反転中心は 1̄ として回反軸に含める。晶族も同じく回転軸で決まり、3 回軸または 6 回軸を 1 本もつ三方晶系と六方晶系が、まとめて六方晶族になる。</p>
<table class="cls"><tr><th>晶族</th><th>晶系</th><th>決め手となる回転軸</th><th>セルの形（結果として満たす条件）</th></tr>
<tr><td>三斜</td><td>三斜晶系</td><td>なし（1 または 1̄ のみ）</td><td>制約なし</td></tr>
<tr><td>単斜</td><td>単斜晶系</td><td>2 回軸または 2̄ 軸が 1 本</td><td>2 回軸を b 軸にとると α = γ = 90°</td></tr>
<tr><td>直方</td><td>直方晶系</td><td>互いに直交する 2 回軸または 2̄ 軸が 3 本</td><td>α = β = γ = 90°</td></tr>
<tr><td>正方</td><td>正方晶系</td><td>4 回軸または 4̄ 軸が 1 本</td><td>a = b, α = β = γ = 90°</td></tr>
<tr><td rowspan="2">六方</td><td>三方晶系</td><td>3 回軸または 3̄ 軸が 1 本</td><td>六方軸で a = b, γ = 120°（hR は菱面体軸でも記述可）</td></tr>
<tr><td>六方晶系</td><td>6 回軸または 6̄ 軸が 1 本</td><td>a = b, γ = 120°</td></tr>
<tr><td>立方</td><td>立方晶系</td><td>体対角線方向の 3 回軸または 3̄ 軸が 4 本</td><td>a = b = c, α = β = γ = 90°</td></tr></table>
<p>逆向きは成り立たない。セルの形が条件を満たしていても、その回転軸がなければその晶系・晶族ではない（次の例）。</p>
<h2>同じ形のセルでも晶系が違う例</h2>
<figure>{SVG_RECT}<figcaption>左右とも同じ長方形のセル。分子が傾くと鏡映面が消え、2 回軸だけが残る（紙面に垂直な c 軸をとると単斜晶に相当）。右では γ = 90° は偶然で、温度などでずれうる（擬対称）。右の結晶は晶系・ブラベー格子の型（mP）・晶族のいずれも単斜であり、直方晶族ではない。γ = 90° は対称性から要求されない偶然の一致なので、分類には使わない。</figcaption></figure>
<h2>格子系：hP と hR</h2>
<figure>{SVG_LAT}<figcaption>hR では高さ 1/3, 2/3 に格子点が加わる。60° 回すと高さが合わないので 6 回軸は失われ、格子の対称は 3̄m に下がる。どの格子点も並進で重なるので、すべての格子点に 3 回軸がある。</figcaption></figure>
<h2>六角柱と単位胞（菱形柱）の関係</h2>
<p>六方格子を六角柱で描くことが多いが、格子を生み出しているのは菱形柱（単位胞）1 個の平行移動である。どの図も c 軸方向から見下ろしたもので、柱は紙面に垂直に伸びている。</p>
<figure>{TA}<figcaption>菱形はすべて同じ向き。紫の単位胞を a, b 方向に平行移動するだけで全体がすき間なく埋まる。</figcaption></figure>
<figure>{TB}<figcaption>六角柱は、中心の格子点を共有して 120° ずつ回した 3 つの菱形柱からなる。2 つ目と 3 つ目は 1 つ目を回転したもので、平行移動したものではない。6 回対称が見やすい「見せるための枠」であり、格子の単位胞ではない（蜂の巣状に並べるときの移動量は格子ベクトルより大きい）。</figcaption></figure>
<figure>{TC}{ZLEG}<figcaption>hR を六方軸の菱形柱（慣用セル）で敷き詰めた図。各菱形の内部に高さ 1/3 と 2/3 の格子点がある。格子点 1 個分の基本セルは菱面体（<a href="cells.html">慣用セルと基本セル</a> のページ）。</figcaption></figure>
<h2>晶系：同じ hP 格子で原子配置だけが違う例</h2>
<figure>{SVG_MOT}<figcaption>格子は同じ hP。原子が 6 回対称なら六方晶系、3 回対称なら三方晶系。α-石英は格子が hP で、結晶は三方晶系。</figcaption></figure>
<h2>晶族・ブラベー格子・晶系の対応と結晶の例</h2>
<p>教科書でいう「広義の六方格子」は晶族（crystal family）にあたる。晶族は 6 つで、ブラベー格子（14）と晶系（7）で分けると次のようになる。違いが出るのは六方晶族の中だけ。</p>
<table class="cls cls3"><tr><th>晶族</th><th>ブラベー格子</th><th>晶系</th><th>結晶の例（空間群）</th></tr>
<tr><td>三斜</td><td>aP</td><td>三斜晶系</td><td>硫酸銅五水和物 CuSO₄·5H₂O（P1̄）、藍晶石 Al₂SiO₅（P1̄）</td></tr>
<tr><td>単斜</td><td>mP</td><td>単斜晶系</td><td>単斜晶ジルコニア ZrO₂（P2₁/c）</td></tr>
<tr><td>単斜</td><td>mC</td><td>単斜晶系</td><td>石膏 CaSO₄·2H₂O（C2/c）</td></tr>
<tr><td>直方</td><td>oP</td><td>直方晶系</td><td>アラゴナイト CaCO₃（Pnma）</td></tr>
<tr><td>直方</td><td>oC</td><td>直方晶系</td><td>α-ガリウム（Cmce）、α-ウラン（Cmcm）</td></tr>
<tr><td>直方</td><td>oI</td><td>直方晶系</td><td>CeCu₂（Imma）</td></tr>
<tr><td>直方</td><td>oF</td><td>直方晶系</td><td>α-硫黄 S₈（Fddd）</td></tr>
<tr><td>正方</td><td>tP</td><td>正方晶系</td><td>ルチル TiO₂（P4₂/mnm）</td></tr>
<tr><td>正方</td><td>tI</td><td>正方晶系</td><td>アナターゼ TiO₂、β-スズ（I4₁/amd）</td></tr>
<tr><td><b>六方（広義）</b></td><td><b>hP</b></td><td><b>三方晶系</b></td><td>α-石英 SiO₂（P3₁21 / P3₂21）、テルル（P3₁21 / P3₂21）</td></tr>
<tr><td><b>六方（広義）</b></td><td><b>hP</b></td><td><b>六方晶系</b></td><td>マグネシウム（P6₃/mmc）、グラファイト（P6₃/mmc）、ウルツ鉱 ZnO（P6₃mc）</td></tr>
<tr><td><b>六方（広義）</b></td><td><b>hR</b></td><td><b>三方晶系</b></td><td>コランダム α-Al₂O₃（R3̄c）、方解石 CaCO₃（R3̄c）、ビスマス（R3̄m）</td></tr>
<tr><td><b>六方（広義）</b></td><td><b>hR</b></td><td><b>六方晶系</b></td><td>存在しない（R 格子は 6 回軸と両立しない）</td></tr>
<tr><td>立方</td><td>cP</td><td>立方晶系</td><td>塩化セシウム CsCl（Pm3̄m）、チタン酸ストロンチウム SrTiO₃（Pm3̄m）</td></tr>
<tr><td>立方</td><td>cI</td><td>立方晶系</td><td>α-鉄（Im3̄m）</td></tr>
<tr><td>立方</td><td>cF</td><td>立方晶系</td><td>銅、塩化ナトリウム NaCl（Fm3̄m）、ダイヤモンド、ケイ素（Fd3̄m）</td></tr></table>
<p>三方晶系は hP と hR の両方にまたがり、六方晶系は hP だけをとる。そのため晶族 6、晶系 7、ブラベー格子 14 と数が合わない。例は室温の相（SrTiO₃ などは低温で対称性が下がる）。α-石英とテルルは右手型・左手型で P3₁21 と P3₂21 の対になる。CeCu₂ の空間群は <a href="https://aflowlib.duke.edu/prototype-encyclopedia/AB2_oI12_74_e_h-001">AFLOW の結晶構造データベース</a> で確認。</p>''')

# 3D pages: reuse standalone files with nav + shared css
def adapt(src,dst,title):
    s=open(src,encoding='utf-8').read()
    s=s.replace('<head>','<head>\n<link rel="stylesheet" href="style.css">',1)
    s=re.sub(r'<title>.*?</title>',f'<title>{title}｜結晶の対称性と格子</title>',s)
    s=s.replace('<body>\n<main>','<body>\n'+nav(dst)+'\n<main>',1)
    assert nav(dst) in s
    open(dst,'w',encoding='utf-8').write(s)
adapt('src/3d/bravais_conventional_primitive.html','cells.html','慣用セルと基本セル')
adapt('src/3d/bravais_basis_vectors.html','basis-vectors.html','基底ベクトル')
print('built')
