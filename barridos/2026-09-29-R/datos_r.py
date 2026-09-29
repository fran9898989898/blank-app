"""Barrido R 29-sep: tipos curados a mano sobre la Biblioteca (raw/*.json), precios.csv y ali.csv.
Genera tipos.csv y anuncios.json. Lo curado (qué dominios son del tipo, genérico elegido) está aquí, a la vista."""
import csv, json, os, sys, urllib.parse
sys.path.insert(0, 'tools')
from meta_library import pick, days_running

B = 'barridos/2026-09-29-R'
ALI = {r['id']: r for r in csv.DictReader(open(f'{B}/ali.csv'))}

# raw = keyword guardada · doms = dominios que SÍ venden el tipo (redes gemelas unidas con +) · lider · rivales = precios leídos (precios.csv)
T = [
 dict(k='rain_catcher', tipo='Cadena de lluvia con pájaros (rain catcher)', cat='Jardín', raw='rain_catcher',
      doms=['dailyardmall.com+dailyardpro.com', 'accurateg.com', 'perpetualing.com'], lider='perpetualing.com', stt_activos=27,
      rivales=[25.99, 35.99], ali='3256811982331062', escalon='Base', falla='persona en pantalla sin verificar; precio Ali de nuevo usuario (no firme)',
      angulos=['Jardín vacío → jardín con pájaros: la lluvia llena los cuencos y los pájaros vuelven (a quien tiene jardín y comedero).',
               'Sustituto bonito del bajante feo: el agua baja cantando por la cadena en vez de por un tubo (a quien acaba de reformar la fachada).',
               'Regalo para madre/abuela jardinera en otoño: decoración que "trabaja" cuando llueve.']),
 dict(k='sheet_holder', tipo='Tensores de sábana (sheet holder straps)', cat='Hogar', raw='sheet_holder',
      doms=['shoppaya.com', 'beginnse.com', 'avocadobite.com', 'alaskatag.com', 'mindsparkl.com+wordmindglow.com+devmindglow.com'], lider='avocadobite.com', stt_activos=None,
      rivales=[12.95, 14.99, 29.99], ali='3256807605643524', escalon='Escalón 1 + 3', falla='antigüedad 123 d; ticket medio $19',
      angulos=['La bajera que se sale a las 3 de la mañana: un clip y la cama queda como de hotel (a quien tiene colchón grueso o topper).',
               'Cama hecha en 30 segundos: demo de antes/después con la sábana tirante (a padres con críticas de cama de niños).',
               'Pack 4+4 "uno por esquina de cada cama": vender el pack que nadie enseña.']),
 dict(k='hat_rack', tipo='Organizador de gorras de pared', cat='Organización', raw='hat_rack',
      doms=['viqzes.com', 'mindsparkl.com+bisnftwrem.com', 'm.lifesparking.com'], lider='mindsparkl.com', stt_activos=183,
      rivales=[15.90, 19.99], ali='3256809728547733', escalon='Escalón 3', falla='ticket $16–20 (<$20)',
      angulos=['Las gorras aplastadas en un montón: 10 gorras colgadas, visibles y sin deformarse (al coleccionista de gorras).',
               'Sin taladro: se pega en la puerta del armario en 10 segundos (a quien vive de alquiler).',
               'Regalo para él que "tiene de todo" pero tiene 30 gorras tiradas.']),
 dict(k='burner_covers', tipo='Protectores de quemadores de gas reutilizables', cat='Cocina', raw='burner_covers',
      doms=['thegiftnorth.com', 'glowsoftnook.com'], lider='glowsoftnook.com', stt_activos=None,
      rivales=[20.99], ali='3256807521722078', escalon='Escalón 2', falla='solo 2 anunciantes ≥21 d; precio de 1 rival',
      angulos=['Deja de frotar la placa cada día: se quita, se lava y la placa queda como nueva (a quien cocina a diario).',
               'Antes de devolver el piso de alquiler: protege la fianza (a inquilinos).',
               'Demo de grasa quemada saliendo en el fregadero en 5 s.']),
 dict(k='egg_opener', tipo='Abridor de huevos', cat='Cocina', raw='egg_opener',
      doms=['shopellox.com', 'pineapplea.com', 'focoor.com', 'yamloveme.com', 'thegiftnorth.com', 'mindsparkl.com+mindglowbook.com+bisnftwrem.com', 'kutaye.com'], lider='pineapplea.com', stt_activos=None,
      rivales=[9.98, 14.99, 17.99, 21.99], ali='3256806080339062', escalon='Escalón 1 + 3', falla='antigüedad 144 d; ticket medio $16; margen <$5',
      angulos=['Cero cáscaras en la masa: un clic y el huevo cae limpio (a quien hornea).',
               'Desayuno con niños: que casquen los huevos ellos sin desastre.',
               'Mano con artritis: abrir huevos sin fuerza (sin claim de salud: solo "sin esfuerzo").']),
 dict(k='hose_nozzle', tipo='Boquilla de manguera a presión giratoria', cat='Jardín / Coche', raw='hose_nozzle',
      doms=['bubblaz.com', 'feasiblte.com', 'propositik.com', 'zenblux.com', 'signaturte.com'], lider='zenblux.com', stt_activos=None,
      rivales=[], ali='3256811941398689', rel='nozzle', escalon='Base', falla='precio de rivales no verificado (tiendas no leídas)',
      angulos=['Hidrolimpiadora sin hidrolimpiadora: la manguera de siempre quita barro del coche (a quien lava el coche en casa).',
               'Patio verde de moho → piedra limpia en una pasada (antes/después en 5 s).',
               'La boquilla de plástico que se rompe cada verano vs. metal que dura.']),
 dict(k='leather_repair_patch', tipo='Parche autoadhesivo de cuero', cat='Hogar', raw='leather_repair_patch',
      doms=['zontinis.com', 'jetjetty.com', 'outwardsk.com', 'mindsparkl.com', 'aurorawyn.com'], lider='mindsparkl.com', stt_activos=153,
      rivales=[29.99], ali='3256808114686064', escalon='Fuera de filtro', falla='tipo con 894 d (evergreen) y 9 tiendas nuevas en <21 d: enjambre entrando',
      angulos=['No tires el sofá: cortar, pegar, presionar y el roto desaparece.',
               'Asiento del coche agrietado por $30 en vez de tapicero.',
               'Arañazos del gato en el sofá de piel.']),
 dict(k='back_seat_extender', tipo='Extensor de asiento trasero para perro (base rígida)', cat='Mascotas / Coche', raw='back_seat_extender',
      doms=['urbanpupgears.com+theluxepuppy.com', 'petsvetsupply.com', 'teamk9.com'], lider='urbanpupgears.com', stt_activos=None,
      rivales=[99.99, 119.99, 99.99], ali='3256810620250423', escalon='Fuera de filtro', falla='ticket $100–120 y genérico $41 (>$12)',
      angulos=['El perro grande que se cae al hueco del suelo en cada frenazo: base rígida = plataforma plana.',
               'Pelo y barro fuera del asiento en viajes largos.',
               'Kit completo "back-seat setup" (lo que venden los líderes).']),
 dict(k='exfoliating_glove', tipo='Guante exfoliante de ducha', cat='Baño / Belleza', raw='exfoliating_glove',
      doms=['nerra.com', 'cheekyglo.com', 'vistagood.com', 'koreic.com', 'wildpier.com'], lider='cheekyglo.com', stt_activos=None,
      rivales=[9.99, 23.00], ali='3256806810306410', escalon='Fuera de filtro', falla='tipo con 228 d; rivales con claims de piel (KP)',
      angulos=['Piel suave tras una ducha sin exfoliantes químicos (sin prometer curar nada).',
               'Antes del autobronceador: base uniforme.',
               'Adiós a la esponja que cría bacterias: se lava y se seca.']),
 dict(k='ice_cube_water_bottle', tipo='Botella que hace hielo (ice cube bottle)', cat='Cocina / Viaje', raw='ice_cube_water_bottle',
      doms=['shopmoderny.com'], lider='shopmoderny.com', stt_activos=73,
      rivales=[24.99], ali='3256811988063359', escalon='Fuera de filtro', falla='1 solo anunciante y su anuncio dice que cierra la colección (escasez)',
      angulos=['Hielo que cabe en la botella: cubos alargados listos al salir.',
               'Agua fría todo el día en el gimnasio.',
               'Congela, presiona, bebe: demo de 3 pasos.']),
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
