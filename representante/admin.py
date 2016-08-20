from django.contrib import admin
from models import Representante

from import_export import resources, fields
from import_export.admin import ImportMixin

# Register your models here.

class RepresentanteResource(resources.ModelResource):
	class Meta:
		model = Representante
		fields = ('id', 'apellidos', 'nombres')
		import_order = fields
		IMPORT_EXPORT_SKIP_ADMIN_LOG = True

#@admin.register(Representante)
class RepresentanteAdmin(ImportMixin, admin.ModelAdmin):
	list_display = ['nombres', 'apellidos', ]
	resource_class = RepresentanteResource

admin.site.register(Representante, RepresentanteAdmin)