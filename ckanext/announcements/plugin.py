from ckanext.announcements import actions, auth, blueprints, helpers
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.config.declaration import Declaration, Key


class announcementsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigDeclaration)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "announcements")

    # IConfigDeclaration

    def declare_config_options(self, declaration: Declaration, key: Key):
        declaration.annotate("ckanext-announcements settings")
        declaration.declare(
            key.ckanext.announcements.limit_announcements, 50
        ).set_validators("convert_int").set_description(
            "Maximum number of announcements shown in the admin list"
        )

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "get_all_announcements": helpers.get_all_announcements,
            "get_public_announcements": helpers.get_public_announcements,
        }

    # IBlueprint

    def get_blueprint(self):
        return [
            blueprints.announcements_blueprint,
        ]

    # IAuthFunctions

    def get_auth_functions(self):
        functions = {
            "announcement_create": auth.announcement_create,
            "announcement_update": auth.announcement_update,
            "announcement_delete": auth.announcement_delete,
            "announcement_show": auth.announcement_show,
        }
        return functions

    # IActions

    def get_actions(self):
        functions = {
            "announcement_create": actions.announcement_create,
            "announcement_update": actions.announcement_update,
            "announcement_delete": actions.announcement_delete,
            "announcement_show": actions.announcement_show,
        }
        return functions
