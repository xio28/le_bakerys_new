%include('header.tpl', title='Registro de usuario')
    <div class="item-background">
        <div class="container-register">
            <div class="form-title"><h2>Crear cuenta nueva</h2></div>
            <div class="form-item">
                <div class="left-content"></div>
                <div class="right-content">
                    <form action="/registro" method="POST" enctype="multipart/form-data" autocomplete="on">
                        <div class="fieldset-item">
                            <fieldset>
                                <legend>Datos de usuario:</legend>
                                <div class="form-content">
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-envelope"></i>{{ form.email }}
                                    </div>
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-lock"></i>{{ form.password }}
                                    </div>
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-lock"></i>{{ form.password_confirm }}
                                    </div>
                                    <div class="input-cont">
                                        <input id='file-reg' data-multiple-caption='{count} files selected' type="file" accept="image/png, image/jpg, image/jpeg" name="upload" value="upload">
                                        <label for="file-reg"><i class="file-icon fa-color fa fa-solid fa-upload"></i><span>Subir imagen</span></label>
                                    </div>
                                </div>
                            </fieldset>
                        </div>
                        <div class="fieldset-item">
                            <fieldset>
                                <legend>Datos personales:</legend>
                                <div class="form-content">
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-user"></i>{{ form.c_name }}
                                    </div>
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-user"></i>{{ form.surname1 }}
                                    </div>
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-user"></i>{{ form.surname2 }}
                                    </div>
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-address-card"></i>{{ form.nid }}
                                    </div>
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-phone"></i>{{ form.contact }}
                                    </div>
                                </div>
                            </fieldset>
                        </div>
                        <div class="fieldset-item">
                            <fieldset>
                                <legend>Dirección:</legend>
                                <div class="form-content">
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-address-book"></i>{{ form.address }}
                                    </div>
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-address-book"></i>{{ form.postal_code }}
                                    </div>
                                    <div class="input-cont">
                                        <i class="fa-color fa fa-solid fa-building"></i>{{ form.city }}
                                    </div>
                                </div>
                            </fieldset>
                        </div>
                        
                        <div class="check-item">
                            {{ form.privacy_policy }}
                            <a target="_blank" href="https://www.boe.es/buscar/doc.php?id=BOE-A-2018-16673">He leído los términos.</a>
                        </div>
                        <div class="buttons-item">
                            <a href="/" class="btn-cancel">Volver</a>
                            {{ form.save }}
                        </div>
                        <div class="return-login">
                            ¿Tienes cuenta?<a href="/login" class="btn-login">Entrar</a>
                        </div>
                    </form>
                </div>
            </div>
        </div> 
    </div>
%include('footer.tpl')
