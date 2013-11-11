from flask import Blueprint
from flask.ext.babel import lazy_gettext
from flask.ext.babel import gettext as _gettext
from .security.views import AuthView, ResetPasswordView, UserGeneralView, RoleGeneralView, PermissionViewGeneralView, ViewMenuGeneralView, PermissionGeneralView, IndexView, PermissionView
from .babel.views import LocaleView


class BaseApp():

    lst_baseview = []
    app = None
    menu = None
    app_name = ""
    indexview = None
    
    languages = None
    admin = None
    _gettext = _gettext

    """
    ------------------------------------
                 INIT
     Add menu with categories inserted
    #-----------------------------------
    """
    def __init__(self, app, menu, indexview = None):
        self.menu = menu
        self.app = app
        self.app_name = app.config['APP_NAME']
        self.app_theme = app.config['APP_THEME']
        self.languages = app.config['LANGUAGES']
        self.indexview = indexview or IndexView
        self._add_admin_views()

    def _add_admin_views(self):
        self.add_view_no_menu(self.indexview)
        self.add_view_no_menu(LocaleView)
        self.add_view_no_menu(AuthView)
        self.add_view_no_menu(ResetPasswordView)

        self.add_view(UserGeneralView, "List Users"
                                        ,"/users/list","user",
                                        "Security")
        self.add_view(RoleGeneralView, "List Roles","/roles/list","tags","Security")
        self.menu.add_separator("Security")
        self.add_view(PermissionViewGeneralView, "Base Permissions","/permissions/list","lock","Security")
        self.add_view(ViewMenuGeneralView, "Views/Menus","/viewmenus/list","list-alt","Security")
        self.add_view(PermissionGeneralView, "Permission on Views/Menus","/permissionviews/list","lock","Security")
	self.admin = Blueprint('admin', __name__, static_folder='static')


    def add_view(self, baseview, name, href, icon, category):
        print "Registering:", category,".", name, "at", href
        self.menu.add_link(name, href, icon, category)
        if baseview not in self.lst_baseview:
            baseview.baseapp = self
            self.lst_baseview.append(baseview)
            self.register_blueprint(baseview)
            self._add_permission(baseview)

    def add_view_no_menu(self, baseview, endpoint = None, static_folder = None):
        if baseview not in self.lst_baseview:
            baseview.baseapp = self
            self.lst_baseview.append(baseview)
            self.register_blueprint(baseview, endpoint = endpoint, static_folder = static_folder)
            self._add_permission(baseview)

    def _add_permission(self, baseview):
        pvm = PermissionView()
        bv = baseview()
        try:
            pvm.add_view_permissions(bv.base_permissions, bv.__class__.__name__)
        except:
            print "General _add_permission Error: DB not created?"
        bv = None
        pvm = None

    def register_blueprint(self, baseview, endpoint = None, static_folder = None):
        self.app.register_blueprint(baseview().create_blueprint(self,  endpoint = endpoint, static_folder = static_folder))
