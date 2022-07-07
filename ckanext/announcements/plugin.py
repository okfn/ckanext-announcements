from ckanext.announcements import helpers, blueprints
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class announcementsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'announcements')
        toolkit.add_ckan_admin_tab(config_, 'announcements.index', 'Announcements', icon='bell')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_announcements': helpers.get_announcements,
        }

    # IBlueprint

    def get_blueprint(self):
        return [
            blueprints.announcements_blueprint,
        ]
