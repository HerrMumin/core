""" Modul, um die Daten vom Broker zu erhalten.
"""

import json
import paho.mqtt.client as mqtt
import re

import bat
import chargepoint
import counter
import ev
import general
import graph
import optional
import prepare
import pv
import stats

class subData():
    """ Klasse, die die benötigten Topics abonniert, die Instanzen ertstellt, wenn z.b. ein Modul neu konfiguriert wird, 
    Instanzen löscht, wenn Module gelöscht werden, und die Werte in die Attribute der Instanzen schreibt.
    """

    #Instanzen
    cp_data={}
    cp_template_data={}
    pv_data={}
    pv_module_data={}
    ev_data={}
    ev_template_data={}
    ev_charge_template_data={}
    counter_data={}
    counter_module_data={}
    bat_module_data={}
    evu_data={}
    evu_module_data={}
    general_data={}
    optional_data={}
    graph_data={}

    def __init__(self):
        pass

    def sub_topics(self):
        """ abonniert alle Topics.
        """
        mqtt_broker_ip = "localhost"
        client = mqtt.Client("openWB-mqttsub-" + self.getserial())
        # ipallowed='^[0-9.]+$'
        # nameallowed='^[a-zA-Z ]+$'
        # namenumballowed='^[0-9a-zA-Z ]+$'

        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.message_callback_add("openWB/vehicle/#", self.process_vehicle_topic)
        client.message_callback_add("openWB/chargepoint/#", self.process_chargepoint_topic)
        client.message_callback_add("openWB/pv/#", self.process_pv_topic)
        client.message_callback_add("openWB/bat/#", self.process_bat_topic)
        client.message_callback_add("openWB/general/#", self.process_general_topic)
        client.message_callback_add("openWB/optional/#", self.process_optional_topic)
        client.message_callback_add("openWB/counter/#", self.process_counter_topic)
        client.message_callback_add("openWB/graph/#", self.process_graph_topic)
        # client.message_callback_add("openWB/smarthome/#", self.processSmarthomeTopic)
        client.message_callback_add("openWB/lp/#", self.processTest)

        client.connect(mqtt_broker_ip, 1883)
        client.loop_forever()
        client.disconnect()

    def getserial(self):
        """ Extract serial from cpuinfo file
        """
        with open('/proc/cpuinfo','r') as f:
            for line in f:
                if line[0:6] == 'Serial':
                    return line[10:26]
            return "0000000000000000"

    def on_connect(self, client, userdata, flags, rc):
        """ connect to broker and subscribe to set topics
        """
        client.subscribe("openWB/#", 2)

    def on_message(self, client, userdata, msg):
        """ wartet auf eingehende Topics.
        """
        #self.log_mqtt()
        #print("Unknown topic: "+msg.topic+", "+str(msg.payload.decode("utf-8")))

    def get_index(self, topic):
        """extrahiert den Index aus einemTtopic (zwischen zwei //)
        """
        index=re.search('(?!/)([0-9]+)(?=/)', topic)
        return index.group()

    def processTest(self, client, userdata, msg):
        if re.search("^openWB/lp/1/.+$", msg.topic) != None:
            index=self.get_index(msg.topic)
            if "lp"+index not in self.cp_data:
                self.cp_data["lp"+index]=chargepoint.chargepoint()
            if (re.search("^.+/VPhase1$", msg.topic) or re.search("^.+/VPhase2$", msg.topic)) != None:
                self.set_json_payload(self.cp_data["lp"+index].data, msg)
                #print(self.cp_data)
                #print(self.cp_data["cp1"].data)

    def set_json_payload(self, dict, msg):
        """ dekodiert das JSON-Objekt und setzt diesen für den Value in das übergebene Dictionary, als Key wird der Name nach dem letzten / verwendet.
        """
        key=re.search("/([a-z,A-Z,0-9]+)(?!.*/)", msg.topic).group(1)
        dict[key]=json.loads(str(msg.payload.decode("utf-8")))
 
    def process_vehicle_topic(self, client, userdata, msg):
        """ Handler für die EV-Topics
        """
        if re.search("^openWB/vehicle/[0-9]+/.+$", msg.topic) != None:
            index=self.get_index(msg.topic)
            if re.search("^openWB/vehicle/[0-9]+$", msg.topic) != None:
                if int(msg.payload)==1:
                    if "ev"+index not in self.ev_data:
                        self.ev_data["ev"+index]=ev.ev()
                else:
                    if "ev"+index in self.ev_data:
                        self.ev_data.pop("ev"+index)
            elif re.search("^openWB/vehicle/[0-9]+/get.+$", msg.topic) != None:
                if "get" not in self.ev_data["ev"+index].data:
                    self.ev_data["ev"+index].data["get"]={}
                self.set_json_payload(self.ev_data["ev"+index].data["get"], msg)
            elif re.search("^openWB/vehicle/[0-9]+/soc_config.+$", msg.topic) != None:
                if "soc_config" not in self.ev_data["ev"+index].data:
                    self.ev_data["ev"+index].data["soc_config"]={}
                self.set_json_payload(self.ev_data["ev"+index].data["soc_config"], msg)
            else: 
                self.set_json_payload(self.ev_data["ev"+index].data, msg)
        elif re.search("^openWB/vehicle/default.+$", msg.topic) != None:
            if "default" not in self.ev_data:
                self.ev_data["default"]=ev.ev()
            self.set_json_payload(self.ev_data["default"].data, msg)
        elif "openWB/vehicle/template/charge_template" in msg.topic:
            index=self.get_index(msg.topic)
            if re.search("^openWB/vehicle/template/charge_template/[0-9]+$", msg.topic) != None:
                if int(msg.payload)==1:
                    if "ct"+index not in self.ev_charge_template_data:
                        self.ev_charge_template_data["ct"+index]=ev.chargeTemplate()
                else:
                    if "ct"+index in self.ev_charge_template_data:
                        self.ev_charge_template_data.pop("ct"+index)
            elif re.search("^openWB/vehicle/template/charge_template/[0-9]+/charge_mode/instant_load/.+$", msg.topic) != None:
                if "instant_load" not in self.ev_charge_template_data["ct"+index].data:
                    self.ev_charge_template_data["ct"+index].data["instant_load"]={}
                self.set_json_payload(self.ev_charge_template_data["ct"+index].data["instant_load"], msg)
            elif re.search("^openWB/vehicle/template/charge_template/[0-9]+/charge_mode/pv_load/.+$", msg.topic) != None:
                if "pv_load" not in self.ev_charge_template_data["ct"+index].data:
                    self.ev_charge_template_data["ct"+index].data["pv_load"]={}
                self.set_json_payload(self.ev_charge_template_data["ct"+index].data["pv_load"], msg)
            elif re.search("^openWB/vehicle/template/charge_template/[0-9]+/charge_mode/scheduled_load/.+$", msg.topic) != None:
                if "scheduled_load" not in self.ev_charge_template_data["ct"+index].data:
                    self.ev_charge_template_data["ct"+index].data["scheduled_load"]={}
                index_second=re.search(".+/([0-9]+)/.+/([0-9]+)/.+", msg.topic).group(2)
                if re.search("^openWB/vehicle/template/charge_template/[0-9]+/charge_mode/scheduled_load/[0-9]+$", msg.topic) != None:
                    if int(msg.payload)==1:
                        if "plan"+index_second not in self.ev_charge_template_data["ct"+index].data["scheduled_load"]:
                            self.ev_charge_template_data["ct"+index].data["scheduled_load"]["plan"+index_second]={}
                    else:
                        if "plan"+index_second in self.ev_charge_template_data["ct"+index].data["scheduled_load"]:
                            self.ev_charge_template_data["ct"+index].data["scheduled_load"].pop("plan"+index_second)
                self.set_json_payload(self.ev_charge_template_data["ct"+index].data["scheduled_load"]["plan"+index_second], msg)
            elif re.search("^openWB/vehicle/template/chargeTecharge_templatemplate/[0-9]+/time_load/.+$", msg.topic) != None:
                if "pv_load" not in self.ev_charge_template_data["ct"+index].data:
                    self.ev_charge_template_data["ct"+index].data["time_load"]={}
                index_second=re.search(".+/([0-9]+)/.+/([0-9]+)/.+", msg.topic).group(2)
                if re.search("^openWB/vehicle/template/charge_template/[0-9]+/time_load/[0-9]+$", msg.topic) != None:
                    if int(msg.payload)==1:
                        if "plan"+index_second not in self.ev_charge_template_data["ct"+index].data["time_load"]:
                            self.ev_charge_template_data["ct"+index].data["time_load"]["plan"+index_second]={}
                    else:
                        if "plan"+index_second in self.ev_charge_template_data["ct"+index].data["time_load"]:
                            self.ev_charge_template_data["ct"+index].data["time_load"].pop("plan"+index_second)
                self.set_json_payload(self.ev_charge_template_data["ct"+index].data["time_load"]["plan"+index_second], msg)
            else:
                self.set_json_payload(self.ev_charge_template_data["ct"+index].data, msg)
        elif "openWB/vehicle/template/ev_template" in msg.topic:
            index=self.get_index(msg.topic)
            if re.search("^openWB/vehicle/template/ev_template/[0-9]+$", msg.topic) != None:
                if int(msg.payload)==1:
                    if "et"+index not in self.ev_template_data:
                        self.ev_template_data["et"+index]=ev.evTemplate()
                else:
                    if "et"+index in self.ev_template_data:
                        self.ev_template_data.pop("et"+index)
                self.set_json_payload(self.ev_template_data["et"+index].data, msg)

    def process_chargepoint_topic(self, client, userdata, msg):
        """ Handler für die Ladepunkt-Topics
        """
        if re.search("^openWB/chargepoint/[0-9]+/.+$", msg.topic) != None:
            index=self.get_index(msg.topic)
            if re.search("^openWB/chargepoint/[0-9]+$", msg.topic) != None:
                if int(msg.payload)==1:
                    if "cp"+index not in self.cp_data:
                        self.cp_data["cp"+index]=chargepoint.chargepoint()
                else:
                    if "cp"+index in self.cp_data:
                        self.cp_data.pop("cp"+index)
            elif re.search("^openWB/chargepoint/[0-9]+/get/.+$", msg.topic) != None:
                if "get" not in self.cp_data["cp"+index].data:
                    self.cp_data["cp"+index].data["get"]={}
                self.set_json_payload(self.cp_data["cp"+index].data["get"], msg)
            elif re.search("^openWB/chargepoint/[0-9]+/set/.+$", msg.topic) != None:
                if "set" not in self.cp_data["cp"+index].data:
                    self.cp_data["cp"+index].data["set"]={}
                self.set_json_payload(self.cp_data["cp"+index].data["set"], msg)
            elif re.search("^openWB/chargepoint/[0-9]+/config/.+$", msg.topic) != None:
                if "config" not in self.cp_data["cp"+index].data:
                    self.cp_data["cp"+index].data["config"]={}
                self.set_json_payload(self.cp_data["cp"+index].data["config"], msg)
        elif re.search("^openWB/chargepoint/template/[0-9]+/.+$", msg.topic) != None:
            index=self.get_index(msg.topic)
            if int(msg.payload)==1:
                if "cpt"+index not in self.cp_template_data:
                    self.cp_template_data["cpt"+index]=chargepoint.cpTemplate()
            else:
                if "cpt"+index in self.cp_template_data:
                    self.cp_template_data.pop("cpt"+index)
            self.set_json_payload(self.cp_template_data["cpt"+index].data, msg)
        print(self.cp_data["cp1"].data)

    def process_pv_topic(self, client, userdata, msg):
        """ Handler für die PV-Topics
        """
        if re.search("^openWB/pv/config/.+$", msg.topic) != None:
            if "config" not in self.pv_data:
                self.pv_data["config"]=pv.pv()
            self.set_json_payload(self.pv_data["config"].data, msg)
        elif re.search("^openWB/pv/modules/[0-9]+/.+$", msg.topic) != None:
            index=self.get_index(msg.topic)
            if re.search("^openWB/pv/modules/[0-9]+$", msg.topic) != None:
                if int(msg.payload)==1:
                    if "pv"+index not in self.pv_module_data:
                        self.pv_module_data["pv"+index]=pv.pvModule()
                else:
                    if "pv"+index in self.pv_module_data:
                        self.pv_module_data.pop("pv"+index)
            elif re.search("^openWB/pv/modules/[0-9]+/config/.+$", msg.topic) != None:
                if "config" not in self.pv_module_data["pv"+index].data:
                    self.pv_module_data["pv"+index].data["config"]={}
                self.set_json_payload(self.pv_module_data["pv"+index].data["config"], msg)
            elif re.search("^openWB/pv/modules/[0-9]+/get/.+$", msg.topic) != None:
                if "get" not in self.pv_module_data["pv"+index].data:
                    self.pv_module_data["pv"+index].data["get"]={}
                self.set_json_payload(self.pv_module_data["pv"+index].data["get"], msg)

    def process_bat_topic(self, client, userdata, msg):
        """ Handler für die Hausspeicher-Topics
        """
        if re.search("^openWB/bat/modules/[0-9]+/.+$", msg.topic) != None:
            index=self.get_index(msg.topic)
            if re.search("^openWB/bat/modules/[0-9]+$", msg.topic) != None:
                if int(msg.payload)==1:
                    if "bat"+index not in self.bat_module_data:
                        self.bat_module_data["bat"+index]=bat.batModule()
                else:
                    if "bat"+index in self.bat_module_data:
                        self.bat_module_data.pop("bat"+index)
            elif re.search("^openWB/bat/modules/[0-9]+/config/.+$", msg.topic) != None:
                if "config" not in self.bat_module_data["bat"+index].data:
                    self.bat_module_data["bat"+index].data["config"]={}
                self.set_json_payload(self.bat_module_data["bat"+index].data["config"], msg)
            elif re.search("^openWB/bat/modules/[0-9]+/get/.+$", msg.topic) != None:
                if "get" not in self.bat_module_data["bat"+index].data:
                    self.bat_module_data["bat"+index].data["get"]={}
                self.set_json_payload(self.bat_module_data["bat"+index].data["get"], msg)

    def process_general_topic(self, client, userdata, msg):
        """
        """
        if re.search("^openWB/general/.+$", msg.topic) != None:
            if "general" not in self.general_data:
                self.general_data["general"]=general.general()
            if re.search("^openWB/general/notifications/.+$", msg.topic) != None:
                if "notifications_config" not in self.general_data["general"].data:
                    self.general_data["general"].data["notifications_config"]={}
                self.set_json_payload(self.general_data["general"].data["notifications_config"], msg)
            else: 
                self.set_json_payload(self.general_data["general"].data, msg)

    def process_optional_topic(self, client, userdata, msg):
        """ Handler für die Optionalen-Topics
        """
        if re.search("^openWB/optional/.+$", msg.topic) != None:
            if "optional" not in self.optional_data:
                self.optional_data["optional"]=optional.optional()
            if re.search("^openWB/optional/led/.+$", msg.topic) != None:
                if "led" not in self.optional_data["optional"].data:
                    self.optional_data["optional"].data["led"]={}
                self.set_json_payload(self.optional_data["optional"].data["led"], msg)
            elif re.search("^openWB/optional/int_display/.+$", msg.topic) != None:
                if "int_display" not in self.optional_data["optional"].data:
                    self.optional_data["optional"].data["int_display"]={}
                self.set_json_payload(self.optional_data["optional"].data["int_display"], msg)
            else: 
                self.set_json_payload(self.optional_data["optional"].data, msg)

    def process_counter_topic(self, client, userdata, msg):
        """ Handler für die Zähler-Topics
        """
        if re.search("^openWB/counter/intermediate_counter/[0-9]+/.+$", msg.topic) != None:
            index=self.get_index(msg.topic)
            if re.search("^openWB/counter/intermediate_counter/[0-9]+$", msg.topic) != None:
                if int(msg.payload)==1:
                    if "counter"+index not in self.counter_module_data:
                        self.counter_module_data["counter"+index]=counter.counterModule()
                else:
                    if "counter"+index in self.counter_module_data:
                        self.counter_module_data.pop("counter"+index)
            elif re.search("^openWB/counter/intermediate_counter/[0-9]+/get.+$", msg.topic) != None:
                if "get" not in self.counter_module_data["counter"+index].data:
                    self.counter_module_data["counter"+index].data["get"]={}
                self.set_json_payload(self.counter_module_data["counter"+index].data["get"], msg)
            elif re.search("^openWB/counter/intermediate_counter/[0-9]+/config.+$", msg.topic) != None:
                if "config" not in self.counter_module_data["counter"+index].data:
                    self.counter_module_data["counter"+index].data["config"]={}
                self.set_json_payload(self.counter_module_data["counter"+index].data["config"], msg)
        elif re.search("^openWB/counter/evu.+$", msg.topic) != None:
            if "evu" not in self.counter_data:
                self.counter_data["evu"]=counter.counter()
            if re.search("^openWB/counter/evu/[0-9]+/get.+$", msg.topic) != None:
                if "get" not in self.counter_data["counter"+index].data:
                    self.counter_data["counter"+index].data["get"]={}
                self.set_json_payload(self.counter_data["counter"+index].data["get"], msg)
            elif re.search("^openWB/counter/evu/[0-9]+/config.+$", msg.topic) != None:
                if "config" not in self.counter_data["counter"+index].data:
                    self.counter_data["counter"+index].data["config"]={}
                self.set_json_payload(self.counter_data["counter"+index].data["config"], msg)

    def process_graph_topic(self, client, userdata, msg):
        """ Handler für die Graph-Topics
        """
        if re.search("^openWB/graph/.+$", msg.topic) != None:
            if "graph" not in self.graph_data:
                self.graph_data["graph"]=graph.graph()
            if re.search("^openWB/graph/config.+$", msg.topic) != None:
                if "config" not in self.graph_data["graph"].data:
                    self.graph_data["graph"].data["config"]={}
                self.set_json_payload(self.graph_data["graph"].data["config"], msg)
            elif re.search("^openWB/graph/values.+$", msg.topic) != None:
                if "values" not in self.graph_data["graph"].data:
                    self.graph_data["graph"].data["values"]={}
                self.set_json_payload(self.graph_data["graph"].data["values"], msg)

    # def processSmarthomeTopic(self, client, userdata, msg):
    #     """
    #     """
    #     pass

