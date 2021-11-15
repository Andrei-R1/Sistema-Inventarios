from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/inventarios_andrei'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Item(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(30), nullable=False)
    codigo_identificacion=db.Column(db.Integer, nullable=False)
    precio=db.Column(db.Integer, nullable=False)
    categoria=db.Column(db.String(30), nullable=True)
    foto=db.Column(db.String(255), nullable=True)
    descripcion=db.Column(db.String(255), nullable=True)
    anotacion_gerente=db.Column(db.String(255), nullable=True)
    
    def __repr__(self) :
        return "[Item %s]" % str(self.id)
db.create_all()

class Empleado(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(30), nullable=False)
    codigo_identificacion=db.Column(db.Integer, nullable=False)
    puesto=db.Column(db.String(50), nullable=False)
    rol=db.Column(db.String(50), nullable=False)
    foto=db.Column(db.String(255), nullable=True)
    descripcion=db.Column(db.String(255), nullable=True)
    anotacion_gerente=db.Column(db.String(255), nullable=True)
    
    def __repr__(self) :
        return "[Empleado %s]" % str(self.id)
db.create_all()

class IndexRoute(Resource):
    def get(self):
        return {'response': 'Sistema de inventarios'},200

class IndexRouteItem(Resource):
    def get(self):
        items= Item.query.all()
        response=[]
        if items:
            for item in items:
                response.append({
                    "Id":item.id,
                    "Nombre":item.nombre,
                    "Codigo de Identificacion":item.codigo_identificacion,
                    "Precio":item.precio,
                    "Categoria":item.categoria,
                    "Foto":item.foto,
                    "Descripcion":item.descripcion,
                    "Anotacion Gerente":item.anotacion_gerente
                })
        return {'response':response},200

    def post(self):
        item_crear=request.get_json()
        if item_crear is None:
            return "Los campos no estan completos", 404
        if 'Nombre' not in item_crear:
            return 'Nombre no registrado',404
        if 'CodigoIdentificacion' not in item_crear:
            return 'Codigo de Identificacion no registrado', 404 
        if 'Precio' not in item_crear:
            return "Precio no registrado",404
        else:
            item = Item(nombre=item_crear['Nombre'], codigo_identificacion=item_crear['CodigoIdentificacion'], precio=item_crear['Precio'], categoria=item_crear['Categoria'],foto=item_crear['Foto'],descripcion=item_crear['Descripcion'],anotacion_gerente=item_crear['AnotacionGerente'] )
            db.session.add(item)
            db.session.commit()
        return {"response":"¡Item registrado exitosamente!"}, 200

class IndexRouteEmpleado(Resource):
    def get(self):
        empleados= Empleado.query.all()
        response=[]
        if empleados:
            for empleado in empleados:
                response.append({
                    "Id":empleado.id,
                    "Nombre":empleado.nombre,
                    "Codigo de Identificacion":empleado.codigo_identificacion,
                    "Puesto":empleado.puesto,
                    "Rol":empleado.rol,
                    "Foto":empleado.foto,
                    "Descripcion":empleado.descripcion,
                    "Anotacion Gerente":empleado.anotacion_gerente
                })
        return {'response':response},200

    def post(self):
        empleado_crear=request.get_json()
        if empleado_crear is None:
            return "Los campos no estan completos", 404
        if 'Nombre' not in empleado_crear:
            return 'Nombre no registrado',404
        if 'CodigoIdentificacion' not in empleado_crear:
            return 'Codigo de Identificacion no registrado', 404 
        if 'Puesto' not in empleado_crear:
            return "Puesto no registrado",404
        if 'Rol' not in empleado_crear:
            return "Rol no registrado",404
        else:
            empleado = Empleado(nombre=empleado_crear['Nombre'], codigo_identificacion=empleado_crear['CodigoIdentificacion'], puesto=empleado_crear['Puesto'], rol=empleado_crear['Rol'],foto=empleado_crear['Foto'],descripcion=empleado_crear['Descripcion'],anotacion_gerente=empleado_crear['AnotacionGerente'] )
            db.session.add(empleado)
            db.session.commit()
        return {"response":"¡Empleado registrado exitosamente!"}, 200

class ItembyID(Resource):
    def get(self,id):
        item=Item.query.filter_by(id=id).first()
        if item:
            return{'response':{
                "Id":item.id,
                "Nombre":item.nombre,
                "Codigo de Identificacion":item.codigo_identificacion,
                "Precio":item.precio,
                "Categoria":item.categoria,
                "Foto":item.foto,
                "Descripcion":item.descripcion,
                "Anotacion Gerente":item.anotacion_gerente
            }},200
        else:
            return{"response":"Id de Item no registrada"},404
    
    def put(self,id):
        item=Item.query.filter_by(id=id).first()
        if item:
            datos = request.get_json()
            item.nombre = datos['Nombre']
            item.codigo_identificacion = datos['CodigoIdentificacion']
            item.precio = datos['Precio']
            item.categoria =  datos['Categoria']
            item.foto = datos['Foto']
            item.descripcion = datos['Descripcion']
            db.session.commit()
            return {"response": "¡Item actualizado con exito!"}
        else:
            return{"response":"Datos no validos"},404


    def delete(self,id):
        item=Item.query.filter_by(id=id).first()
        db.session.delete(item)
        db.session.commit()
        if item:
            return { "response": "Item con Id: {item}. Borrado exitosamente.".format(item=id)}, 200
        else:
            return{"response":"Id de Item no registrada, no se puede borrar"},

class EmpleadobyID(Resource):
    def get(self,id):
        empleado=Empleado.query.filter_by(id=id).first()
        if empleado:
            return{'response':{
                "Id":empleado.id,
                "Nombre":empleado.nombre,
                "Codigo de Identificacion":empleado.codigo_identificacion,
                "Puesto":empleado.puesto,
                "Rol":empleado.rol,
                "Foto":empleado.foto,
                "Descripcion":empleado.descripcion,
                "Anotacion Gerente":empleado.anotacion_gerente
            }},200
        else:
            return{"response":"Id de Empleado no registrada"},404
    
    def put(self,id):
        empleado=Empleado.query.filter_by(id=id).first()
        if empleado:
            datos = request.get_json()
            empleado.nombre = datos['Nombre']
            empleado.codigo_identificacion = datos['CodigoIdentificacion']
            empleado.puesto = datos['Puesto']
            empleado.rol =  datos['Rol']
            empleado.foto = datos['Foto']
            empleado.descripcion = datos['Descripcion']
            db.session.commit()
            return {"response": "¡Empleado actualizado con exito!"}
        else:
            return{"response":"Datos no validos o el empleado no existe"},404


    def delete(self,id):
        empleado=Empleado.query.filter_by(id=id).first()
        db.session.delete(empleado)
        db.session.commit()
        if empleado:
            return { "response": "Empleado con Id: {empleado}. Borrado exitosamente.".format(empleado=id)}, 200
        else:
            return{"response":"Id de Empleado no registrada, no se puede borrar"}

api.add_resource(IndexRoute,'/')
api.add_resource(IndexRouteItem,'/item')
api.add_resource(IndexRouteEmpleado,'/empleado')
api.add_resource(ItembyID,'/item/<int:id>')
api.add_resource(EmpleadobyID,'/empleado/<int:id>')