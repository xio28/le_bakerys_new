from bottle import (auth_basic, debug, error, route, get, post, redirect, request,
                    route, run, static_file, template)

from controller.register import RegistrationForm
from controller.contact import ContactForm
from controller.add_employees import AddEmpForm
from controller.add_products import AddProdForm
from controller.chang_pass import ChangePassForm
from controller.login import LogInForm
from model.productos import *
from model.usuarios import *
from model.modules import *
from model.carrito import *
from model.pedidos import *
from model.compras import *


@route('/')
@route('/index')
def index():
    return static_file("index.html", root ="static")

@get('/login')
def login():
    form = LogInForm(request.POST)
    return template('login', form=form)
    
@post('/login')
def post_login():
    form = LogInForm(request.POST)
    if Clientes.user_logged():
        return redirect('/cliente')
    else:
        if form.save.data and Usuarios.check_credentials(form.email.data, form.password.data):
            Clientes.user_log(form.email.data)
            return redirect('/')
        
        return redirect('/login')

        # return template('login', form=form)

@post('/logout')
def post_login():
    Modules.write_config({'user_email': 0, 'user_id':0})
    return redirect('/')


@get('/admin')
@auth_basic(Modules.auth_admin)
def admin_panel():
    formEmp = AddEmpForm(request.POST)
    formPro = AddProdForm(request.POST)
    
    return template('admin_panel', formEmp=formEmp, formPro=formPro, odrows=Pedidos.inner_pedido(),  prows=Productos.select(), incrows=Clientes.inner_cliente(), inerows=Empleados.inner_empleado())

@get('/cliente')
def panel():
    if Usuarios.user_logged():
        form = ChangePassForm(request.POST)
        return template('client_panel', form=form)
        
    return redirect('/login')

@post('/admin')
def add_item():
    form_emp = AddEmpForm(request.POST)
    form_pro = AddProdForm(request.POST)
    root = '/static/resources/img/upload/users'

    if form_emp.save_emp.data and form_emp.validate():
        upload = request.POST.get('upload')
        print(upload)
        print("entre")

        if upload.filename != "empty":
            img = Upload.save_img(root, upload, form_emp.e_name.data)
        else:
            img = os.path.join(root, 'default.png')

        d_form_user = {
            'Email': form_emp.email.data,
            'Password': form_emp.password.data,
            'Nombre': form_emp.e_name.data,
            'Apellido1': form_emp.surname1.data,
            'Apellido2': form_emp.surname2.data,
            'Imagen': img
        }

        print(d_form_user)

        d_form_emp = {
            'Email': form_emp.email.data
        }

        Usuarios.insert(d_form_user)
        Empleados.insert(d_form_emp)

    elif form_pro.save_emp.data and form_pro.validate():
        upload = request.POST.get('upload')
        print(type(upload))

        if upload.filename != "empty":
            img = Upload.save_img(root, upload, form_pro.pro_name.data)
        else:
            img = os.path.join(root, 'default.png')

        d_form_pro = {
            'Producto': form_pro.pro_name.data,
            'Precio': form_pro.price.data,
            'Categoria': form_pro.category.data,
            'Stock': form_pro.stock.data,
            'Imagen': img
        }

        print(d_form_pro)

        Productos.insert(d_form_pro)

    return redirect("/admin")

@post('/delete/<no:int>')
def delete_item(no):
    
    if request.POST.delete_pro:
        where = {'ID': no}
        Productos.delete(where)
    elif request.POST.delete_ord:
        where = {'ID': no}
        Productos.delete(where)

    # return redirect('/')

@get('/cliente')
def client_panel():
    form = ChangePassForm(request.POST)
    return template('client_panel', form=form)

@get('/registro')
def register():
    form = RegistrationForm(request.POST)
    return template('registration', form=form)

@post('/registro')
def post_registration():
    form = RegistrationForm(request.POST)
    root = '/static/resources/img/upload/users' # si es para users si no pones products

    if form.save.data and form.validate():
        upload = request.POST.get('upload')
        print(upload)

        if upload.filename != "empty":
            img = Upload.save_img(root, upload, form.c_name.data)
        else:
            img = os.path.join(root, 'default.png')

        form_user = {
            'Email': form.email.data,
            'Password': form.password.data,
            'Nombre': form.c_name.data,
            'Apellido1': form.surname1.data,
            'Apellido2': form.surname2.data,
            'Imagen': img
        }

        form_client = {
            'Email': form.email.data,
            'NIF': form.nid.data,
            'Contacto': form.contact.data,
            'Calle': form.address.data,
            'Codigo_Postal': form.postal_code.data,
            'Ciudad': form.city.data
        }

        Usuarios.insert(form_user)
        Clientes.insert(form_client)

    return redirect('/')

