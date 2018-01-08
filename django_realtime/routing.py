from channels.routing import route, route_class
from channels.staticfiles import StaticFilesConsumer
from django_realtime import consumers
from django_realtime.consumers import ws_add_dashboard, ws_message_dashboard, ws_disconnect_dashboard, msg_consumer_dashboard, \
                            ws_add_technicians, ws_message_technicians, ws_disconnect_technicians, msg_consumer_technicians, \
                            ws_add_jobs, ws_message_jobs, ws_disconnect_jobs, msg_consumer_jobs, \
                            ws_add_biogas, ws_message_biogas, ws_disconnect_biogas, msg_consumer_biogas        
 
# routes defined for channel calls
# this is similar to the Django urls, but specifically for Channels
channel_routing = [
    #route_class(consumers.DashboardConsumer,  path=r"^/dashboard/"),
    route("websocket.connect", ws_add_dashboard,path=r"^/dashboard/"),
    route("websocket.receive", ws_message_dashboard,path=r"^/dashboard/"),
    route("websocket.disconnect", ws_disconnect_dashboard,path=r"^/dashboard/"),
    route("updatedata", msg_consumer_dashboard),

    route("websocket.connect", ws_add_technicians,path=r"^/technicians/"),
    route("websocket.receive", ws_message_technicians,path=r"^/technicians/"),
    route("websocket.disconnect", ws_disconnect_technicians,path=r"^/technicians/"),
    route("updatedata", msg_consumer_technicians),

    route("websocket.connect", ws_add_jobs,path=r"^/jobs/"),
    route("websocket.receive", ws_message_jobs,path=r"^/jobs/"),
    route("websocket.disconnect", ws_disconnect_jobs,path=r"^/jobs/"),
    route("updatedata", msg_consumer_jobs),

    route("websocket.connect", ws_add_biogas,path=r"^/biogasplants/"),
    route("websocket.receive", ws_message_biogas,path=r"^/biogasplants/"),
    route("websocket.disconnect", ws_disconnect_biogas,path=r"^/biogasplants/"),
    route("updatedata", msg_consumer_biogas),
]