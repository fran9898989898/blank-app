"""Barrido R 1-oct (candidatos por gasto y creativo en STT): tipos curados a mano sobre la Biblioteca (raw/*.json), precios.csv y ali.csv.
Genera tipos.csv y anuncios.json. Lo curado (qué dominios son del tipo, genérico elegido) está aquí, a la vista."""
import csv, json, os, sys, urllib.parse
sys.path.insert(0, 'tools')
from meta_library import pick, days_running

B = 'barridos/2026-10-01-R3'
ALI = {r['id']: r for f in ('ali.csv', 'ali2.csv') for r in csv.DictReader(open(f'{B}/{f}'))}

# raw = keyword guardada · doms = dominios que SÍ venden el tipo (redes gemelas unidas con +) · lider · rivales = precios leídos (precios.csv)
T = [
 dict(k='frying_pot', tipo='Olla de freír de acero con escurridor (tipo japonesa)', cat='Cocina', raw='frying_pot', persona='sí',
      doms=['pineapplea.com', 'clarioy.com', 'm.sakerplus.com', 'familygiftsale.com', 'tewvo.com', 'm.alessntials.com', 'shopellisellis.com', 'summarizei.com'], lider='m.sakerplus.com', stt_activos=None,
      rivales=[27.99, 34.99, 36.99], ali='3256809857842506', escalon='Base', falla='precio Ali de nuevo usuario ($6,33; tachado $20,88): si el real pasa de $8,30 deja de ser verde. Ellis (marca) la vende a $59,99',
      angulos=['Fritos crujientes sin llenar la cocina de aceite: freír, levantar, escurrir y verter en una sola olla (a quien fríe en casa y odia el desastre).',
               'La freidora de aire no fríe de verdad: esto sí, con 1/3 del aceite de una freidora.',
               'Termómetro + rejilla: el aceite a la temperatura justa sin adivinar (demo de alitas en 5 s).']),
 dict(k='stainless_steel_cutting_board', tipo='Tabla de cortar de acero inoxidable', cat='Cocina', raw='stainless_steel_cutting_board',
      doms=['londyx.com', 'getkant.shop', 'shoppurevo.com', 'luxelane.life', 'modernlivingco.us', 'ahlwoprime.com', 'm.sakerplus.com', 'allessya.com'], lider='luxelane.life', stt_activos=None,
      rivales=[29.99, 34.95], ali='3256806392706375', escalon='Escalón 1', falla='anuncio más antiguo 165 d (>120); mindsparkl lanzó 15+ anuncios hace 12 días (enjambre llegando); persona sin ver (el texto describe manos cortando)',
      angulos=['La tabla de madera guarda bacterias y olores: el acero se enjuaga en 10 segundos (demo con pollo crudo).',
               'No se raya, no se deforma, no huele: la última tabla que compras.',
               'Doble cara: acero para carne, la otra cara para verdura o masa.']),
 dict(k='bark_deterrent', tipo='Disuasor ultrasónico de ladridos', cat='Mascotas', raw='bark_deterrent',
      doms=['try.furrybasics.com+furrybasics.com', 'pawtique.co', 'yqyworkshop.com', 'convictioni.com+bestemall.com+onemartly.com', 'doggydior.store'], lider='try.furrybasics.com', stt_activos=None,
      rivales=[34.99, 39.99], ali='3256809902812909', escalon='Escalón 1 + 2', falla='solo 2 anunciantes con ≥21 d (FurryBasics 137 d, pawtique 150 d); 6 tiendas nuevas en <14 d',
      angulos=['El perro del vecino (o el tuyo) deja de ladrar sin collar ni descargas.', 'Pulsa y silencio: cartero, timbre, tele.', 'Paz con los vecinos antes de la queja.']),
 dict(k='christmas_projector', tipo='Proyector navideño HD (escenas en la pared)', cat='Hogar / Q4', raw='christmas_projector', persona='sí',
      doms=['propositik.com', 'ggvbeauty.com', 'noomoriey.com', 'gochicgolden.com', 'jovqelo.com', 'mindpagewise.com'], lider='gochicgolden.com', stt_activos=None,
      rivales=[25.99, 24.99, 24.99], ali='3256809548574579', escalon='Base', falla='landed 30 % y margen $9,7 a $25: solo sale si se vende a $35+',
      angulos=['Navidad en la pared en 10 segundos sin colgar luces.', 'Noche de peli navideña con los niños.', 'Regalo de $30 para Q4.']),
 dict(k='mini_steam_iron', tipo='Mini plancha de vapor portátil', cat='Hogar', raw='mini_steam_iron', persona='sí',
      doms=['clarioy.com', 'loribeaut.com', 'choosemuc.com'], lider='loribeaut.com', stt_activos=None,
      rivales=[29.99, 19.99, 33.99], ali='3256812845106910', escalon='Base', falla='genérico $15,51 (>$12); aparato de 110 V: enchufe y certificación a revisar',
      angulos=['Camisa arrugada lista en 60 s sin tabla.', 'Para viajes: cabe en la maleta.', 'Rota 90°: plancha en percha.']),
 dict(k='deshedding_tool', tipo='Cepillo deslanador para perro y gato', cat='Mascotas', raw='deshedding_tool', persona='sí',
      doms=['theorganicbunny.com', 'rhykin.com', 'dailyardsupply.com', 'mindsparkl.com+perpetualing.com', 'suzvo.com', 'thegiftnorth.com'], lider='rhykin.com', stt_activos=None,
      rivales=[29.00, 22.99, 23.99, 17.99], ali='3256808858899774', escalon='Fuera de filtro', falla='tipo con 532 d (evergreen) y marca de referencia FURminator en retail; margen $10',
      angulos=['—', '—', '—']),
]

