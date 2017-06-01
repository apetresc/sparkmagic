# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.
from sparkmagic.controllerwidget.abstractmenuwidget import AbstractMenuWidget
from sparkmagic.controllerwidget.addendpointwidget import AddEndpointWidget
from sparkmagic.controllerwidget.manageendpointwidget import ManageEndpointWidget
from sparkmagic.controllerwidget.managesessionwidget import ManageSessionWidget
from sparkmagic.controllerwidget.createsessionwidget import CreateSessionWidget
from sparkmagic.livyclientlib.endpoint import Endpoint
import sparkmagic.utils.configuration as conf


class MagicsControllerWidget(AbstractMenuWidget):
    def __init__(self, spark_controller, ipywidget_factory, ipython_display, endpoints=None):
        super(MagicsControllerWidget, self).__init__(spark_controller, ipywidget_factory, ipython_display)

        if endpoints is None:
            endpoints = {endpoint.url: endpoint for endpoint in self._get_default_endpoints()}
        self.endpoints = endpoints

        self._refresh()

    def run(self):
        pass

    def _get_default_endpoints(self):
        default_endpoints = set()
        kernel_types = ['python', 'python3', 'scala', 'r']

        for kernel_type in kernel_types:
            endpoint_credentials = getattr(conf, 'kernel_%s_credentials' % kernel_type)()
            if "url" not in endpoint_credentials or endpoint_credentials["url"] == "" or "password" not in endpoint_credentials:
                continue
            default_endpoints.add(Endpoint(
                username=endpoint_credentials["username"],
                password=endpoint_credentials["password"],
                url=endpoint_credentials["url"],
                is_default=True))

        return default_endpoints

    def _refresh(self):
        self.endpoints_dropdown_widget = self.ipywidget_factory.get_dropdown(
                description="Endpoint:",
                options=self.endpoints
        )

        self.manage_session = ManageSessionWidget(self.spark_controller, self.ipywidget_factory, self.ipython_display,
                                                  self._refresh)
        self.create_session = CreateSessionWidget(self.spark_controller, self.ipywidget_factory, self.ipython_display,
                                                  self.endpoints_dropdown_widget, self._refresh)
        self.add_endpoint = AddEndpointWidget(self.spark_controller, self.ipywidget_factory, self.ipython_display,
                                              self.endpoints, self.endpoints_dropdown_widget, self._refresh)
        self.manage_endpoint = ManageEndpointWidget(self.spark_controller, self.ipywidget_factory, self.ipython_display,
                                                    self.endpoints, self._refresh)

        self.tabs = self.ipywidget_factory.get_tab(children=[self.manage_session, self.create_session,
                                                             self.add_endpoint, self.manage_endpoint])
        self.tabs.set_title(0, "Manage Sessions")
        self.tabs.set_title(1, "Create Session")
        self.tabs.set_title(2, "Add Endpoint")
        self.tabs.set_title(3, "Manage Endpoints")

        self.children = [self.tabs]

        for child in self.children:
            child.parent_widget = self