@get('/contacto')
def contact():
    form = ContactForm(request.POST)    
    if form.save.data:
        f = request.files['user_image']
    return template('contact', form=form)

@post('/contacto')
def post_contact():
    form = ContactForm(request.POST)
    
    return redirect('/')

@get("/social")
def social():
    return template("social")

@get('/productos')
def products():
    count_products = Carrito.get_select(['Count(IdProducto)'], {'IdCliente' : Modules.load_session().get('user_id')})
    products_list = Productos.select()
    return template("products", products_list=products_list, count_products=count_products)

@post('/productos')
def filter():
    if request.POST.get('todos'):
        return redirect('/productos')

    else:
        if request.POST.get('tartas'):
            category = 'Tartas'

        elif request.POST.get('helados'):
            category = 'Helados'

        elif request.POST.get('dulces'):
            category = 'Dulces'

        elif request.POST.get('salados'):
                category = 'Salados'

        products_list = Productos.get_select(['*'], {'Categoria' : category})
        count_products = Carrito.get_select(['Count(IdProducto)'], {'IdCliente' : Modules.load_session().get('user_id')})
        return template("products", products_list = products_list, count_products=count_products)

# @get('/carrito')
# def carrito():
#     id_client = Modules.load_session().get('user_id')
#     datas = Carrito.inner_carrito(Modules.load_session().get('user_id'))
#     total = Carrito.get_total(id_client)[0][0]
#     return template('carrito', datas = datas, total=total)

@post('/productos')
def filter():
    if request.POST.get('todos'):
        return redirect('/productos')

    else:
        if request.POST.get('tartas'):
            category = 'Tartas'

        elif request.POST.get('helados'):
            category = 'Helados'

        elif request.POST.get('dulces'):
            category = 'Dulces'

        elif request.POST.get('salados'):
                category = 'Salados'

        products_list = Productos.get_select(['*'], {'Categoria' : category})
        count_products = Carrito.get_select(['Count(IdProducto)'], {'IdCliente' : Modules.load_session().get('user_id')})
        return template("products", products_list = products_list, count_products=count_products)

@get('/carrito')
def carrito():
    id_client = Modules.load_session().get('user_id')
    datas = Carrito.inner_carrito(Modules.load_session().get('user_id'))
    total = Carrito.get_total(id_client)[0][0]
    return template('carrito', datas=datas, total=total)


@post('/carrito/<id_product>')
def add_carrito(id_product):
    id_client = Modules.load_session().get('user_id')

    if Clientes.user_logged():
        if request.POST.get('add_product'):
            if not Carrito.shoplist_check(id_product, id_client):
                data = {
                    'IdProducto' : id_product,
                    'IdCliente' : id_client
                }

                client_id = Modules.load_session().get('user_id')
                Carrito.insert(data)

        elif request.POST.get('remove_one'):
            Carrito.edit_unity(id_product, id_client, "remove")
            return redirect('/carrito')

        elif request.POST.get('add_one'):
            Carrito.edit_unity(id_product, id_client, "add")
            return redirect('/carrito')

    return redirect('/productos')

@post('/pedido')
def order():
    id_client = Modules.load_session().get('user_id')
    if request.POST.get('submit-order'):
        Pedidos.do_order(id_client)

    return redirect('/productos')

def order():
    id_client = Modules.load_session().get('user_id')
    if request.POST.get('submit-order'):
        Pedidos.do_order(id_client)
    
    return redirect('/productos')

@error(404)
def error404(error):
    return static_file('404.html', root='static/src')

@get('/test')
def test():
    #return f'{Pedidos.select()}'
    return f'{Pedidos.gen_order_id()}'
    
# Static Routes
@get("/static/styles/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static/styles")

@get("/static/fonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="static/fonts")

@get("/static/resources/img/<filepath:re:.*\.(jpg|png|gif|ico|svg|jpeg|webp)>")
def img(filepath):
    return static_file(filepath, root="static/resources/img")

@get("/static/resources/video/<filepath:re:.*\.mp4>")
def video(filepath):
    return static_file(filepath, root="static/resources/video")

@get("/static/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="static/js")

@get("/static/src/<filepath:re:.*\.html>")
def src(filepath):
    return static_file(filepath, root="static/src")


@get("/static/src/<filepath:re:.*.html>")
def src(filepath):
    return static_file(filepath, root="static/src")

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
