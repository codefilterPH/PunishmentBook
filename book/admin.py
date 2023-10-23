from .models import (
    OffenseLibrary, PlaceOfOmission, PunishmentLibrary, ImposedByWhom, Resolution, Offense, AFP_Personnel
)
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup
)


class OffenseLibraryAdmin(ModelAdmin):
    model = OffenseLibrary
    menu_label = 'Offense Library'
    base_url_path = "offense-record-admin"
    menu_icon = 'folder-open-1'
    menu_order = 100
    can_create = True
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('violation',)
    search_fields = ('violation',)


class PlaceOfOmissionAdmin(ModelAdmin):
    model = PlaceOfOmission
    menu_label = 'Place of Omission'
    base_url_path = "place-omission-admin"
    menu_icon = 'date'
    menu_order = 100
    can_create = True
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('place', 'date')
    list_filter = ('place', 'date')
    search_fields = ('place', 'date')


class PunishmentLibraryAdmin(ModelAdmin):
    model = PunishmentLibrary
    menu_label = 'Punishment Library'
    base_url_path = "punishment-libray-admin"
    menu_icon = 'form'
    menu_order = 100
    can_create = True
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('punishment',)
    list_filter = ('punishment',)
    search_fields = ('punishment',)


class ImposedByWhomAdmin(ModelAdmin):
    model = ImposedByWhom
    menu_label = 'Imposed by Whom'
    base_url_path = "imposed-by-whom-admin"
    menu_icon = 'user'
    menu_order = 100
    can_create = True
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class ResolutionAdmin(ModelAdmin):
    model = Resolution
    menu_label = 'Resolution'
    base_url_path = "resolution-admin"
    menu_icon = 'view'
    menu_order = 100
    can_create = True
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('decision_of_appeal', 'mitigation_re_remission', 'remarks', 'date', 'intl_first_sergeant', 'initial_of_ep')
    list_filter = ('decision_of_appeal', 'date')
    search_fields = ('decision_of_appeal', 'intl_first_sergeant')


class AFPPersonnelAdmin(ModelAdmin):
    model = AFP_Personnel
    menu_label = 'AFP Personnel'
    base_url_path = "afp-personnel-admin"
    menu_icon = 'group'
    menu_order = 103
    can_create = True
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('rank_id', 'last_name', 'first_name', 'middle_name', 'afpsn',)
    list_filter = ('rank_id', 'last_name', 'afpsn')
    search_fields = ('rank_id', 'last_name', 'afpsn')


class OffenseAdmin(ModelAdmin):
    model = Offense
    menu_label = 'Submitted Offense'
    base_url_path = "submitted-offense-admin"
    menu_icon = 'upload'
    menu_order = 103
    can_create = True
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('offense', 'place', 'display_punishments', 'display_imposers', 'display_resolutions')
    list_filter = ('place__place', 'punishments__punishment', 'imposer__name', 'resolution__date')
    search_fields = (
        'offense__name', 'place__place', 'punishments__punishment', 'imposer__name', 'resolution__date'
    )

    def display_punishments(self, obj):
        return ", ".join([p.punishment for p in obj.punishments.all()])

    display_punishments.short_description = 'Punishments'

    def display_imposers(self, obj):
        return ", ".join([i.name for i in obj.imposer.all()])

    display_imposers.short_description = 'Imposers'

    def display_resolutions(self, obj):
        return ", ".join([str(r.date) for r in obj.resolution.all()])

    display_resolutions.short_description = 'Resolutions'


class ManageBookGroupAdmin(ModelAdminGroup):
    menu_label = "Punishment Book"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = True
    items = (
        OffenseAdmin,
        OffenseLibraryAdmin,
        PlaceOfOmissionAdmin,
        PunishmentLibraryAdmin,
        ImposedByWhomAdmin,
        ResolutionAdmin,
        AFPPersonnelAdmin,
    )

    # Override to restrict access to only 'admin' group
    @staticmethod
    def is_registered(request):
        user = request.user
        # Check if the user is in the 'admin' group
        return user.is_active and (user.is_superuser or user.groups.filter(name='admin').exists())


modeladmin_register(ManageBookGroupAdmin)
