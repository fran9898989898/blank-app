"""Barrido R fitness en casa 30-sep: tipos curados a mano sobre la Biblioteca (raw/*.json), precios.csv y ali.csv.
Genera tipos.csv y anuncios.json. Lo curado (qué dominios son del tipo, genérico elegido) está aquí, a la vista."""
import csv, json, os, sys, urllib.parse
sys.path.insert(0, 'tools')
from meta_library import pick, days_running

B = 'barridos/2026-09-30-R-fitness'
ALI = {r['id']: r for r in csv.DictReader(open(f'{B}/ali.csv'))}

# raw = keyword guardada · doms = dominios que SÍ venden el tipo (redes gemelas unidas con +) · lider · rivales = precios leídos (precios.csv)
T = [
 dict(k='push_up_board', tipo='Tabla de flexiones plegable (push-up board)', cat='Fuerza', raw='push_up_board',
      doms=['formafitness.co', 'advancetell.com', 'clingman.co', 'm.alessntials.com', 'colody.com'], lider='formafitness.co', stt_activos=None,
      rivales=[59.99, 49.99, 27.00], ali='3256808243818458', escalon='Escalón 1', falla='anuncio más antiguo 148 d; genérico $12,66 (roza el tope de $12, precio de nuevo usuario); un rival usa claim corporal ("man boobs")',
      angulos=['Gimnasio de pecho en 60 cm: la tabla dice dónde poner las manos para pecho, hombro o tríceps (al que entrena en casa sin pesas).',
               'Flexiones que de verdad cuentan: colores = rutina guiada de 20 minutos.',
               'Regalo para él de $40 que no necesita espacio (Q4).']),
 dict(k='pedal_resistance_band', tipo='Banda elástica de pedal (4–6 tubos)', cat='Tonificación', raw='pedal_resistance_band',
      doms=['gentlegains.com', 'cozyhoome.com+shopellox.com', 'wordmindglow.com+feasiblte.com+booksoftmind.com+zenblux.com'], lider='gentlegains.com', stt_activos=None,
      rivales=[54.99, 12.95], ali='3256811754873752', escalon='Escalón 1', falla='anuncio más antiguo 163 d; precios de rivales dispares ($13 vs $55); copys con "slimming" (claim a evitar)',
      angulos=['Entrenar de cuerpo entero en el salón con una sola pieza que cabe en un cajón (a mujeres 40+ que no van al gimnasio).',
               'Sustituto de 4 aparatos: remo, bíceps, abdominales y piernas con la misma banda.',
               'Rutina de 10 minutos viendo la tele (testimonio en primera persona, sin prometer kilos).']),
 dict(k='pilates_ring', tipo='Aro de pilates', cat='Pilates', raw='pilates_ring',
      doms=['wondeea.com+housewor.com+ancienflow.com+forttender.com', 'rouvenor.com', 'sqzwellness.com'], lider='forttender.com', stt_activos=None,
      rivales=[29.98, 39.99, 89.00], ali='3256809462963347', escalon='Fuera de filtro', falla='anuncio más antiguo 266 d (>180): tipo ya maduro',
      angulos=['Pilates de estudio en casa por el precio de una clase.', 'Suelo pélvico y core tras el embarazo (sin claim médico).', 'Kit aro + pelota como regalo.']),
 dict(k='grip_strengthener', tipo='Fortalecedor de agarre (hand gripper)', cat='Fuerza', raw='grip_strengthener',
      doms=['culmenwild.com', 'spainho.com', 'm.sakerplus.com'], lider='culmenwild.com', stt_activos=None,
      rivales=[], ali='3256806220927618', escalon='Fuera de filtro', falla='0 anunciantes con ≥21 d (solo tiendas nuevas y Amazon); precio de rivales no verificado',
      angulos=['Antebrazos de escalador en 5 minutos al día.', 'Contador electrónico: gamifica el agarre.', 'Regalo de escritorio para él.']),
 dict(k='pilates_bar', tipo='Barra de pilates con bandas', cat='Pilates', raw='pilates_bar',
      doms=['stretchedfusion.com', 'lulupassion.com'], lider='stretchedfusion.com', stt_activos=None,
      rivales=[49.99, 69.99], ali='3256812784473837', escalon='Fuera de filtro', falla='1 marca dominante (stretchedfusion, 375 d); el resto <21 d',
      angulos=['Reformer de pilates que se guarda debajo de la cama.', 'Entrenamiento de cuerpo entero en 20 min.', 'Alternativa a $200/mes de estudio.']),
 dict(k='ab_roller', tipo='Rueda abdominal (ab roller)', cat='Core', raw='ab_roller',
      doms=['postureflex.co+try.postureflex.co+30daychallenge.postureflex.co', 'homefitnesslab.co'], lider='postureflex.co', stt_activos=None,
      rivales=[89.99, 89.00], ali='3256812781512050', escalon='Fuera de filtro', falla='2 marcas, 295 d; se vende a $89 un genérico de $13 con claims de barriga ("men 30+")',
      angulos=['Reto de 30 días para hombres 30+ (ángulo del líder, sin prometer kilos).', 'Core sin gimnasio en 5 minutos.', 'Rueda con rebote para principiantes.']),
 dict(k='pull_up_bar', tipo='Barra de dominadas portátil / de puerta', cat='Fuerza', raw='pull_up_bar',
      doms=['jayflexfitness.com', 'bullbarfit.com'], lider='jayflexfitness.com', stt_activos=None,
      rivales=[], ali='3256812729197492', escalon='Fuera de filtro', falla='2 anunciantes, 509 d; precio de barra de puerta no verificado (el único leído, $399, es una estación de dominadas)',
      angulos=['Dominadas sin taladrar.', 'Barra de puerta que no marca el marco.', 'Plan de 0 a 10 dominadas.']),
 dict(k='jump_rope', tipo='Comba con peso', cat='Cardio', raw='jump_rope',
      doms=['elitejumps.co', 'boxeliteclub.com', 'swissskip.ch', 'crossrope.com', 'yokkao.com'], lider='swissskip.ch', stt_activos=None,
      rivales=[65.99], ali='3256809062699452', escalon='Fuera de filtro', falla='mercado de marcas (Crossrope, Elite Jumps) con 145–348 d',
      angulos=['Cardio de boxeador en 10 minutos.', 'Comba con peso = cardio + brazos.', 'Kit progresión para principiantes.']),
 dict(k='suspension_trainer', tipo='Cintas de suspensión (tipo TRX)', cat='Fuerza', raw='suspension_trainer',
      doms=['trxtraining.com', 'bellsofsteel.us'], lider='trxtraining.com', stt_activos=None,
      rivales=[], ali='3256811866500219', escalon='Fuera de filtro', falla='marca de referencia TRX; precio de rivales no verificado',
      angulos=['Un gimnasio en dos cintas colgadas de la puerta.', 'Entrenar en viajes.', 'Rutinas de peso corporal guiadas.']),
 dict(k='weighted_hula_hoop', tipo='Hula hoop con peso (smart hoop)', cat='Cardio', raw='weighted_hula_hoop',
      doms=['infinityhoop.com'], lider='infinityhoop.com', stt_activos=None,
      rivales=[59.99], ali='3256806528084929', escalon='Fuera de filtro', falla='1 solo anunciante y todo el ángulo es pérdida de peso (claim prohibido en el filtro)',
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
                    'frase': first, 'link': f'https://www.facebook.com/ads/library/?id={aid}', 'persona': 'verificar'})
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
