from flask import Flask, render_template, request, redirect, url_for, session
from data_manager import buscar_datos, df

app = Flask(__name__)
app.secret_key = 'aseg_clave_secreta'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('busqueda', '')
        mensaje, resultados_df = buscar_datos(query)
        
        session['res'] = resultados_df.to_dict('records') if resultados_df is not None else None
        session['msg'] = mensaje
        return redirect(url_for('index'))

    resultados = session.pop('res', None)
    mensaje = session.pop('msg', None)
    return render_template('index.html', resultados=resultados, mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)
