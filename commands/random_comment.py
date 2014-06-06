# coding=utf-8

import re
import random
import hashlib

# Weight for sorting
weight = 10

trigger = hashlib.md5()
limit = 6 # 0 .. 16
responses = (
    (
        u'Que pedo cabrones',
        u'Que no mamen, que no ven como estamos?',
        u'También,',
        u'Pero no se te olvide que',
        u'Si wey,',
        u'Acuerdate como estabamos el otro día que,',
        u'Ya no te hagas bolas y no empieces con el circulo-chaquetero que,',
        u'La otra vez me acorde que,',
        u'Hay que armar algo no cren?, ademas,',
        u'No le pidas peras al olmo, que no vez que',
        u'Ademas, no empieces a suponer que',
        u'Eso es lo que diria un alt,',
        u'No mamen ya me hicieron dudar!!!,',
        u'Que pedo con esto, no se dejen llevar por el circulo chaquetero porque,',
        u'Mmmm... Aqui hace falta una referencia del TDS, o donde se ha visto que,'
    ), (
        u'la vez que andaba comentando bien pedo',
        u'Las burradas que se le ocurren a estos cabrones',
        u'las Alts estan aumentando y yo me estoy encabronando',
        u'la neta por eso estamos como estamos,
        u'pues a mi me late como esta el Sub eeh,',
        u'el ver cada cosa que suben al Sub esta chido',
        u'hay que hacer promocion del Sub no sean culeros',
        u'el que esté aqui no significa que voy a subir mamadas',
        u'para mi que este wey es un Alt',
        u'el día que este cabron diga algo coherente',
        u'un día de estos les voy a disparar una quesadilla con queso',
        u'la mamada que hizo este wey ya la olvide',
        u'una vez que este wey comienza',
        u'la condición es que este wey nos invite una chela',
        u'el comment de este wey hizo que se me antojara'
    ), (
        u'nos obliga a un exhaustivo análisis',
        u'cumple un rol escencial en la formación',
        u'exige la precisión y la determinación',
        u'ayuda a la preparación y a la realización',
        u'garantiza la participación de un grupo importante en la formación',
        u'cumple deberes importantes en la determinación',
        u'facilita la creación',
        u'obstaculiza la apreciación de la importancia',
        u'ofrece un ensayo interesante de verificación',
        u'implica el proceso de reestructuración y modernización',
        u'habrá de significar un auténtico y eficaz punto de partida',
        u'permite en todo caso explicitar las razones fundamentales',
        u'asegura, en todo caso, un proceso muy sensible de inversión',
        u'radica en una elaboración cuidadosa y sistemática de las estrategias adecuadas',
        u'deriva de una indirecta incidencia superadora'
    ), (
        u'de las condiciones financieras y administrativas existentes.',
        u'de las directivas de desarrollo para el futuro.',
        u'del sistema de participación general.',
        u'de las actitudes de los miembros hacia sus deberes ineludibles.',
        u'de las nuevas proposiciones.',
        u'de las direcciones educativas en el sentido del progreso.',
        u'del sistema de formación de cuadros que corresponda a las necesidades.',
        u'de las condiciones de las actividades apropiadas.',
        u'del modelo de desarrollo.',
        u'de las formas de acción.',
        u'de las básicas premisas adoptadas.',
        u'de toda una casuística de amplio espectro.',
        u'de los elementos generadores.',
        u'para configurar una interface amigable y coadyuvante a la reingeniería del sistema.',
        u'de toda una serie de criterios ideológicamente sistematizados en un frente común de actuación regeneradora.'
    )
)

def triggered_by (comment):
    trigger.update(comment.body)
    triggered = int('0x' + trigger.digest()[-1:], 0) <= limit
    return True if triggered and hasattr(comment, 'vote') else False

def run (comment):
    r = comment.reddit_session
    action = 'random comment'
    
    if comment.is_root:
        author = comment.submission.author.name.lower() if comment.submission else None
    else:
        #parent = r.get_submission(comment.permalink.replace(comment.id,comment.parent_id[3:]))
        parent = r.get_info(thing_id=comment.parent_id)
        author = parent.author.name.lower() if parent else None
    
    if author == r.user.name.lower():
        return action
    
    response = ''
    
    for section in responses:
        response += random.sample(section, 1)[0] + ' '
    
    comment.reply(response)
    r.log('%s :: Haciendo comentario a /u/%s' % (comment.permalink, comment.author.name if comment.author else '[deleted]'))
    action = 'random comment made'
    
    return action