def dom(a):
    link = pick(a, 'snapshot.linkUrl', 'snapshot.cards.0.linkUrl') or ''
    return urllib.parse.urlparse(link).netloc.lower().replace('www.', ''), link

filas, anuncios = [], {}
for t in T:
    ads = json.load(open(f"{B}/raw/{t['raw']}.json"))
    grupos = [set(g.split('+')) for g in t['doms']]
    per = {}
    for a in ads:
        d, _ = dom(a)
        for i, g in enumerate(grupos):
            if d in g:
                v = per.setdefault(i, {'dias': 0, 'n': 0}); v['dias'] = max(v['dias'], days_running(a) or 0); v['n'] += 1
    n21 = sum(1 for v in per.values() if v['dias'] >= 21)
    oldest = max((v['dias'] for v in per.values()), default=0)
    rel = t.get('rel')
    lid = [a for a in ads if dom(a)[0] == t['lider'] and (not rel or rel in json.dumps(a.get('snapshot') or {}).lower())]
    lid.sort(key=lambda a: -(days_running(a) or 0))
    top = []
    for a in lid[:3]:
        s = a.get('snapshot') or {}
        body = ((s.get('body') or {}).get('text') or ((s.get('cards') or [{}])[0].get('body') or '') or '').strip()
        first = body.replace('\n', ' ').split('. ')[0][:160]
        start = str(pick(a, 'startDateFormatted', 'startDate'))[:10]
        aid = str(pick(a, 'adArchiveID', 'adArchiveId') or '')
        fmt = (s.get('displayFormat') or '').upper()
        top.append({'inicio': start, 'dias': days_running(a) or 0, 'formato': {'VIDEO': 'vídeo', 'IMAGE': 'imagen', 'DCO': 'dinámico', 'CAROUSEL': 'carrusel', 'DPA': 'catálogo'}.get(fmt, fmt.lower() or '—'),
                    'frase': first, 'link': f'https://www.facebook.com/ads/library/?id={aid}', 'persona': t.get('persona', 'verificar')})
    al = ALI[t['ali']]
    pr = round(sum(t['rivales']) / len(t['rivales']), 2) if t['rivales'] else None
    ali = float(al['precio'] or 0)
    margen = round(pr - ali - 8, 2) if pr else None
    fila = dict(k=t['k'], tipo=t['tipo'], categoria=t['cat'], anunciantes_21d=n21, dias_mas_antiguo=oldest,
                lider=t['lider'], lider_anuncios_muestra=len(lid), lider_stt_activos=t['stt_activos'],
                precio_rivales=pr, precios_leidos=' / '.join(f'${p}' for p in t['rivales']) or 'no verificado',
                precio_ali=ali, ali_tachado=al['tachado'], ali_nuevo_usuario=al['precio_nuevo_usuario'], ali_vendidos=al['vendidos'], ali_titulo=al['titulo'],
                ali_url=al['url'], ali_foto=al['imagen'], landed_pct=round(100 * ali / pr) if pr else None,
                margen_bruto=margen, escalon=t['escalon'], falla=t['falla'])
    filas.append(fila); anuncios[t['k']] = {'top3': top, 'angulos': t['angulos']}

with open(f'{B}/tipos.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(filas[0])); w.writeheader(); w.writerows(filas)
json.dump({'tipos': filas, 'anuncios': anuncios}, open(f'{B}/anuncios.json', 'w'), ensure_ascii=False, indent=1)
for r in filas:
    print(r['k'], r['anunciantes_21d'], r['dias_mas_antiguo'], r['precio_rivales'], r['precio_ali'], r['landed_pct'], r['margen_bruto'], len(anuncios[r['k']]['top3']))
