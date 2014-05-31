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
        u'Queridos compañeros',
        u'Por otra parte, y dados los condicionamientos actuales',
        u'Asimismo,',
        u'Sin embargo no hemos de olvidar que',
        u'De igual manera,',
        u'La práctica de la vida cotidiana prueba que,',
        u'No es indispensable argumentar el peso y la significación de estos problemas ya que,',
        u'Las experiencias ricas y diversas muestran que,',
        u'El afán de organización, pero sobre todo',
        u'Los superiores principios ideológicos, condicionan que',
        u'Incluso, bien pudiéramos atrevernos a sugerir que',
        u'Es obvio señalar que,',
        u'Pero pecaríamos de insinceros si soslayásemos que,',
        u'Y además, quedaríamos inmersos en la más abyecta de las estulticias si no fueramos consacientes de que,',
        u'Por último, y como definitivo elemento esclarecedor, cabe añadir que,'
    ), (
        u'la realización de las premisas del programa',
        u'la complejidad de los estudios de los dirigentes',
        u'el aumento constante, en cantidad y en extensión, de nuestra actividad',
        u'la estructura actual de la organización',
        u'el nuevo modelo de actividad de la organización,',
        u'el desarrollo continuo de distintas formas de actividad',
        u'nuestra actividad de información y propaganda',
        u'el reforzamiento y desarrollo de las estructuras',
        u'la consulta con los numerosos militantes',
        u'el inicio de la acción general de formación de las actitudes',
        u'un relanzamiento específico de todos los sectores implicados',
        u'la superación de experiencias periclitadas',
        u'una aplicación indiscriminada de los factores confluyentes',
        u'la condición sine qua non rectora del proceso',
        u'el proceso consensuado de unas y otras aplicaciones concurrentes'
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
