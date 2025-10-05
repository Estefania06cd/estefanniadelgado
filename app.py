from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
# ¡IMPORTANTE! Clave secreta para seguridad de Flask.
# Es necesario para usar sesiones o flash messages.
app.secret_key = 'CLAVE_SECRETA_PARA_FLASK_PROFESIONAL_MEDICINA' 

# Base de datos simulada (diccionario global) para guardar los datos entre la solicitud POST y el renderizado
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

MAX_SCORE_TEORICO = 22 # Puntuación máxima posible

# ----------------------------------------------------------------------------------
# FUNCIONES DE LÓGICA
# ----------------------------------------------------------------------------------

def calcular_puntuacion(respuestas):
    """Calcula la puntuación total del usuario basada en las respuestas."""
    puntuacion = 0
    
    for section_key in ['vocacion', 'valores']:
        for key, config in PREGUNTAS[section_key].items():
            if respuestas.get(key) == config['correcta']:
                puntuacion += config['puntos']

    for key, config in PREGUNTAS['rasgos'].items():
        respuesta_str = respuestas.get(key, '')
        if key == 'rasgo_org' and respuesta_str.isdigit() and int(respuesta_str) >= config['min_valor']:
            puntuacion += config['puntos']
        elif key == 'rasgo_critica' and respuesta_str == config['correcta']:
             puntuacion += config['puntos']
             
    if respuestas.get('hipo_triage') == PREGUNTAS['hipoteticas']['hipo_triage']['correcta']:
        puntuacion += PREGUNTAS['hipoteticas']['hipo_triage']['puntos']

    respuesta_proyecto = respuestas.get('proyecto_vida', '')
    if len(respuesta_proyecto.split()) >= PREGUNTAS['proyecto']['proyecto_vida']['min_palabras']:
         puntuacion += PREGUNTAS['proyecto']['proyecto_vida']['puntos']
            
    return puntuacion


# ----------------------------------------------------------------------------------
# RUTA PRINCIPAL (ÚNICA)
# ----------------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def home():
    """Ruta principal: maneja el formulario (GET) y procesa los datos (POST)."""
    if request.method == 'POST':
        global usuario_sesion
        
        # 1. Recuperar datos del formulario
        nombre_completo = request.form.get('nombre_usuario', 'Aspirante')
        carrera_deseada = request.form.get('carrera_deseada', 'Medicina General')
        
        # 2. Calcular el resultado
        puntuacion = calcular_puntuacion(request.form)
        
        # 3. Determinar el prefijo Dr./Dra.
        nombre_lower = nombre_completo.lower()
        if 'a' in nombre_lower[-1:] or 'maria' in nombre_lower or 'ana' in nombre_lower or 'eza' in nombre_lower:
            prefijo = "Dra."
        else:
            prefijo = "Dr."
            
        # 4. Renderizar index.html para mostrar los RESULTADOS
        # La variable 'mostrar_resultado=True' hace que index.html muestre la sección de resultados.
        return render_template('index.html', 
                               mostrar_resultado=True, 
                               nombre=nombre_completo, 
                               prefijo=prefijo, 
                               score=puntuacion, 
                               max_score=MAX_SCORE_TEORICO, 
                               carrera=carrera_deseada)
    
    # Si es GET, renderiza el FORMULARIO de inicio.
    # La variable 'mostrar_resultado=False' hace que index.html muestre la sección del formulario.
    return render_template('index.html', mostrar_resultado=False)


# ----------------------------------------------------------------------------------
# EJECUCIÓN (SOLO PARA DESARROLLO LOCAL)
# ----------------------------------------------------------------------------------

if __name__ == '__main__':
    # Esto solo se ejecuta cuando corres 'python app.py' en local
    app.run(debug=True)