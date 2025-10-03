from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Base de datos simulada para la sesión del usuario. 
# Usamos una variable global para este ejemplo simple.
usuario_sesion = {}

# Configuraciones de preguntas y lógica de puntuación
PREGUNTAS = {
    # Vocación y Motivación (6 preguntas, puntaje total 13 puntos)
    'vocacion': {
        'q1': {'correcta': 'c', 'puntos': 3},  # Aliviar el sufrimiento
        'q2': {'correcta': 'b', 'puntos': 2},  # Reflexiono para aprender
        'q3': {'correcta': '5', 'puntos': 2},  # Alta disposición al sacrificio (5)
        'q4': {'correcta': 'b', 'puntos': 1},  # Trabajar en equipo
        'q5': {'correcta': 'Si', 'puntos': 3}, # Ética ante el error
        'q6': {'correcta': 'Si', 'puntos': 2}, # Comodidad con fluidos/presión
    },
    # Valores y Ética (3 preguntas, puntaje total 6 puntos)
    'valores': {
        'q_val_1': {'correcta': 'b', 'puntos': 3}, # Respetar autonomía y dialogar
        'q_val_2': {'correcta': 'c', 'puntos': 2}, # Confrontar con tacto
        'q_val_3': {'correcta': 'c', 'puntos': 1}, # Empatía como valor crucial
    },
    # Rasgos Personales (2 preguntas, puntaje total 3 puntos)
    'rasgos': {
        'rasgo_org': {'min_valor': 4, 'puntos': 2}, # Metódico y excelente (4 o 5)
        'rasgo_critica': {'correcta': 'b', 'puntos': 1}, # Tomar crítica como mejora
    },
    # Situaciones Hipotéticas (1 pregunta, puntaje total 2 puntos)
    'hipoteticas': {
        'hipo_triage': {'correcta': 'B', 'puntos': 2}, # Anciano con dolor de pecho (Emergencia)
    },
    # Proyecto de Vida (1 pregunta, puntaje total 1 punto por longitud)
    'proyecto': {
        'proyecto_vida': {'min_palabras': 30, 'puntos': 1}, 
    }
}

# Calcular el puntaje máximo teórico
MAX_SCORE_TEORICO = sum(
    p.get('puntos', 0) for section in PREGUNTAS.values() for p in section.values()
)

@app.route('/', methods=['GET', 'POST'])
def home():
    """Ruta principal: maneja el registro y la presentación del examen."""
    if request.method == 'POST':
        global usuario_sesion
        
        # Almacenar datos de registro y todas las respuestas
        nombre_completo = request.form.get('nombre_usuario', 'Aspirante')
        carrera_deseada = request.form.get('carrera_deseada', 'Medicina General')
        
        usuario_sesion = {
            'nombre': nombre_completo,
            'carrera': carrera_deseada,
            'respuestas': request.form # Guarda todas las respuestas del formulario
        }
        
        puntuacion = calcular_puntuacion(usuario_sesion['respuestas'])
        
        return redirect(url_for('resultado', score=puntuacion))
    
    return render_template('home.html')

@app.route('/resultado/<int:score>')
def resultado(score):
    """Muestra la página de resultados finales."""
    # ¡CORRECCIÓN! El 'global' debe ir al principio de la función si se reasigna la variable.
    global usuario_sesion
    
    if not usuario_sesion:
        return redirect(url_for('home'))

    # Recuperar datos
    nombre = usuario_sesion.get('nombre', 'Aspirante')
    carrera = usuario_sesion.get('carrera', 'Medicina General')
    
    # Determinar el prefijo Dr./Dra.
    nombre_lower = nombre.lower()
    if 'a' in nombre_lower[-1:] or 'maria' in nombre_lower or 'ana' in nombre_lower or 'eza' in nombre_lower:
        prefijo = "Dra."
    else:
        prefijo = "Dr."

    # Limpiar la sesión
    usuario_sesion = {}
    
    return render_template('resultado.html', 
                           nombre=nombre, 
                           prefijo=prefijo, 
                           score=score, 
                           max_score=MAX_SCORE_TEORICO, 
                           carrera=carrera)

def calcular_puntuacion(respuestas):
    """Calcula la puntuación total del usuario basada en las respuestas."""
    puntuacion = 0
    
    # Lógica para preguntas de opción múltiple (Vocación y Valores)
    for section_key in ['vocacion', 'valores']:
        for key, config in PREGUNTAS[section_key].items():
            if respuestas.get(key) == config['correcta']:
                puntuacion += config['puntos']

    # Lógica para Rasgos Personales (Numéricos y Opción Múltiple)
    for key, config in PREGUNTAS['rasgos'].items():
        respuesta_str = respuestas.get(key, '')
        if key == 'rasgo_org' and respuesta_str.isdigit() and int(respuesta_str) >= config['min_valor']:
            puntuacion += config['puntos']
        elif key == 'rasgo_critica' and respuesta_str == config['correcta']:
             puntuacion += config['puntos']
             
    # Lógica para Situaciones Hipotéticas (Triage)
    if respuestas.get('hipo_triage') == PREGUNTAS['hipoteticas']['hipo_triage']['correcta']:
        puntuacion += PREGUNTAS['hipoteticas']['hipo_triage']['puntos']

    # Lógica para Proyecto de Vida (Punto por extensión)
    respuesta_proyecto = respuestas.get('proyecto_vida', '')
    if len(respuesta_proyecto.split()) >= PREGUNTAS['proyecto']['proyecto_vida']['min_palabras']:
         puntuacion += PREGUNTAS['proyecto']['proyecto_vida']['puntos']
            
    return puntuacion

if __name__ == '__main__':
    app.run(debug=True)