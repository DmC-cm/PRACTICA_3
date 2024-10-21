from flask import Flask,url_for,request,session,redirect,render_template

app=Flask(__name__)
app.secret_key="unaclavesecreta"

def generar_id():
    if 'registros' in session and len(session['registros'])>0:
        return max(item['id'] for item in session['registros'])+1
    else:
        return 1
    
@app.route("/")
def index():
    if 'registros' not in session:
        session['registros']=[]

    registros=session.get('registros',[])
    return render_template('index.html',registros=registros)

@app.route("/nuevo",methods=['GET','POST'])
def nuevo():
    if request.method=='POST':
        nombre=request.form['nombre']
        apellidos=request.form['apellidos']
        turno=request.form['turno']
        fecha=request.form['fecha']
        seminarios=request.form.getlist('seminarios')

        nuevo_registro={
            'id':generar_id(),
            'nombre':nombre,
            'apellidos':apellidos,
            'turno':turno,
            'fecha':fecha,
            'seminarios':seminarios
        }

        if 'registros' not in session:
            session['registros']=[]
        
        session['registros'].append(nuevo_registro)
        session.modified=True
        return redirect(url_for('index'))
    return render_template("nuevo.html")

@app.route("/editar/<int:id>",methods=['GET','POST'])
def editar(id):
    lista_r=session.get('registros',[])
    registro=next((c for c in lista_r if c['id']==id),None)
    if not registro:
        return redirect(url_for('index'))
    
    if request.method=='POST':
        registro['nombre']=request.form['nombre']
        registro['apellidos']=request.form['apellidos']
        registro['turno']=request.form['turno']
        registro['fecha']=request.form['fecha']
        registro['seminarios']=request.form.getlist('seminarios')
        session.modified=True
        return redirect(url_for('index'))
    return render_template('editar.html',registro=registro)

@app.route("/eliminar/<int:id>",methods=['GET','POST'])
def eliminar(id):
    lista_r=session.get('registros',[])
    registro=next((c for c in lista_r if c['id']==id),None)
    if registro:
        session['registros'].remove(registro)
        session.modified=True
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

