import GlobalVariables as GV
class _domain_elements(object):
    # domain = ''
    # ARM = ''
    # ethernet_address = ''
    # server_name = ''

    def create_exemplar(self, _domain, _ARM, _ethernet_address, _server_name):
        self._domain = _domain
        self._ARM = _ARM
        self._ethernet_address = _ethernet_address
        self._server_name = _server_name
        print("Создан Новый экземпляр")
