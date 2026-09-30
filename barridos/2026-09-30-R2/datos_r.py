"""Barrido R 30-sep (2º general): tipos curados a mano sobre la Biblioteca (raw/*.json), precios.csv y ali.csv.
Genera tipos.csv y anuncios.json. Lo curado (qué dominios son del tipo, genérico elegido) está aquí, a la vista."""
import csv, json, os, sys, urllib.parse
sys.path.insert(0, 'tools')
from meta_library import pick, days_running

B = 'barridos/2026-09-30-R2'
ALI = {r['id']: r for r in csv.DictReader(open(f'{B}/ali.csv'))}

# raw = keyword guardada · doms = dominios que SÍ venden el tipo (redes gemelas unidas con +) · lider · rivales = precios leídos (precios.csv)
T = [
 dict(k='heatless_curls', tipo='Rulo sin calor (heatless curling rod)', cat='Belleza', raw='heatless_curls',
      doms=['cozyconfidence.com', 'thesleepytie.com', 'mykitsch.com', 'm.eigoods.com'], lider='thesleepytie.com', stt_activos=None,
      rivales=[28.00, 32.99], ali='3256810467119627', escalon='Base', falla='persona sin verificar; en el tipo anuncia Kitsch, marca que vende en retail (no verificado en esta sesión)',
      angulos=['Rizos de peluquería al despertar sin plancha: te lo pones al acostarte y te lo quitas por la mañana (a mujeres con pelo largo que evitan el calor).',
               'Cero pelo quemado: el mismo rizo que con la tenacilla sin dañar el pelo (sin prometer "reparar").',
               'Pack de 2 (uno para ti y otro para regalar): la marca no lo ofrece.']),
 dict(k='grout_pen', tipo='Rotulador para juntas de azulejo (grout pen)', cat='Baño / Limpieza', raw='grout_pen',
      doms=['dailyardmall.com+dailyardpro.com', 'pineapplea.com', 'mytrendyes.com', 'makdledge.com', 'mindsparkl.com+bisnftwrem.com+perpetualing.com+mindpagewise.com', 'kariney.com'], lider='dailyardmall.com', stt_activos=None,
      rivales=[12.99, 11.99, 15.99, 22.99, 15.99], ali='3256807911692278', escalon='Escalón 3', falla='ticket medio $16; enjambre de tiendas-catálogo; commodity de ferretería',
      angulos=['Juntas negras → blancas en 1 minuto sin frotar: antes/después en el mismo plano.',
               'Antes de vender o devolver el piso: el baño parece reformado por $20.',
               'Pack 3 colores (blanco, gris, negro) para baño y cocina.']),
 dict(k='bumper_repair', tipo='Adhesivo para reparar parachoques', cat='Coche', raw='bumper_repair',
      doms=['copenrain.com', 'paintapart.com', 'thegiftnorth.com', 'moonighty.com'], lider='thegiftnorth.com', stt_activos=None,
      rivales=[19.99, 12.99, 15.99], ali='3256811596315988', escalon='Escalón 3', falla='ticket medio $16; paintapart vende otro producto (kit de pintura); mismo texto de proveedor en 3 tiendas',
      angulos=['Parachoques suelto o rajado: arreglado en casa sin taller.', 'El taller pide $400; esto cuesta $20.', 'Demo: grieta → presión → seco en minutos.']),
 dict(k='mandala_light', tipo='Lámpara solar con proyección mandala', cat='Jardín', raw='mandala_light',
      doms=['reemoreemoo.com', 'flowarmth.com+forttender.com+blissorin.com+bestemall.com', 'mindsparkl.com+bisnftwrem.com', 'pvzxr.com'], lider='mindsparkl.com', stt_activos=None,
      rivales=[16.99, 18.90, 16.99], ali='3256812148154543', escalon='Escalón 1 + 3', falla='127 d; ticket $17–19; redes de tiendas-catálogo',
      angulos=['El patio oscuro se convierte en un patio con encanto sin cables.', 'Solar: cero factura de luz.', 'Regalo de decoración de otoño para jardín.']),
 dict(k='tire_valve_caps', tipo='Tapones de válvula LED / fluorescentes', cat='Coche', raw='tire_valve_caps',
      doms=['autoyunn.com', 'thegiftnorth.com', 'wordmindglow.com+interestcen.com', 'carsfanatics.store'], lider='thegiftnorth.com', stt_activos=None,
      rivales=[12.95, 19.48], ali='3256806807860632', escalon='Escalón 1 + 3', falla='132 d; ticket $13–19; commodity de $2',
      angulos=['Ruedas que brillan de noche en 3 segundos.', 'Se ven los tapones en el aparcamiento oscuro.', 'Regalo barato para el que tunea el coche.']),
 dict(k='scratch_remover', tipo='Quitarrayones para coche', cat='Coche', raw='scratch_remover',
      doms=['carfidant.com', 'try.nexa-us.com+go.primecell-us.com', 'lyseemin.com', 'exoforma.com', 'getfixapro.com', 'colody.com'], lider='try.nexa-us.com', stt_activos=None,
      rivales=[12.00, 19.99], ali='3256811827538144', escalon='Fuera de filtro', falla='tipo con 200 d (>180) y 6 anunciantes: maduro',
      angulos=['—', '—', '—']),
 dict(k='hair_towel_wrap', tipo='Toalla turbante para el pelo', cat='Belleza', raw='hair_towel_wrap',
      doms=['mykitsch.com', 'm.shein.com'], lider='mykitsch.com', stt_activos=None,
      rivales=[], ali='3256809274325275', escalon='Fuera de filtro', falla='solo marcas y SHEIN; precio del tipo no verificado',
      angulos=['—', '—', '—']),
 dict(k='ice_roller', tipo='Rodillo de hielo facial', cat='Belleza', raw='ice_roller',
      doms=['shopskinnyconfidential.com', 'nurtured9.com'], lider='shopskinnyconfidential.com', stt_activos=None,
      rivales=[79.00], ali='3256810467019956', escalon='Fuera de filtro', falla='marcas; el ángulo del tipo es "deshinchar" (claim de piel)',
      angulos=['—', '—', '—']),
 dict(k='wall_sconces', tipo='Apliques de pared inalámbricos', cat='Hogar', raw='wall_sconces',
      doms=['pridola.co'], lider='pridola.co', stt_activos=None,
      rivales=[59.99], ali='3256808032532896', escalon='Fuera de filtro', falla='1 anunciante (pridola, 189 d); genérico $22,57 (>$12)',
      angulos=['—', '—', '—']),
 dict(k='diamond_painting', tipo='Kits de diamond painting', cat='Manualidades', raw='diamond_painting',
      doms=['diamondartclub.com', 'ecoolbuy.com', 'diamondartpaintin.com', 'madewithdiamonds.com', 'diamondartfactory.com', 'dpover.com', 'craft-hub.com'], lider='diamondartclub.com', stt_activos=None,
      rivales=[], ali='3256810190161494', escalon='Fuera de filtro', falla='marcas con 143–1.939 d; cientos de diseños (no son 1–3 variantes)',
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
