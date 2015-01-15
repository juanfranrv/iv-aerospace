
import urllib
import cgi

from google.appengine.api import users
from google.appengine.ext import ndb

from google.appengine.ext.webapp.util import run_wsgi_app
import os
import webapp2
import jinja2
import feedparser
import random
import json

class ErrorPage(webapp2.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('template/error.html')
        self.response.write(template.render(template_values))
        
class MainPage(webapp2.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        rss = feedparser.parse('http://www.sondasespaciales.com/portada/feed/')
        
        titulos = []
        links = []
        descripciones = []
        
        for i in range (len(rss.entries)):

            titulos.append(rss.entries[i].title)
            links.append(rss.entries[i].link)
            descripcion = rss.entries[i].description
            descripciones.append(descripcion)
        
        template_values={'titulos':titulos, 'links':links, 'descripciones':descripciones}
        template = JINJA_ENVIRONMENT.get_template('template/index.html')
        self.response.write(template.render(template_values))
        
class InfoPage(webapp2.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('template/info_proyecto.html')
        self.response.write(template.render(template_values))
        
class FormularioRegistro(webapp2.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('template/registro.html')
        self.response.write(template.render(message=""))

class Usuario(ndb.Model):
    usuario = ndb.StringProperty()
    password = ndb.StringProperty()
    nombre = ndb.StringProperty()
    apellido = ndb.StringProperty()
    correo = ndb.StringProperty()
    telefono = ndb.StringProperty()

class registro_usuario(webapp2.RequestHandler):
    
    def post(self):
        user = Usuario()
        usu=self.request.get('usuario')
        result = Usuario.query(Usuario.usuario==usu)
        if result>0:
            self.response.headers['Content-Type'] = 'text/html'
            template = JINJA_ENVIRONMENT.get_template('template/registro.html')
            self.response.write(template.render(message="El usuario ya se encuentra registrado en la base de datos"))

        else:
            user.usuario = self.request.get('usuario')
            user.password = self.request.get('password')
            user.nombre = self.request.get('nombre')
            user.apellido = self.request.get('apellido')
            user.correo = self.request.get('correo')
            user.telefono = self.request.get('telefono')
                    
            user.put()
            
            self.redirect('/')


class consulta_usuario(webapp2.RequestHandler):
    def get(self):
        usuarios = []
        result = Usuario.query()
        for usuario in result:
            usuarios.append(usuario)
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {'usuarios':usuarios}
        template = JINJA_ENVIRONMENT.get_template('template/consulta_usuario.html')
        self.response.write(template.render(template_values))
        
        
class highchart(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        num = int(random.random()*30)
        template_values = {'num':num}
        template = JINJA_ENVIRONMENT.get_template('template/highchart.html')
        self.response.write(template.render(template_values))
        
class test(webapp2.RequestHandler):
    def get(self):
        num = int(random.random()*30)
        self.response.write(json.dumps(num))
        
class MainPageLoged(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        rss = feedparser.parse('http://www.sondasespaciales.com/portada/feed/')
        titulos = []
        links = []
        descripciones = []
        
        for i in range (len(rss.entries)):

            titulos.append(rss.entries[i].title)
            links.append(rss.entries[i].link)
            descripcion = rss.entries[i].description
            descripciones.append(descripcion)
        
        template_values={'titulos':titulos, 'links':links, 'descripciones':descripciones}
        template = JINJA_ENVIRONMENT.get_template('template/index_loged.html')
        self.response.write(template.render(template_values))
        
class TablaDatos(ndb.Model):
    temperatura = ndb.FloatProperty()
    velocidadViento = ndb.FloatProperty()
    direccionViento = ndb.StringProperty()
    racha = ndb.FloatProperty()
    direccionRacha = ndb.StringProperty()
    precipitacion = ndb.FloatProperty()
    presion = ndb.FloatProperty()
    tendencia = ndb.FloatProperty()
    humedad = ndb.FloatProperty()

class FormularioInsercion(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('template/insercion_datos.html')
        self.response.write(template.render(template_values))
 
class InsertarDatos(webapp2.RequestHandler):
    def post(self):
        
        datos = TablaDatos()
        datos.temperatura = float(self.request.get('temperatura'))
        datos.velocidadViento = float(self.request.get('velocidadViento'))
        datos.direccionViento = self.request.get('direccionViento')
        datos.racha = float(self.request.get('racha'))
        datos.direccionRacha = self.request.get('direccionRacha')
        datos.precipitacion = float(self.request.get('precipitacion'))
        datos.presion = float(self.request.get('presion'))
        datos.tendencia = float(self.request.get('tendencia'))
        datos.humedad = float(self.request.get('humedad'))
             
        datos.put()
            
        self.redirect('/listar')
        
class ListarDatos(webapp2.RequestHandler):
    def get(self):
        
        lista = TablaDatos.query()
        
        datos = []
         
        for dato in lista:
            datos.append(dato)
            
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('template/listar_datos.html')
        template_values={'datos':datos}
        self.response.write(template.render(template_values))
         
class mapa(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('template/mapa.html')
        self.response.write(template.render())
        
class coordenadas(webapp2.RequestHandler):
    def get(self):
        lat = random.random()*50
        lng = random.random()*150
        latLng = [lat, lng]
        self.response.write(json.dumps(latLng))
        
urls = [('/',MainPage),
        ('/error',ErrorPage),
        ('/registrarse',FormularioRegistro),
        ('/info_page',InfoPage),
        ('/reg_usuario', registro_usuario),
        ('/consulta_usuario', consulta_usuario),
        ('/highchart', highchart),
        ('/test', test),
        ('/loged', MainPageLoged),
        ('/formulario', FormularioInsercion),
        ('/guardarDatos', InsertarDatos),
        ('/listar', ListarDatos),
        ('/mapa', mapa),
        ('/coordenadas', coordenadas),
       ]
application = webapp2.WSGIApplication(urls, debug=True)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()