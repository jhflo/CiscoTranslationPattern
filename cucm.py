from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning




def updatetp(celular, proyecto, ambito):
    disable_warnings(InsecureRequestWarning)
    username = 'python'
    password = '12345'
    # If you're not disabling SSL verification, host should be the FQDN of the server rather than IP
    host = '172.16.4.100'

    wsdl = '/app/axlsqltoolkit/schema/current/AXLAPI.wsdl'
    location = 'https://{host}:8443/axl/'.format(host=host)
    binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

    # Create a custom session to disable Certificate verification.
    # In production you shouldn't do this,
    # but for testing it saves having to have the certificate in the trusted store.
    session = Session()
    session.verify = False
    session.auth = HTTPBasicAuth(username, password)

    transport = Transport(cache=SqliteCache(), session=session, timeout=20)
    history = HistoryPlugin()
    client = Client(wsdl=wsdl, transport=transport, plugins=[history])
    service = client.create_service(binding, location)
    try:
        if proyecto == "Colsubsidio" and ambito == "Bases de datos":
            final_num = "*03" + str(celular)
            resp = service.updateTransPattern(calledPartyTransformationMask=final_num, pattern='44904', routePartitionName="Internas")
            return "Cambio realizado por favor verificar con una llamada"
        elif proyecto == "Colsubsidio" and ambito == "Microsoft":
            final_num = "*03" + str(celular)
            resp = service.updateTransPattern(calledPartyTransformationMask=final_num, pattern='44903',
                                              routePartitionName="Internas")
            return "Cambio realizado por favor verificar con una llamada"

    except Fault:
        return "Error al actualizar contacta el adminsitrador del CUCM"
